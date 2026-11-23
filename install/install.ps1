# Vektra Laws installer for Windows (PowerShell 5.1 or 7+).
#
#   iex (irm https://vektraindustries.com/laws/install.ps1)
#
# Read it first (recommended):
#   irm https://vektraindustries.com/laws/install.ps1 -OutFile install.ps1; notepad install.ps1
#   powershell -ExecutionPolicy Bypass -File install.ps1
#
# Same steps as install.sh: check Python 3.10+ and git, download the newest release (never unreleased
# code unless you set VEKTRA_LAWS_REF=main) into %LOCALAPPDATA%\vektra-laws\src, check every file
# against the signed LAWS.lock BEFORE running any of it, make a private venv with hash-checked
# packages, verify the Laws again with the Core, add the vektra-laws command, run setup.
# Env: VEKTRA_LAWS_HOME, VEKTRA_LAWS_REF, VEKTRA_LAWS_REPO, VEKTRA_LAWS_NO_SETUP=1
$ErrorActionPreference = "Stop"

# Steward key fingerprints (SHA-256 of each raw Ed25519 public key), comma-separated: main key, then
# recovery key. Same values as VERIFYING.md and vektraindustries.com. Empty until the first signed release.
$PinnedKeys = ""
$Trusted = if ($env:VEKTRA_LAWS_TRUSTED_KEYS) { $env:VEKTRA_LAWS_TRUSTED_KEYS } else { $PinnedKeys }

