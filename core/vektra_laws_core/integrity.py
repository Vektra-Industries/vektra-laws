"""Integrity: the Laws and the Core code are pinned by hash in LAWS.lock, and signed at each release.

The engine refuses to start when the locked parts change (a bright line, a clause, the precedence
rules or the action levels). A creator can still fork and edit the code; what they cannot do is edit
the Laws and keep a matching hash, signature or conformance claim. See docs/SECURITY-MODEL.md.

Signing uses Ed25519 through the optional `cryptography` package. The steward keeps the private key
offline; only the public key ships in core/keys/.

LAWS.lock (format v2) lists the Laws hash, the SHA-256 of laws.yaml, requirements.txt and every Core
.py file, a version and a sequence number. The steward signs `digest`, the hash of all of that, so a
signature covers the checking code too, and an older signed release cannot be swapped back in
(the sequence must not go down). install/preverify.py runs the same file check, with no
dependencies, before any downloaded code runs.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "core" / "LAWS.lock"
PUBKEY = ROOT / "core" / "keys" / "steward-ed25519.pub"
RECOVERY_NAME = "recovery-ed25519.pub"   # second offline key, kept apart, for rotation (core/keys/README.md)
TRUST_ENV = "VEKTRA_LAWS_TRUSTED_KEYS"   # comma-separated pinned fingerprints, set by the installer

# The parts no one may change at runtime. Wording outside these (intent, examples) is informative.
LOCKED_KEYS = ("version", "precedence", "mission", "core", "understanding_matrix", "action_levels", "decisions")


class IntegrityError(RuntimeError):
    pass


def locked_digest(data: dict) -> str:
    locked = {k: data[k] for k in LOCKED_KEYS}
    for part in [locked["mission"], *locked["core"]]:
        for k in ("intent", "example"):
            part.pop(k, None)
    canon = json.dumps(locked, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return hashlib.sha256(canon.encode()).hexdigest()


LOCK_FORMAT = "vektra-laws-lock/v2"
SIGNED_FIELDS = ("format", "version", "sequence", "sha256", "files")
CODE_DIR = "core/vektra_laws_core"
LOCKED_FILES = ("laws.yaml", "requirements.txt")        # plus every .py file in CODE_DIR
STATE_FILE = "state.json"                               # in VEKTRA_LAWS_HOME: highest sequence installed
MIN_SEQ_ENV = "VEKTRA_LAWS_MIN_SEQUENCE"


def file_digest(path: Path) -> str:
    """SHA-256 with CRLF read as LF, so a Windows checkout hashes the same as Linux."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def code_files(root: Path = ROOT) -> list[str]:
    py = sorted(p.relative_to(root).as_posix() for p in (root / CODE_DIR).rglob("*.py")
                if "__pycache__" not in p.parts)
    return [*LOCKED_FILES, *py]


def lock_digest(lock: dict) -> str:
    """What the steward signs: the hash of the version, sequence, Laws hash and every file hash."""
    body = {k: lock[k] for k in SIGNED_FIELDS}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_lock(data: dict, path: Path = LOCK, root: Path = ROOT, sequence: int | None = None) -> dict:
    old = json.loads(path.read_text()) if path.exists() else {}
    lock = {"format": LOCK_FORMAT, "version": str(data["version"]),
            "sequence": int(sequence if sequence is not None else old.get("sequence", 1)),
            "sha256": locked_digest(json.loads(json.dumps(data, default=str))),
            "files": {rel: file_digest(root / rel) for rel in code_files(root)}}
    lock["digest"] = lock_digest(lock)
    lock["signature"] = None
    path.write_text(json.dumps(lock, indent=2) + "\n")
    return lock


def sign_lock(private_key_pem: bytes, path: Path = LOCK) -> dict:
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    lock = json.loads(path.read_text())
    key = load_pem_private_key(private_key_pem, password=None)
    lock["signature"] = base64.b64encode(key.sign(bytes.fromhex(lock_digest(lock)))).decode()
    path.write_text(json.dumps(lock, indent=2) + "\n")
    return lock


def files_changed(lock: dict, root: Path = ROOT) -> list[str]:
    """Files that differ from the lock, are missing, or are new Core code it does not list."""
    listed = lock.get("files", {})
    bad = [rel for rel, want in listed.items()
           if not (root / rel).is_file() or file_digest(root / rel) != want]
    bad += [rel for rel in code_files(root) if rel not in listed]
    return sorted(set(bad))


