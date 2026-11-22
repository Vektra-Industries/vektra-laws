"""Pin the locked parts of laws.yaml in core/LAWS.lock, and optionally sign the pin.

    python tools/lock_laws.py                      # update the hash after an approved change
    python tools/lock_laws.py --sign KEY.pem       # steward only: sign with the offline private key

Changing the Laws is deliberate: validate.py fails until the lock is updated, and the engine refuses
to run on Laws that do not match the lock.
"""
import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))
from vektra_laws_core.integrity import sign_lock, write_lock  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--sign", type=Path, help="PEM file of the steward's Ed25519 private key")
a = ap.parse_args()
lock = write_lock(yaml.safe_load((ROOT / "laws.yaml").read_text()))
if a.sign:
    lock = sign_lock(a.sign.read_bytes())
print(f"LAWS.lock: {lock['version']} {lock['sha256']} signed={bool(lock['signature'])}")