function Install-VektraLaws {
# BEGIN PREVERIFY: generated from install/preverify.py by tools/embed_preverify.py. Do not edit here.
$PreVerify = @'
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
'@
# END PREVERIFY
$Repo   = if ($env:VEKTRA_LAWS_REPO) { $env:VEKTRA_LAWS_REPO } else { "https://github.com/Vektra-Industries/vektra-laws.git" }
$Api    = "https://api.github.com/repos/Vektra-Industries/vektra-laws/releases/latest"
$VLHome = if ($env:VEKTRA_LAWS_HOME) { $env:VEKTRA_LAWS_HOME } else { Join-Path $env:LOCALAPPDATA "vektra-laws" }
$Ref    = $env:VEKTRA_LAWS_REF

function Say($m)  { Write-Host "==> $m" -ForegroundColor Yellow }
function Fail($m) { Write-Host "error: $m" -ForegroundColor Red; throw $m }

Write-Host "`nVektra Laws" -ForegroundColor White
Write-Host "A safety core for AI, agents and robots. Humans stay in command.`n"

# 1. Requirements
$Py = $null
foreach ($c in @(@("py", "-3"), @("python"), @("python3"))) {
    $exe = Get-Command $c[0] -ErrorAction SilentlyContinue
    if (-not $exe) { continue }
    $args0 = @($c | Select-Object -Skip 1)
    & $exe.Source @args0 -c "import sys, venv, ensurepip; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) { $Py = @($exe.Source) + $args0; break }
}
if (-not $Py) { Fail "Python 3.10 or newer is needed. Install it with: winget install Python.Python.3.12" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail "git is needed. Install it with: winget install Git.Git" }
Say "Python and git found"

# 2. Download
if (-not $Ref) {
    try { $Ref = (Invoke-RestMethod -Uri $Api -UseBasicParsing).tag_name } catch { $Ref = $null }
}
if (-not $Ref) { Fail "No Vektra Laws release could be found. Check your connection. To try unreleased development code instead, set VEKTRA_LAWS_REF=main and rerun." }
$Src = Join-Path $VLHome "src"
New-Item -ItemType Directory -Force -Path $VLHome | Out-Null
if (Test-Path (Join-Path $Src ".git")) {
    Say "Updating Vektra Laws in $Src to $Ref"
    git -C $Src fetch --quiet --tags origin
    git -C $Src checkout --quiet --force $Ref 2>$null
    if ($LASTEXITCODE -ne 0) { git -C $Src checkout --quiet --force "origin/$Ref" }
} else {
    Say "Downloading Vektra Laws ($Ref) into $Src"
    if (Test-Path $Src) { Remove-Item -Recurse -Force $Src }
    git clone --quiet --depth 1 --branch $Ref $Repo $Src
    if ($LASTEXITCODE -ne 0) { Fail "Download failed. Check your connection, or that release $Ref exists." }
}

# 3. Check the download before any of it runs
Say "Checking every file against LAWS.lock, before running anything"
$State = Join-Path $VLHome "state.json"
$MinSeq = 0
if (Test-Path $State) { try { $MinSeq = [int](Get-Content $State -Raw | ConvertFrom-Json).min_sequence } catch { $MinSeq = 0 } }
$Pv = Join-Path $VLHome "preverify.py"
Set-Content -Encoding UTF8 -Path $Pv -Value $PreVerify
$pvArgs = @($Py | Select-Object -Skip 1) + @("-I", $Pv, "--src", $Src, "--pinned", $Trusted, "--min-sequence", "$MinSeq")
if ($Ref -match '^v[0-9]') { $pvArgs += @("--expect-version", $Ref) }
$pvOut = & $Py[0] @pvArgs
$pvCode = $LASTEXITCODE
$pvOut | Where-Object { $_ -notmatch '^SEQUENCE=' } | ForEach-Object { Write-Host "    $_" }
if ($pvCode -ne 0) { Fail "This download did not verify, so none of it was run. Nothing was added to your PATH. Please report this to security@vektraindustries.com." }
$Seq = (($pvOut | Where-Object { $_ -match '^SEQUENCE=' }) -replace '^SEQUENCE=', '')

# 4. Private Python environment
$Venv = Join-Path $VLHome "venv"
$VPy  = Join-Path $Venv "Scripts\python.exe"
if (-not (Test-Path $VPy)) {
    Say "Making a private Python environment"
    $pyArgs = @($Py | Select-Object -Skip 1) + @("-m", "venv", $Venv)
    & $Py[0] @pyArgs
}
Say "Installing packages (each one checked against its hash in requirements.txt)"
& $VPy -m pip install --quiet --disable-pip-version-check --require-hashes -r (Join-Path $Src "requirements.txt")
if ($LASTEXITCODE -ne 0) { Fail "A package did not match its hash, or could not be downloaded. Nothing was added to your PATH." }

# 5. Verify the Laws with the Core
Say "Checking the Laws with the Core"
$env:PYTHONPATH = Join-Path $Src "core"
$env:VEKTRA_LAWS_TRUSTED_KEYS = $Trusted
$vArgs = @("-m", "vektra_laws_core", "verify")
foreach ($f in ($Trusted -split ",")) { if ($f.Trim()) { $vArgs += @("--expect-key", $f.Trim()) } }
& $VPy @vArgs
if ($LASTEXITCODE -ne 0) { Fail "The Laws did not verify. Nothing was added to your PATH. Please report this to security@vektraindustries.com." }
Set-Content -Encoding ASCII -Path $State -Value ('{"min_sequence": ' + [int]$Seq + '}')

# 6. The command
$Bin = Join-Path $VLHome "bin"
New-Item -ItemType Directory -Force -Path $Bin | Out-Null
$Launcher = Join-Path $Bin "vektra-laws.cmd"
@"
@echo off
rem vektra-laws launcher, written by the Vektra Laws installer (VEKTRA_LAWS_HOME).
set "VEKTRA_LAWS_HOME=$VLHome"
set "VEKTRA_LAWS_BIN=$Bin"
set "VEKTRA_LAWS_TRUSTED_KEYS=$Trusted"
set "PYTHONPATH=$Src\core;%PYTHONPATH%"
"$VPy" -m vektra_laws_core %*
"@ | Set-Content -Encoding ASCII $Launcher
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not ($userPath -split ";" | Where-Object { $_ -eq $Bin })) {
    [Environment]::SetEnvironmentVariable("Path", "$Bin;$userPath", "User")
}
$env:Path = "$Bin;$env:Path"
Say "Installed the vektra-laws command at $Launcher"

# 7. Setup wizard
if (-not $env:VEKTRA_LAWS_NO_SETUP -and [Environment]::UserInteractive) {
    Write-Host ""
    & $Launcher setup
} else {
    Write-Host "`nRun 'vektra-laws setup' in your project folder to set it up."
}
Write-Host "`nDone. Open a new terminal, then try: vektra-laws doctor"
}

# Runs only once the whole script has arrived, so a cut-off download runs nothing.
Install-VektraLaws
