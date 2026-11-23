#!/usr/bin/env bash
# Vektra Laws installer for Linux, macOS and WSL2.
#
#   curl -fsSL https://vektraindustries.com/laws/install.sh | bash
#
# Want to read it first? (recommended)
#   curl -fsSL https://vektraindustries.com/laws/install.sh -o install.sh
#   less install.sh && bash install.sh
#
# What it does, and nothing more:
#   1. checks for Python 3.10+ and git
#   2. downloads the newest Vektra Laws release (a tag, never unreleased code) into ~/.vektra-laws/src
#   3. before running any of it, checks every file against the signed LAWS.lock with the checker
#      built into this script, and refuses an older release than one already installed
#   4. makes a private Python environment in ~/.vektra-laws/venv (no sudo, no system packages) and
#      installs packages only if their hashes match requirements.txt
#   5. checks the Laws again with the Core itself; stops if anything fails
#   6. adds the `vektra-laws` command to ~/.local/bin
#   7. runs `vektra-laws setup`, the wizard, when you are at a terminal
#
# Options:  --ref <tag>   --dir <path>   --no-setup   --require-signature   --help
#           (--ref main installs unreleased development code; it is never chosen for you)
# Env:      VEKTRA_LAWS_HOME, VEKTRA_LAWS_REF, VEKTRA_LAWS_BIN, VEKTRA_LAWS_REPO
#
# The whole script is one function that runs on the last line, so a download cut off halfway
# runs nothing.
set -euo pipefail

# Steward key fingerprints: SHA-256 of each raw Ed25519 public key, comma-separated (the main key,
# then the recovery key). The same values are published in VERIFYING.md, on vektraindustries.com
# and on the steward's profiles. When this is set, the installer requires the Laws to be signed by
# one of these keys, and every run of the engine pins them too. Empty until the first signed release.
PINNED_KEYS="c41973a80abab5a0f8e78513f4c3ba04d684c6fd8183a10f9c2fb816f1183150,ad45f28f13572602b0c1ffc7b4087d49d3f62243a42536f732edcdd62aa7d0d9"

main() {

# BEGIN PREVERIFY: generated from install/preverify.py by tools/embed_preverify.py. Do not edit here.
PREVERIFY=''
IFS= read -r -d '' PREVERIFY <<'PYEOF' || true
"""Check a Vektra Laws download BEFORE any of its code runs. Python standard library only.

The installers carry a copy of this file inside them (tools/embed_preverify.py keeps the copies in
sync), so the check comes from the installer you fetched, not from the download it is checking.
It runs with `python -I`, so nothing in the download can be imported by accident.

It checks, in order:
  1. core/LAWS.lock is the v2 format and its digest is the hash of what it lists.
  2. Every file the lock lists (laws.yaml, requirements.txt, all Core code) has the listed SHA-256,
     and no unlisted Python file sits in the Core package.
  3. When steward fingerprints are pinned: the lock is signed by a pinned Ed25519 key.
  4. The lock's sequence number is not older than one already installed (no rollback).
  5. A release tag matches the version in the lock.

    python -I preverify.py --src DIR [--pinned FPR,FPR] [--min-sequence N] [--expect-version V]
                           [--require-signature]
Exit 0 and a last line SEQUENCE=<n> when it passes; exit 1 with the reason when it does not.
"""
import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

LOCK_FORMAT = "vektra-laws-lock/v2"
SIGNED_FIELDS = ("format", "version", "sequence", "sha256", "files")
CODE_DIR = "core/vektra_laws_core"
KEY_FILES = ("core/keys/steward-ed25519.pub", "core/keys/recovery-ed25519.pub")
SPKI_ED25519 = bytes.fromhex("302a300506032b6570032100")


def file_digest(path: Path) -> str:
    # Line endings are normalised, so a Windows checkout (CRLF) hashes the same as Linux (LF).
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def lock_digest(lock: dict) -> str:
    body = {k: lock[k] for k in SIGNED_FIELDS}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def raw_public_key(pem: bytes) -> bytes:
    lines = [ln.strip() for ln in pem.decode("ascii").splitlines()]
    if "-----BEGIN PUBLIC KEY-----" not in lines:
        raise ValueError("not a PEM public key")
    body = lines[lines.index("-----BEGIN PUBLIC KEY-----") + 1:lines.index("-----END PUBLIC KEY-----")]
    der = base64.b64decode("".join(body))
    if len(der) != 44 or not der.startswith(SPKI_ED25519):
        raise ValueError("not an Ed25519 public key")
    return der[12:]


def fingerprint(pem: bytes) -> str:
    """SHA-256 of the raw 32-byte key: the same value `vektra-laws fingerprint` prints."""
    return hashlib.sha256(raw_public_key(pem)).hexdigest()


# Ed25519 signature check (RFC 8032, section 5.1.7). Verification only; no secrets are handled here.
_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_I = pow(2, (_P - 1) // 4, _P)


def _recover_x(y: int, sign: int):
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P:
        x = x * _I % _P
    if (x * x - x2) % _P:
        return None
    if (x & 1) != sign:
        x = _P - x
    return x


def _add(a, b):
    A = (a[1] - a[0]) * (b[1] - b[0]) % _P
    B = (a[1] + a[0]) * (b[1] + b[0]) % _P
    C = 2 * a[3] * b[3] * _D % _P
    D = 2 * a[2] * b[2] % _P
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _P, G * H % _P, F * G % _P, E * H % _P)


def _mul(s: int, pt):
    q = (0, 1, 1, 0)
    while s:
        if s & 1:
            q = _add(q, pt)
        pt = _add(pt, pt)
        s >>= 1
    return q


def _same(a, b) -> bool:
    return (a[0] * b[2] - b[0] * a[2]) % _P == 0 and (a[1] * b[2] - b[1] * a[2]) % _P == 0


def _point(s: bytes):
    y = int.from_bytes(s, "little")
    sign, y = y >> 255, y & ((1 << 255) - 1)
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % _P)


