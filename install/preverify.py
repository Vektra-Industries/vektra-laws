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
