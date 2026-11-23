"""Pin the Laws and the Core code in core/LAWS.lock, and optionally sign the pin.

    python tools/lock_laws.py                      # update the hashes after an approved change
    python tools/lock_laws.py --release            # before a release: re-hash and raise the sequence
    python tools/lock_laws.py --sign KEY.pem       # steward only: sign with the offline private key

The steward signs the `digest` line. Every release must have a higher sequence than the last, so
an installed copy refuses an older signed release.

Changing the Laws is deliberate: validate.py fails until the lock is updated, and the engine refuses
to run on Laws that do not match the lock.
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))
from vektra_laws_core.integrity import sign_lock, write_lock  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--sign", type=Path, help="PEM file of the steward's Ed25519 private key")
ap.add_argument("--release", action="store_true", help="raise the sequence by one for a new release")
a = ap.parse_args()
lock_path = ROOT / "core" / "LAWS.lock"
seq = None
if a.release and lock_path.exists():
    seq = int(json.loads(lock_path.read_text()).get("sequence", 0)) + 1
lock = write_lock(yaml.safe_load((ROOT / "laws.yaml").read_text()), sequence=seq)
if a.sign:
    lock = sign_lock(a.sign.read_bytes())
print(f"LAWS.lock: {lock['version']} sequence {lock['sequence']} signed={bool(lock['signature'])}")
print(f"digest to sign: {lock['digest']}")
