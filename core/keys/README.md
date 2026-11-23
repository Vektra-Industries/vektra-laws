# Steward signing keys

Two Ed25519 keys protect the Laws. Both private halves are made and kept offline by the steward.
They never go into this repository, a CI secret, a chat, or any machine an AI agent can reach.

| File | Key | Used for |
| --- | --- | --- |
| `steward-ed25519.pub` | Main key | Signs `core/LAWS.lock` for each version |
| `recovery-ed25519.pub` | Recovery key | Kept apart and almost never used. Signs a release that replaces a lost or stolen main key |

Each key has a **fingerprint**: the SHA-256 of its raw 32-byte public key. The fingerprints are
pinned in `install/install.sh` and `install/install.ps1` (`PINNED_KEYS`), listed in VERIFYING.md,
and published on vektraindustries.com. The engine accepts a signature only from a pinned key, so a
download that swaps the Laws, the lock and the key together still fails.

## Make the keys and sign (steward)

Before you sign, the maintainer runs `python tools/lock_laws.py --release`, which hashes every file
again, raises the sequence number by one and prints the `digest` to sign. Sign only a digest from a
commit you have looked at.

Use your own computer with Wi-Fi off. You need OpenSSL 3 (`openssl version` should say 3.x; on macOS
install it with `brew install openssl` and use that one, since the built-in LibreSSL may not sign
Ed25519).

```bash
# 1. Make both key pairs (first time only)
openssl genpkey -algorithm ed25519 -out steward-ed25519.pem
openssl pkey -in steward-ed25519.pem -pubout -out steward-ed25519.pub
openssl genpkey -algorithm ed25519 -out recovery-ed25519.pem
openssl pkey -in recovery-ed25519.pem -pubout -out recovery-ed25519.pub

# 2. Sign the lock digest (the "digest" value in core/LAWS.lock, which the maintainer sends you)
#    with the MAIN key. The digest covers the Laws, every Core file, the version and the sequence.
H="PASTE_DIGEST_HERE"
printf "$(printf '%s' "$H" | sed 's/../\\x&/g')" > lock.bin     # 32 bytes
openssl pkeyutl -sign -rawin -inkey steward-ed25519.pem -in lock.bin | base64 | tr -d '\n'; echo

# 3. Show the two fingerprints (write them down on paper too)
for k in steward recovery; do
  printf '%s  ' "$k"; openssl pkey -pubin -in "$k-ed25519.pub" -outform DER | tail -c 32 | sha256sum
done
```

On macOS, use `shasum -a 256` in place of `sha256sum`.

4. Store the private keys:
   - `steward-ed25519.pem`: two USB drives in two places.
   - `recovery-ed25519.pem`: a third place, apart from both (for example a USB drive with someone
     you trust, or a safe). Never on the same drive as the main key.
   Then delete both `.pem` files from the computer.
5. Send the maintainer both `.pub` files, the signature line and both fingerprints. All are public.
6. The maintainer runs:

   ```bash
   python tools/add_signature.py --pub steward-ed25519.pub --sig "..." --fingerprint MAIN_FPR \
       --recovery-pub recovery-ed25519.pub --recovery-fingerprint RECOVERY_FPR
   ```

   It checks that each key matches the fingerprint you saw on the offline machine and that the
   signature is valid, then prints the `PINNED_KEYS` line for the installers.

Or, with this repo and Python on the offline machine: `python tools/lock_laws.py --sign steward-ed25519.pem`.

## If the main key is lost or stolen

1. **Lost** (no one else has it): make a new main key, sign the current lock with it, and publish a
   release whose installers pin the new main key and the same recovery key.
2. **Stolen**: do the same, sign that release's lock with the **recovery key** (so installs that pin
   the old pair still accept it), remove the stolen key from `PINNED_KEYS`, and post a notice on
   vektraindustries.com, in SECURITY.md and in CHANGELOG.md saying which versions the stolen key
   signed and the date it stopped being trusted. Then make a new recovery key.
3. If both keys are gone, publish new keys and fingerprints with a public notice. Users must
   re-check the fingerprints by hand.
