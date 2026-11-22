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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "core" / "LAWS.lock"
PUBKEY = ROOT / "core" / "keys" / "steward-ed25519.pub"

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


def verify(data: dict, lock_path: Path = LOCK, pubkey_path: Path = PUBKEY,
           require_signature: bool = False) -> dict:
    if not lock_path.exists():
        raise IntegrityError("LAWS.lock is missing; the engine will not run on unpinned Laws.")
    lock = json.loads(lock_path.read_text())
    got = locked_digest(json.loads(json.dumps(data, default=str)))
    if got != lock["sha256"] or str(data["version"]) != lock["version"]:
        raise IntegrityError("The locked parts of the Laws do not match LAWS.lock. The engine will not run.")
    status = {"version": lock["version"], "sha256": got, "signed": False}
    if lock.get("signature") and pubkey_path.exists():
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.exceptions import InvalidSignature
        try:
            load_pem_public_key(pubkey_path.read_bytes()).verify(
                base64.b64decode(lock["signature"]), bytes.fromhex(lock["sha256"]))
        except InvalidSignature as e:
            raise IntegrityError("LAWS.lock signature is not valid for the steward key.") from e
        status["signed"] = True
    elif require_signature:
        raise IntegrityError("A signed LAWS.lock is required, and none was found.")
    return status
