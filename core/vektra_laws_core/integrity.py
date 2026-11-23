"""Integrity: the locked parts of laws.yaml are pinned by hash and, optionally, signed.

The engine refuses to start when the locked parts change (a bright line, a clause, the precedence
rules or the action levels). A creator can still fork and edit the code; what they cannot do is edit
the Laws and keep a matching hash, signature or conformance claim. See docs/SECURITY-MODEL.md.

Signing uses Ed25519 through the optional `cryptography` package. The steward keeps the private key
offline; only the public key ships in core/keys/.
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


def write_lock(data: dict, path: Path = LOCK) -> dict:
    lock = {"format": "vektra-laws-lock/v1", "version": str(data["version"]),
            "sha256": locked_digest(json.loads(json.dumps(data, default=str))), "signature": None}
    path.write_text(json.dumps(lock, indent=2) + "\n")
    return lock


def sign_lock(private_key_pem: bytes, path: Path = LOCK) -> dict:
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    lock = json.loads(path.read_text())
    key = load_pem_private_key(private_key_pem, password=None)
    lock["signature"] = base64.b64encode(key.sign(bytes.fromhex(lock["sha256"]))).decode()
    path.write_text(json.dumps(lock, indent=2) + "\n")
    return lock


def key_fingerprint(pub_pem: bytes) -> str:
    """SHA-256 of the raw 32-byte Ed25519 public key, in hex. The same value as:
    openssl pkey -pubin -in KEY.pub -outform DER | tail -c 32 | sha256sum"""
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
    raw = load_pem_public_key(pub_pem).public_bytes(Encoding.Raw, PublicFormat.Raw)
    return hashlib.sha256(raw).hexdigest()


def pinned_from_env() -> set[str]:
    return {f.strip().lower() for f in os.environ.get(TRUST_ENV, "").split(",") if f.strip()}


def verify(data: dict, lock_path: Path = LOCK, pubkey_path: Path = PUBKEY,
           require_signature: bool = False, trusted: set[str] | None = None) -> dict:
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
    got = locked_digest(json.loads(json.dumps(data, default=str)))
    if got != lock["sha256"] or str(data["version"]) != lock["version"]:
        raise IntegrityError("The locked parts of the Laws do not match LAWS.lock. The engine will not run.")
    status = {"version": lock["version"], "sha256": got, "signed": False, "key": None, "pinned": bool(trusted)}
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
                    base64.b64decode(lock["signature"]), bytes.fromhex(lock["sha256"]))
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
