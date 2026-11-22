"""Add the steward's signature to core/LAWS.lock, after checking it.

The steward signs offline with openssl and sends only two public things: the public key file and
the signature. Neither is secret.

    python tools/add_signature.py --pub steward-ed25519.pub --sig "BASE64SIGNATURE"
"""
import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
from cryptography.hazmat.primitives.serialization import load_pem_public_key  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--pub", type=Path, required=True)
ap.add_argument("--sig", required=True)
a = ap.parse_args()

lock_path = ROOT / "core" / "LAWS.lock"
lock = json.loads(lock_path.read_text())
key = load_pem_public_key(a.pub.read_bytes())
sig = a.sig.strip()
key.verify(base64.b64decode(sig), bytes.fromhex(lock["sha256"]))   # raises if it does not match
lock["signature"] = sig
lock_path.write_text(json.dumps(lock, indent=2) + "\n")
dest = ROOT / "core" / "keys" / "steward-ed25519.pub"
if a.pub.resolve() != dest.resolve():
    dest.write_bytes(a.pub.read_bytes())
print(f"Signature valid. LAWS.lock {lock['version']} is signed; public key saved to {dest.relative_to(ROOT)}.")
