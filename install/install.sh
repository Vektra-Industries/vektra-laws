#!/usr/bin/env bash
# Vektra Laws installer for Linux, macOS and WSL2.
#
#   curl -fsSL https://vektraindustries.com/laws/install.sh | bash
#
# Want to read it first? (recommended)
#   curl -fsSL https://vektraindustries.com/laws/install.sh -o install.sh
#   less install.sh && bash install.sh
#
# What it does, and nothing more:
#   1. checks for Python 3.10+ and git
#   2. downloads Vektra Laws (newest release tag, or main) into ~/.vektra-laws/src
#   3. makes a private Python environment in ~/.vektra-laws/venv (no sudo, no system packages)
#   4. checks that the Laws match LAWS.lock (and the steward signature when present); stops if not
#   5. adds the `vektra-laws` command to ~/.local/bin
#   6. runs `vektra-laws setup`, the wizard, when you are at a terminal
#
# Options:  --ref <tag|branch>   --dir <path>   --no-setup   --require-signature   --help
# Env:      VEKTRA_LAWS_HOME, VEKTRA_LAWS_REF, VEKTRA_LAWS_BIN, VEKTRA_LAWS_REPO
set -euo pipefail

REPO="${VEKTRA_LAWS_REPO:-https://github.com/Vektra-Industries/vektra-laws.git}"
API="https://api.github.com/repos/Vektra-Industries/vektra-laws/releases/latest"
VL_HOME="${VEKTRA_LAWS_HOME:-$HOME/.vektra-laws}"
BIN_DIR="${VEKTRA_LAWS_BIN:-$HOME/.local/bin}"
REF="${VEKTRA_LAWS_REF:-}"
RUN_SETUP=1
REQUIRE_SIG=0

if [ -t 1 ]; then B=$'\033[1m'; G=$'\033[33m'; R=$'\033[31m'; N=$'\033[0m'; else B=""; G=""; R=""; N=""; fi
say()  { printf '%s\n' "${G}==>${N} ${B}$*${N}"; }
fail() { printf '%s\n' "${R}error:${N} $*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --ref) REF="${2:?--ref needs a value}"; shift 2 ;;
    --dir) VL_HOME="${2:?--dir needs a value}"; shift 2 ;;
    --no-setup) RUN_SETUP=0; shift ;;
    --require-signature) REQUIRE_SIG=1; shift ;;
    -h|--help) sed -n '2,21p' "$0" 2>/dev/null || true; exit 0 ;;
    *) fail "unknown option: $1 (try --help)" ;;
  esac
done

printf '\n%s\n%s\n\n' "${B}Vektra Laws${N}" "A safety core for AI, agents and robots. Humans stay in command."

# 1. Requirements ----------------------------------------------------------------------------------
PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys, venv, ensurepip; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$(command -v "$c")"; break
  fi
done
[ -n "$PY" ] || fail "Python 3.10 or newer, with venv, is needed. Ubuntu/Debian: sudo apt install python3 python3-venv   macOS: brew install python"
command -v git >/dev/null 2>&1 || fail "git is needed. Ubuntu/Debian: sudo apt install git   macOS: xcode-select --install"
say "Python $("$PY" -c 'import platform; print(platform.python_version())') and git found"

# 2. Download --------------------------------------------------------------------------------------
if [ -z "$REF" ] && command -v curl >/dev/null 2>&1; then
  REF="$(curl -fsSL "$API" 2>/dev/null | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n1 || true)"
fi
REF="${REF:-main}"
SRC="$VL_HOME/src"
mkdir -p "$VL_HOME"
chmod 700 "$VL_HOME"
if [ -d "$SRC/.git" ]; then
  say "Updating Vektra Laws in $SRC to $REF"
  git -C "$SRC" fetch --quiet --tags origin
  git -C "$SRC" checkout --quiet --force "$REF" 2>/dev/null || git -C "$SRC" checkout --quiet --force "origin/$REF"
else
  say "Downloading Vektra Laws ($REF) into $SRC"
  rm -rf "$SRC"
  git clone --quiet --depth 1 --branch "$REF" "$REPO" "$SRC" \
    || fail "Download failed. Check your connection, or that release $REF exists."
fi
COMMIT="$(git -C "$SRC" rev-parse --short=12 HEAD)"

# 3. Private Python environment --------------------------------------------------------------------
VENV="$VL_HOME/venv"
if [ ! -x "$VENV/bin/python" ]; then
  say "Making a private Python environment"
  "$PY" -m venv "$VENV"
fi
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --upgrade pip
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check -r "$SRC/requirements.txt"

# 4. Verify the Laws -------------------------------------------------------------------------------
say "Checking the Laws against LAWS.lock"
VFLAG=""; [ "$REQUIRE_SIG" = 1 ] && VFLAG="--require-signature"
# shellcheck disable=SC2086
PYTHONPATH="$SRC/core" "$VENV/bin/python" -m vektra_laws_core verify $VFLAG \
  || fail "The Laws did not verify. Nothing was installed on your PATH. Please report this to security@vektraindustries.com."

# 5. The command -----------------------------------------------------------------------------------
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/vektra-laws"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
# vektra-laws launcher, written by the Vektra Laws installer. Remove with: vektra-laws uninstall
export VEKTRA_LAWS_HOME="$VL_HOME"
export VEKTRA_LAWS_BIN="$BIN_DIR"
export PYTHONPATH="$SRC/core\${PYTHONPATH:+:\$PYTHONPATH}"
exec "$VENV/bin/python" -m vektra_laws_core "\$@"
EOF
chmod 755 "$LAUNCHER"
say "Installed the vektra-laws command at $LAUNCHER (commit $COMMIT)"

case ":$PATH:" in
  *":$BIN_DIR:"*) ON_PATH=1 ;;
  *) ON_PATH=0
     RCS=""
     for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do [ -f "$rc" ] && RCS="$RCS $rc"; done
     [ -n "$RCS" ] || RCS="$HOME/.profile"
     for rc in $RCS; do
       if ! grep -qs "# vektra-laws" "$rc"; then
         # shellcheck disable=SC2016  # $PATH must stay literal in the rc file
         printf '\nexport PATH="%s:$PATH"  # vektra-laws\n' "$BIN_DIR" >> "$rc"
       fi
     done ;;
esac

# 6. Setup wizard ----------------------------------------------------------------------------------
if [ "$RUN_SETUP" = 1 ] && [ -t 1 ] && { : </dev/tty; } 2>/dev/null; then
  printf '\n'
  "$LAUNCHER" setup </dev/tty || true
else
  printf '\nRun %s in your project folder to set it up.\n' "${B}vektra-laws setup${N}"
fi

printf '\n%s\n' "${B}Done.${N} Useful commands:"
printf '  vektra-laws setup     add the guard to a project\n'
printf '  vektra-laws doctor    check everything\n'
printf '  vektra-laws verify    check the Laws are the real, unchanged text\n'
printf '  vektra-laws update    move to the newest release\n'
[ "$ON_PATH" = 1 ] || printf '\nOpen a new terminal (or run: source ~/.bashrc) so the command is found.\n'
