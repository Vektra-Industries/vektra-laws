# Installing Vektra Laws

*This document is informative.* It covers Vektra Laws Core, the reference engine in `core/`, and
the `vektra-laws` command. The Laws themselves are the text in [LAWS.md](LAWS.md) and
[laws.yaml](laws.yaml); installing the software is one way to apply them, not a requirement.

## One command

```bash
# Linux, macOS, WSL2
curl -fsSL https://vektraindustries.com/laws/install.sh | bash
```

```powershell
# Windows (PowerShell 5.1 or 7)
iex (irm https://vektraindustries.com/laws/install.ps1)
```

### Read it first (recommended)

```bash
curl -fsSL https://vektraindustries.com/laws/install.sh -o install.sh
less install.sh
bash install.sh
```

The scripts live in this repository under [install/](install/). The web addresses above point to
those same files, so what you read here is what runs.

## What the installer does

1. Checks for Python 3.10 or newer (with `venv`) and git. It tells you the command to install
   either one if it is missing. It never uses sudo.
2. Downloads Vektra Laws into `~/.vektra-laws/src` (Windows: `%LOCALAPPDATA%\vektra-laws\src`).
   It uses the newest release tag, or `main` when no release exists yet.
3. Makes a private Python environment in `~/.vektra-laws/venv` and installs the two dependencies
   from [requirements.txt](requirements.txt) into it.
4. Checks that the locked parts of the Laws match [core/LAWS.lock](core/LAWS.lock), and that the
   steward signature is valid when one is present. **If the check fails, it stops**, and the command
   is not added to your PATH.
5. Adds the `vektra-laws` command to `~/.local/bin` (Windows: `%LOCALAPPDATA%\vektra-laws\bin`).
6. Starts `vektra-laws setup` when you are at a terminal.

Options for `install.sh`: `--ref <tag|branch>`, `--dir <path>`, `--no-setup`,
`--require-signature` (stop unless the Laws are signed by the steward key). The same settings can
be given as `VEKTRA_LAWS_REF`, `VEKTRA_LAWS_HOME` and `VEKTRA_LAWS_BIN`.

## The setup wizard

Run `vektra-laws setup` in your project folder. It asks five things:

1. The project folder.
2. What you are building: an AI agent, a model app or chatbot, a robot, or several.
3. Who the system answers to (2.18).
4. Responders or others they name (optional).
5. Your tools and their action levels, from a starter list you can keep or replace.

It writes `vektra-laws/creator-policy.yaml`, `vektra-laws/consumer.yaml` and
`vektra-laws/QUICKSTART.md`, makes an approval channel key under `~/.vektra-laws/keys/` that only
your user can read, and runs a self-check. Every question has a flag (`--kind`, `--assigned`,
`--named`, `--tools`, `--yes`) for scripts and CI.

The wizard writes creator policy only. Policy can add tools and make rules stricter; it cannot
loosen a Law or a bright line. See [docs/SECURITY-MODEL.md](docs/SECURITY-MODEL.md).

## Commands

| Command | What it does |
| --- | --- |
| `vektra-laws setup` | Add the guard to a project |
| `vektra-laws verify` | Check the Laws against LAWS.lock and the steward signature |
| `vektra-laws doctor` | Check the install and the project, with the fix for anything wrong |
| `vektra-laws check NAME --level N [--effect E]` | Ask the guard about one action. Exit code 0 allow, 3 ask a person, 4 deny |
| `vektra-laws guard --policy ...` | Run the guard as its own process (JSON lines on stdin and stdout) |
| `vektra-laws test` | Run the Core unit tests |
| `vektra-laws update [--ref TAG]` | Move to the newest release; rolls back if it does not verify |
| `vektra-laws uninstall` | Remove `~/.vektra-laws` and the command. Your project files stay |

## Without the installer

```bash
git clone https://github.com/Vektra-Industries/vektra-laws.git
cd vektra-laws
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=core python -m vektra_laws_core verify
PYTHONPATH=core python -m vektra_laws_core setup
```

## Checking the Laws yourself

[VERIFYING.md](VERIFYING.md) shows how to check the lock and the signature by hand, without
trusting the installer or this code.