_GY = 4 * pow(5, _P - 2, _P) % _P
_GX = _recover_x(_GY, 0)
_G = (_GX, _GY, 1, _GX * _GY % _P)


def ed25519_verify(public: bytes, message: bytes, signature: bytes) -> bool:
    if len(public) != 32 or len(signature) != 64:
        return False
    a, r = _point(public), _point(signature[:32])
    if a is None or r is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= _L:
        return False
    h = int.from_bytes(hashlib.sha512(signature[:32] + public + message).digest(), "little") % _L
    return _same(_mul(s, _G), _add(r, _mul(h, a)))


class Stop(Exception):
    pass


def check(src: Path, pinned: set, min_sequence: int = 0, expect_version: str = "",
          require_signature: bool = False) -> dict:
    lock_path = src / "core" / "LAWS.lock"
    if not lock_path.exists():
        raise Stop("core/LAWS.lock is missing.")
    lock = json.loads(lock_path.read_text())
    if lock.get("format") != LOCK_FORMAT:
        raise Stop(f"LAWS.lock is format {lock.get('format')!r}; this installer needs {LOCK_FORMAT}.")
    digest = lock_digest(lock)
    if lock.get("digest") != digest:
        raise Stop("LAWS.lock does not hash to its own digest; it was edited.")

    files = lock["files"]
    for rel, want in sorted(files.items()):
        p = src / rel
        if ".." in Path(rel).parts or not p.is_file():
            raise Stop(f"{rel} is listed in LAWS.lock but missing.")
        if file_digest(p) != want:
            raise Stop(f"{rel} does not match LAWS.lock; it was changed after signing.")
    for p in sorted((src / CODE_DIR).rglob("*.py")):
        rel = p.relative_to(src).as_posix()
        if "__pycache__" not in rel and rel not in files:
            raise Stop(f"{rel} is not listed in LAWS.lock; unknown code was added.")

    status = {"version": lock["version"], "sequence": int(lock["sequence"]), "digest": digest,
              "signed": False, "key": None}
    if pinned or require_signature:
        if not lock.get("signature"):
            raise Stop("A signed LAWS.lock is required, and none was found.")
        sig = base64.b64decode(lock["signature"])
        keys = [src / k for k in KEY_FILES if (src / k).exists()]
        usable = [(fingerprint(k.read_bytes()), k) for k in keys]
        if pinned:
            usable = [(f, k) for f, k in usable if f in pinned]
            if not usable:
                raise Stop("The public key in this download is not a pinned steward key.")
        for fpr, k in usable:
            if ed25519_verify(raw_public_key(k.read_bytes()), bytes.fromhex(digest), sig):
                status.update(signed=True, key=fpr)
                break
        else:
            raise Stop("The LAWS.lock signature is not valid for a pinned steward key.")

    if status["sequence"] < min_sequence:
        raise Stop(f"This release (sequence {status['sequence']}) is older than the one already "
                   f"installed (sequence {min_sequence}). Rolling back is refused.")
    if expect_version and expect_version.lstrip("v") != status["version"]:
        raise Stop(f"Release {expect_version} contains Laws {status['version']}; they must match.")
    return status


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--pinned", default="")
    ap.add_argument("--min-sequence", type=int, default=0)
    ap.add_argument("--expect-version", default="")
    ap.add_argument("--require-signature", action="store_true")
    a = ap.parse_args(argv)
    pinned = {f.strip().lower() for f in a.pinned.split(",") if f.strip()}
    try:
        st = check(a.src, pinned, a.min_sequence, a.expect_version, a.require_signature)
    except (Stop, ValueError, KeyError) as e:
        print(f"FAIL: {e}")
        return 1
    print(f"OK: every file matches LAWS.lock (Vektra Laws {st['version']}, sequence {st['sequence']}).")
    if st["signed"]:
        print(f"    Signed by pinned steward key {st['key']}.")
    else:
        print("    Pre-release: no steward key is pinned in this installer yet.")
    print(f"SEQUENCE={st['sequence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF
# END PREVERIFY

REPO="${VEKTRA_LAWS_REPO:-https://github.com/Vektra-Industries/vektra-laws.git}"
API="https://api.github.com/repos/Vektra-Industries/vektra-laws/releases/latest"
VL_HOME="${VEKTRA_LAWS_HOME:-$HOME/.vektra-laws}"
BIN_DIR="${VEKTRA_LAWS_BIN:-$HOME/.local/bin}"
REF="${VEKTRA_LAWS_REF:-}"
RUN_SETUP=1
REQUIRE_SIG=0
TRUSTED="${VEKTRA_LAWS_TRUSTED_KEYS:-$PINNED_KEYS}"

if [ -t 1 ]; then B=$'\033[1m'; G=$'\033[33m'; R=$'\033[31m'; N=$'\033[0m'; else B=""; G=""; R=""; N=""; fi
say()  { printf '%s\n' "${G}==>${N} ${B}$*${N}"; }
fail() { printf '%s\n' "${R}error:${N} $*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --ref) REF="${2:?--ref needs a value}"; shift 2 ;;
    --dir) VL_HOME="${2:?--dir needs a value}"; shift 2 ;;
    --no-setup) RUN_SETUP=0; shift ;;
    --require-signature) REQUIRE_SIG=1; shift ;;
    -h|--help) sed -n '2,35p' "$0" 2>/dev/null || true; exit 0 ;;
    *) fail "unknown option: $1 (try --help)" ;;
  esac
