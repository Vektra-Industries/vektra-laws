# Steward signing key

`steward-ed25519.pub` (to be added) is the public half of the key that signs `core/LAWS.lock`. The
private half is created and kept offline by the steward. It never goes into this repository, a CI
secret, or any machine an AI agent can reach.

Create it once, on an offline machine:

```bash
openssl genpkey -algorithm ed25519 -out steward-ed25519.pem
openssl pkey -in steward-ed25519.pem -pubout -out steward-ed25519.pub
python tools/lock_laws.py --sign steward-ed25519.pem
```

Commit only `steward-ed25519.pub` and the signed `LAWS.lock`.
