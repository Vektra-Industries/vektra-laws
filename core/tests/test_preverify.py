"""Tests for install/preverify.py, the dependency-free checker the installers run before any
downloaded code, and for the v2 lock it reads (code hashes, sequence, signature over the digest)."""
import base64
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

CORE = Path(__file__).resolve().parents[1]
ROOT = CORE.parent
sys.path.insert(0, str(CORE))
sys.path.insert(0, str(ROOT / "install"))
import preverify  # noqa: E402
from vektra_laws_core import integrity  # noqa: E402

try:
    from cryptography.hazmat.primitives import serialization as ser
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except ImportError:  # pragma: no cover
    Ed25519PrivateKey = None

LAWS = yaml.safe_load((ROOT / "laws.yaml").read_text())


def pem(k):
    return k.public_key().public_bytes(ser.Encoding.PEM, ser.PublicFormat.SubjectPublicKeyInfo)


def priv(k):
    return k.private_bytes(ser.Encoding.PEM, ser.PrivateFormat.PKCS8, ser.NoEncryption())


@unittest.skipIf(Ed25519PrivateKey is None, "cryptography not installed")
class PreVerify(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.src = Path(self.tmp.name, "src")
        for rel in ("laws.yaml", "requirements.txt"):
            (self.src / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, self.src / rel)
        shutil.copytree(ROOT / integrity.CODE_DIR, self.src / integrity.CODE_DIR,
                        ignore=shutil.ignore_patterns("__pycache__"))
        (self.src / "core" / "keys").mkdir(parents=True)
        self.lock = self.src / "core" / "LAWS.lock"
        self.main, self.recovery, self.attacker = (Ed25519PrivateKey.generate() for _ in range(3))
        self.pinned = {preverify.fingerprint(pem(self.main)), preverify.fingerprint(pem(self.recovery))}

    def tearDown(self):
        self.tmp.cleanup()

    def release(self, key, sequence=1):
        integrity.write_lock(LAWS, self.lock, root=self.src, sequence=sequence)
        integrity.sign_lock(priv(key), self.lock)
        (self.src / "core/keys/steward-ed25519.pub").write_bytes(pem(self.main))
        (self.src / "core/keys/recovery-ed25519.pub").write_bytes(pem(self.recovery))

    def check(self, **kw):
        return preverify.check(self.src, kw.pop("pinned", self.pinned), **kw)

    def test_matches_cryptography(self):
        k = Ed25519PrivateKey.generate()
        raw = preverify.raw_public_key(pem(k))
        self.assertEqual(preverify.fingerprint(pem(k)), integrity.key_fingerprint(pem(k)))
        sig = k.sign(b"x" * 32)
        self.assertTrue(preverify.ed25519_verify(raw, b"x" * 32, sig))
        self.assertFalse(preverify.ed25519_verify(raw, b"y" * 32, sig))
        bad = bytearray(sig)
        bad[5] ^= 1
        self.assertFalse(preverify.ed25519_verify(raw, b"x" * 32, bytes(bad)))

    def test_same_hashes_as_core(self):
        self.release(self.main)
        lock = json.loads(self.lock.read_text())
        self.assertEqual(preverify.lock_digest(lock), integrity.lock_digest(lock))
        p = self.src / "laws.yaml"
        self.assertEqual(preverify.file_digest(p), integrity.file_digest(p))

    def test_signed_release_passes_and_crlf_is_fine(self):
        self.release(self.main, sequence=3)
        p = self.src / integrity.CODE_DIR / "engine.py"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))       # a Windows checkout
        st = self.check(min_sequence=3, expect_version="v0.6.0")
        self.assertTrue(st["signed"])
        self.assertEqual(st["sequence"], 3)

    def test_recovery_key_signature_passes(self):
        self.release(self.recovery)
        self.assertEqual(self.check()["key"], preverify.fingerprint(pem(self.recovery)))

    def test_edited_checker_code_is_refused(self):
        self.release(self.main)
        p = self.src / integrity.CODE_DIR / "integrity.py"
        p.write_text(p.read_text() + "\n# skip every check\n")
        with self.assertRaisesRegex(preverify.Stop, "integrity.py"):
            self.check()

    def test_added_code_is_refused(self):
        self.release(self.main)
        (self.src / integrity.CODE_DIR / "plugs" / "evil.py").write_text("print('hi')\n")
        with self.assertRaisesRegex(preverify.Stop, "not listed"):
            self.check()

    def test_changed_requirements_are_refused(self):
        self.release(self.main)
        (self.src / "requirements.txt").write_text("evil==1.0\n")
        with self.assertRaises(preverify.Stop):
            self.check()

    def test_attacker_key_and_signature_are_refused(self):
        self.release(self.attacker)
        (self.src / "core/keys/steward-ed25519.pub").write_bytes(pem(self.attacker))
        with self.assertRaisesRegex(preverify.Stop, "pinned steward key"):
            self.check()

    def test_edited_lock_is_refused(self):
        self.release(self.main)
        lock = json.loads(self.lock.read_text())
        lock["sequence"] = 99
        self.lock.write_text(json.dumps(lock))
        with self.assertRaisesRegex(preverify.Stop, "its own digest"):
            self.check()
        lock["digest"] = preverify.lock_digest(lock)                # re-hashed, but now unsigned
        self.lock.write_text(json.dumps(lock))
        with self.assertRaisesRegex(preverify.Stop, "signature"):
            self.check()

    def test_rollback_is_refused(self):
        self.release(self.main, sequence=2)
        with self.assertRaisesRegex(preverify.Stop, "Rolling back"):
            self.check(min_sequence=5)

    def test_tag_must_match_version(self):
        self.release(self.main)
        with self.assertRaisesRegex(preverify.Stop, "must match"):
            self.check(expect_version="v9.9.9")

    def test_unsigned_without_pins_is_prerelease(self):
        integrity.write_lock(LAWS, self.lock, root=self.src)
        self.assertFalse(self.check(pinned=set())["signed"])
        with self.assertRaises(preverify.Stop):
            self.check(pinned=set(), require_signature=True)

    def test_core_refuses_rollback_and_edits(self):
        self.release(self.main, sequence=2)
        pub = self.src / "core/keys/steward-ed25519.pub"
        self.assertTrue(integrity.verify(LAWS, self.lock, pub, trusted=self.pinned, root=self.src)["signed"])
        os.environ[integrity.MIN_SEQ_ENV] = "3"
        try:
            with self.assertRaises(integrity.IntegrityError):
                integrity.verify(LAWS, self.lock, pub, trusted=self.pinned, root=self.src)
        finally:
            del os.environ[integrity.MIN_SEQ_ENV]
        p = self.src / integrity.CODE_DIR / "policy.py"
        p.write_text(p.read_text() + "\n")
        with self.assertRaises(integrity.IntegrityError):
            integrity.verify(LAWS, self.lock, pub, trusted=self.pinned, root=self.src)

    def test_signature_is_over_the_digest(self):
        self.release(self.main)
        lock = json.loads(self.lock.read_text())
        raw = preverify.raw_public_key(pem(self.main))
        self.assertTrue(preverify.ed25519_verify(raw, bytes.fromhex(lock["digest"]),
                                                 base64.b64decode(lock["signature"])))


if __name__ == "__main__":
    unittest.main()