done

printf '\n%s\n%s\n\n' "${B}Vektra Laws${N}" "A safety core for AI, agents and robots. Humans stay in command."

# 1. Requirements ----------------------------------------------------------------------------------
PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys, venv, ensurepip; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$(command -v "$c")"; break
  fi
done
[ -n "$PY" ] || fail "Python 3.10 or newer, with venv, is needed. Ubuntu/Debian: sudo apt install python3 python3-venv   macOS: brew install python"
command -v git >/dev/null 2>&1 || fail "git is needed. Ubuntu/Debian: sudo apt install git   macOS: xcode-select --install"
say "Python $("$PY" -c 'import platform; print(platform.python_version())') and git found"

# 2. Download --------------------------------------------------------------------------------------
if [ -z "$REF" ] && command -v curl >/dev/null 2>&1; then
  REF="$(curl -fsSL "$API" 2>/dev/null | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n1 || true)"
fi
[ -n "$REF" ] || fail "No Vektra Laws release could be found. Check your connection. To try unreleased development code instead, rerun with: --ref main"
SRC="$VL_HOME/src"
mkdir -p "$VL_HOME"
chmod 700 "$VL_HOME"
if [ -d "$SRC/.git" ]; then
  say "Updating Vektra Laws in $SRC to $REF"
  git -C "$SRC" fetch --quiet --tags origin
  git -C "$SRC" checkout --quiet --force "$REF" 2>/dev/null || git -C "$SRC" checkout --quiet --force "origin/$REF"
else
  say "Downloading Vektra Laws ($REF) into $SRC"
  rm -rf "$SRC"
  git clone --quiet --depth 1 --branch "$REF" "$REPO" "$SRC" \
    || fail "Download failed. Check your connection, or that release $REF exists."
fi
COMMIT="$(git -C "$SRC" rev-parse --short=12 HEAD)"

