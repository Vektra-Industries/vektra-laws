"""Add the steward's signature to core/LAWS.lock, after checking it.

The steward signs offline with openssl and sends only public things: the public key file(s), the
signature and the fingerprints shown on the offline machine. None of them is secret.

    python tools/add_signature.py --pub steward-ed25519.pub --sig "BASE64SIGNATURE" \
        --fingerprint MAIN_FPR [--recovery-pub recovery-ed25519.pub --recovery-fingerprint REC_FPR]

Each fingerprint is checked against the key file it belongs to, so a key changed on the way here is
caught. The fingerprints printed at the end go into PINNED_KEYS in install/install.sh and
install/install.ps1, VERIFYING.md and vektraindustries.com.
"""
import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
from cryptography.hazmat.primitives.serialization import load_pem_public_key  # noqa: E402
from vektra_laws_core.integrity import RECOVERY_NAME, key_fingerprint, lock_digest  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--pub", type=Path, required=True)
ap.add_argument("--sig", required=True)
ap.add_argument("--fingerprint", help="the main key fingerprint as shown on the offline machine")
ap.add_argument("--recovery-pub", type=Path)
ap.add_argument("--recovery-fingerprint")
a = ap.parse_args()


def check_fpr(path: Path, expected: str | None, label: str) -> str:
    got = key_fingerprint(path.read_bytes())
    if expected and expected.strip().lower() != got:
        sys.exit(f"STOP: the {label} key file does not match the fingerprint you were given.\n"
                 f"  file:  {got}\n  given: {expected.strip().lower()}")
    return got


keydir = ROOT / "core" / "keys"
lock_path = ROOT / "core" / "LAWS.lock"
lock = json.loads(lock_path.read_text())
main_fpr = check_fpr(a.pub, a.fingerprint, "main")
rec_fpr = check_fpr(a.recovery_pub, a.recovery_fingerprint, "recovery") if a.recovery_pub else None
if rec_fpr and rec_fpr == main_fpr:
    sys.exit("STOP: the recovery key is the same as the main key. Make a separate key.")

sig = a.sig.strip()
digest = lock_digest(lock)
if lock.get("digest") != digest:
    sys.exit("STOP: LAWS.lock does not hash to its digest. Run tools/lock_laws.py --release first.")
load_pem_public_key(a.pub.read_bytes()).verify(base64.b64decode(sig), bytes.fromhex(digest))
lock["signature"] = sig
lock_path.write_text(json.dumps(lock, indent=2) + "\n")
for src, name in ((a.pub, "steward-ed25519.pub"), (a.recovery_pub, RECOVERY_NAME)):
    if src and src.resolve() != (keydir / name).resolve():
        (keydir / name).write_bytes(src.read_bytes())

print(f"Signature valid. LAWS.lock {lock['version']} (sequence {lock['sequence']}) is signed by the main key.")
print(f"Main key fingerprint:     {main_fpr}")
if rec_fpr:
    print(f"Recovery key fingerprint: {rec_fpr}")
print(f'\nPINNED_KEYS="{main_fpr}{"," + rec_fpr if rec_fpr else ""}"')