def min_sequence() -> int:
    """The highest sequence already installed here: the env var, or VEKTRA_LAWS_HOME/state.json."""
    if os.environ.get(MIN_SEQ_ENV, "").isdigit():
        return int(os.environ[MIN_SEQ_ENV])
    home = os.environ.get("VEKTRA_LAWS_HOME")
    if home and (Path(home) / STATE_FILE).exists():
        try:
            return int(json.loads((Path(home) / STATE_FILE).read_text()).get("min_sequence", 0))
        except (ValueError, OSError):
            return 0
    return 0


def key_fingerprint(pub_pem: bytes) -> str:
    """SHA-256 of the raw 32-byte Ed25519 public key, in hex. The same value as:
    openssl pkey -pubin -in KEY.pub -outform DER | tail -c 32 | sha256sum"""
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
    raw = load_pem_public_key(pub_pem).public_bytes(Encoding.Raw, PublicFormat.Raw)
    return hashlib.sha256(raw).hexdigest()


def pinned_from_env() -> set[str]:
    return {f.strip().lower() for f in os.environ.get(TRUST_ENV, "").split(",") if f.strip()}


def verify(data: dict, lock_path: Path = LOCK, pubkey_path: Path = PUBKEY,
           require_signature: bool = False, trusted: set[str] | None = None, root: Path = ROOT) -> dict:
    """Check the Laws against the lock and, when present, the steward signature.

    trusted: pinned key fingerprints that came from somewhere other than this download (the
    installer, the website, a config the operator controls). When any are pinned, a signature by a
    pinned key is required, so a download that swaps the Laws, the lock and the key together fails.
    Defaults to the fingerprints in VEKTRA_LAWS_TRUSTED_KEYS.
    """
    trusted = {t.lower() for t in trusted} if trusted is not None else pinned_from_env()
    if not lock_path.exists():
        raise IntegrityError("LAWS.lock is missing; the engine will not run on unpinned Laws.")
    lock = json.loads(lock_path.read_text())
    if lock.get("format") != LOCK_FORMAT:
        raise IntegrityError(f"LAWS.lock is format {lock.get('format')!r}; this Core needs {LOCK_FORMAT}.")
    got = locked_digest(json.loads(json.dumps(data, default=str)))
    if got != lock["sha256"] or str(data["version"]) != lock["version"]:
        raise IntegrityError("The locked parts of the Laws do not match LAWS.lock. The engine will not run.")
    digest = lock_digest(lock)
    if lock.get("digest") != digest:
        raise IntegrityError("LAWS.lock does not hash to its own digest; it was edited.")
    floor = min_sequence()
    if int(lock["sequence"]) < floor:
        raise IntegrityError(f"These Laws (sequence {lock['sequence']}) are older than the release already "
                             f"installed (sequence {floor}). Rolling back is refused.")
    # A signed (released) lock also pins every Core file. Between releases the code may move on.
    if lock.get("signature") or trusted or require_signature:
        changed = files_changed(lock, root)
        if changed:
            raise IntegrityError("These files do not match LAWS.lock: " + ", ".join(changed[:5])
                                 + (" ..." if len(changed) > 5 else "") + ". The engine will not run.")
    status = {"version": lock["version"], "sha256": got, "digest": digest, "sequence": int(lock["sequence"]),
              "signed": False, "key": None, "pinned": bool(trusted)}
    keys = [p for p in (pubkey_path, pubkey_path.with_name(RECOVERY_NAME)) if p.exists()]
    if lock.get("signature") and keys:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        unpinned = 0
        for kp in keys:
            fpr = key_fingerprint(kp.read_bytes())
            if trusted and fpr not in trusted:
                unpinned += 1
                continue
            try:
                load_pem_public_key(kp.read_bytes()).verify(
                    base64.b64decode(lock["signature"]), bytes.fromhex(digest))
            except InvalidSignature:
                continue
            status.update(signed=True, key=fpr)
            return status
        if unpinned == len(keys):
            raise IntegrityError("The public key in this download is not a pinned steward key. "
                                 "Do not use this copy; check the fingerprint in VERIFYING.md.")
        raise IntegrityError("LAWS.lock signature is not valid for the steward key.")
    if require_signature or trusted:
        raise IntegrityError("A signed LAWS.lock is required, and none was found.")
    return status