# 3. Check the download before any of it runs ------------------------------------------------------
say "Checking every file against LAWS.lock, before running anything"
STATE="$VL_HOME/state.json"
MIN_SEQ="$("$PY" -I -c 'import json, sys; print(int(json.load(open(sys.argv[1])).get("min_sequence", 0)))' "$STATE" 2>/dev/null || echo 0)"
EXPECT=""
case "$REF" in v[0-9]*) EXPECT="$REF" ;; esac
PV="$VL_HOME/preverify.py"
printf '%s\n' "$PREVERIFY" > "$PV"
PVARGS=(--src "$SRC" --pinned "$TRUSTED" --min-sequence "$MIN_SEQ")
[ -n "$EXPECT" ] && PVARGS+=(--expect-version "$EXPECT")
[ "$REQUIRE_SIG" = 1 ] && PVARGS+=(--require-signature)
PV_OUT="$("$PY" -I "$PV" "${PVARGS[@]}")" || {
  printf '%s\n' "$PV_OUT"
  fail "This download did not verify, so none of it was run. Nothing was installed on your PATH. Please report this to security@vektraindustries.com."
}
printf '%s\n' "$PV_OUT" | grep -v '^SEQUENCE=' | sed 's/^/    /'
SEQ="$(printf '%s\n' "$PV_OUT" | sed -n 's/^SEQUENCE=//p')"

# 4. Private Python environment --------------------------------------------------------------------
VENV="$VL_HOME/venv"
if [ ! -x "$VENV/bin/python" ]; then
  say "Making a private Python environment"
  "$PY" -m venv "$VENV"
fi
say "Installing packages (each one checked against its hash in requirements.txt)"
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --require-hashes -r "$SRC/requirements.txt" \
  || fail "A package did not match its hash, or could not be downloaded. Nothing was installed on your PATH."

# 5. Verify the Laws with the Core -----------------------------------------------------------------
say "Checking the Laws with the Core"
VARGS=()
[ "$REQUIRE_SIG" = 1 ] && VARGS+=(--require-signature)
OLD_IFS="$IFS"; IFS=','
for f in $TRUSTED; do f="${f// /}"; [ -n "$f" ] && VARGS+=(--expect-key "$f"); done
IFS="$OLD_IFS"
PYTHONPATH="$SRC/core" VEKTRA_LAWS_TRUSTED_KEYS="$TRUSTED" "$VENV/bin/python" -m vektra_laws_core verify ${VARGS[@]+"${VARGS[@]}"} \
  || fail "The Laws did not verify. Nothing was installed on your PATH. Please report this to security@vektraindustries.com."
printf '{"min_sequence": %s}\n' "${SEQ:-0}" > "$STATE"

# 6. The command -----------------------------------------------------------------------------------
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/vektra-laws"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
# vektra-laws launcher, written by the Vektra Laws installer. Remove with: vektra-laws uninstall
export VEKTRA_LAWS_HOME="$VL_HOME"
export VEKTRA_LAWS_BIN="$BIN_DIR"
export VEKTRA_LAWS_TRUSTED_KEYS="$TRUSTED"
export PYTHONPATH="$SRC/core\${PYTHONPATH:+:\$PYTHONPATH}"
exec "$VENV/bin/python" -m vektra_laws_core "\$@"
EOF
chmod 755 "$LAUNCHER"
say "Installed the vektra-laws command at $LAUNCHER (commit $COMMIT)"

case ":$PATH:" in
  *":$BIN_DIR:"*) ON_PATH=1 ;;
  *) ON_PATH=0
     RCS=""
     for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do [ -f "$rc" ] && RCS="$RCS $rc"; done
     [ -n "$RCS" ] || RCS="$HOME/.profile"
     for rc in $RCS; do
       if ! grep -qs "# vektra-laws" "$rc"; then
         # shellcheck disable=SC2016  # $PATH must stay literal in the rc file
         printf '\nexport PATH="%s:$PATH"  # vektra-laws\n' "$BIN_DIR" >> "$rc"
       fi
     done ;;
esac

# 7. Setup wizard ----------------------------------------------------------------------------------
if [ "$RUN_SETUP" = 1 ] && [ -t 1 ] && { : </dev/tty; } 2>/dev/null; then
  printf '\n'
  "$LAUNCHER" setup </dev/tty || true
else
  printf '\nRun %s in your project folder to set it up.\n' "${B}vektra-laws setup${N}"
fi

printf '\n%s\n' "${B}Done.${N} Useful commands:"
printf '  vektra-laws setup     add the guard to a project\n'
printf '  vektra-laws doctor    check everything\n'
printf '  vektra-laws verify    check the Laws are the real, unchanged text\n'
printf '  vektra-laws update    move to the newest release\n'
[ "$ON_PATH" = 1 ] || printf '\nOpen a new terminal (or run: source ~/.bashrc) so the command is found.\n'
}

main "$@"
