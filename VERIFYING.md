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

The same values are published in three places outside the download: the installers' `PINNED_KEYS`,
vektraindustries.com/laws/keys, and a pinned post on the steward's profiles. If any two places
disagree, do not use the copy, and email security@vektraindustries.com.

```bash
vektra-laws fingerprint                       # what this copy carries
# or with OpenSSL only:
openssl pkey -pubin -in core/keys/steward-ed25519.pub -outform DER | tail -c 32 | sha256sum
```

To make your own system refuse anything not signed by these keys, set
`VEKTRA_LAWS_TRUSTED_KEYS=MAIN_FPR,RECOVERY_FPR` (the installer does this for you). The engine then
requires a signature by a pinned key every time it starts, with no internet needed.

## What is signed

`core/LAWS.lock` holds:

- a SHA-256 fingerprint of the parts of the Laws that cannot change (the mission, every clause, the
  bright lines and the precedence; examples and intent notes are not included);
- the SHA-256 of `laws.yaml`, `requirements.txt` and **every file of Core code**, including the code
  that does the checking;
- the version and a **sequence number** that goes up with every release.

The steward signs the `digest`: one hash of all of that. So an edited checker, an added file or a
changed package list breaks the signature, and an older signed release cannot be swapped back in.

## What the installer does, before running anything

The installer carries its own checker (`install/preverify.py`, standard library only, run with
`python -I`). It checks the download **before any downloaded code runs**: every file against the
lock, no extra code, a signature by a pinned key, a sequence not older than the one installed, and
a release tag that matches the version. Only then does it install the packages, each one checked
against its hash in `requirements.txt` (`pip --require-hashes`). It installs releases only, never
unreleased code, unless you ask for `--ref main`.

## What the engine does

1. Fingerprints the Laws it is about to use.
2. Refuses to start if they do not match `LAWS.lock`.
3. If the lock is signed, checks every Core file against it, and checks the signature with the
   public key. A host can make the signature required.
4. When fingerprints are pinned, accepts a signature only from a pinned key.
5. Refuses Laws with a lower sequence than the release already installed (`~/.vektra-laws/state.json`).

## Check a signature by hand

With OpenSSL 3 and the lock's `digest`:

```bash
D=$(python3 -c "import json; print(json.load(open('core/LAWS.lock'))['digest'])")
printf "$(printf '%s' "$D" | sed 's/../\\x&/g')" > digest.bin
python3 -c "import json,base64,sys; sys.stdout.buffer.write(base64.b64decode(json.load(open('core/LAWS.lock'))['signature']))" > lock.sig
openssl pkeyutl -verify -pubin -inkey core/keys/steward-ed25519.pub -rawin -in digest.bin -sigfile lock.sig
```

Or with no OpenSSL at all: `python3 -I install/preverify.py --src . --pinned MAIN_FPR,RECOVERY_FPR`.

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
