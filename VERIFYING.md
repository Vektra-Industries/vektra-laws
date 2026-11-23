# Verifying Vektra Laws

How to check that a copy of Vektra Laws, or a product that says it runs them, is genuine.

## The keys

Vektra Laws has a main signing key and a recovery key. Each has two halves:

- **Private key:** kept offline by the steward. Used only to sign the Laws. Never in this
  repository, in CI, or on any machine an AI agent can reach.
- **Public key** (`core/keys/steward-ed25519.pub`, `core/keys/recovery-ed25519.pub`): ships with
  the code. Anyone can use it to check a signature. No one can use it to make one.

## Fingerprints

A public key in a download could be swapped along with the Laws. So the key **fingerprints** (the
SHA-256 of each raw public key) are published in more than one place, and the installer and engine
check against them:

| Key | Fingerprint |
| --- | --- |
| Main | *published with the first signed release* |
| Recovery | *published with the first signed release* |

The same values are in `PINNED_KEYS` in the installers, on vektraindustries.com and on the
steward's profiles. If any two places disagree, do not use the copy, and email
security@vektraindustries.com.

```bash
vektra-laws fingerprint                       # what this copy carries
# or with OpenSSL only:
openssl pkey -pubin -in core/keys/steward-ed25519.pub -outform DER | tail -c 32 | sha256sum
```

To make your own system refuse anything not signed by these keys, set
`VEKTRA_LAWS_TRUSTED_KEYS=MAIN_FPR,RECOVERY_FPR` (the installer does this for you). The engine then
requires a signature by a pinned key every time it starts, with no internet needed.

## What is signed

`core/LAWS.lock` holds a SHA-256 fingerprint of the parts of the Laws that cannot change: the
mission, every clause, the bright lines and the precedence. Examples and intent notes are not
included. The steward signs that fingerprint.

## What the engine does

1. Fingerprints the Laws it is about to use.
2. Refuses to start if they do not match `LAWS.lock`.
3. If the lock is signed, checks the signature with the public key, and refuses a forged or edited
   lock. A host can make the signature required.
4. When fingerprints are pinned, accepts a signature only from a pinned key.

## Check it yourself

```bash
python tools/validate.py              # "Laws lock in sync"
python -c "import sys; sys.path.insert(0,'core'); \
from vektra_laws_core.integrity import verify; import yaml; \
print(verify(yaml.safe_load(open('laws.yaml')), require_signature=True))"
```

A product that claims conformance must show the lock fingerprint in its declaration (see ADOPT.md).
Compare it with the fingerprint published for that version.

## What this means for you

- **Creators** can tighten the Laws for their product: stricter levels, more approvals, fewer
  tools. They cannot loosen or edit the locked parts and keep the name.
- **Consumers** can tighten their own settings. They cannot switch the Laws off.
- **Anyone** can check that a product runs the genuine Laws.

## What it does not do

The code is open source, so anyone can fork it and remove the check. The key does not stop that; it
makes the change visible. A copy that does not match the signed lock cannot call itself Vektra Laws
or claim conformance (TRADEMARKS.md).

## When the Laws change

Each new version gets a new lock, signed with the main key. If the main key is ever lost or stolen,
the recovery key signs the release that replaces it, so pinned installs keep working, and the
steward says publicly which versions the old key signed. See core/keys/README.md.
