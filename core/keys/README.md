# Steward signing key

`steward-ed25519.pub` is the public half of the key that signs `core/LAWS.lock`. The private half is
made and kept offline by the steward. It never goes into this repository, a CI secret, a chat, or
any machine an AI agent can reach.

## Make the key and sign (steward, once per Laws version)

Use your own computer with Wi-Fi off. You only need OpenSSL 3 (`openssl version` should say 3.x; on macOS install it with
`brew install openssl` and use that one, since the built-in LibreSSL may not sign Ed25519).

```bash
# 1. Make the key pair (first time only)
openssl genpkey -algorithm ed25519 -out steward-ed25519.pem
openssl pkey -in steward-ed25519.pem -pubout -out steward-ed25519.pub

# 2. Sign the lock fingerprint (the sha256 value in core/LAWS.lock)
H="PASTE_SHA256_HERE"
printf "$(printf '%s' "$H" | sed 's/../\\x&/g')" > lock.bin     # 32 bytes
openssl pkeyutl -sign -rawin -inkey steward-ed25519.pem -in lock.bin | base64 | tr -d '\n'; echo
```

3. Copy `steward-ed25519.pem` to two USB drives kept in different places, then delete it from the
   computer. Losing it means a new key; leaking it means a new key and a public notice.
4. Send the maintainer `steward-ed25519.pub` and the signature line. Both are public.
5. The maintainer runs `python tools/add_signature.py --pub steward-ed25519.pub --sig "..."`,
   which checks the signature before saving it.

Or, with this repo and Python on the offline machine: `python tools/lock_laws.py --sign steward-ed25519.pem`.

## If the key is lost or stolen

Make a new key pair, sign the current lock, publish the new public key, and state in CHANGELOG.md
which versions the old key signed and the date it stopped being trusted.
