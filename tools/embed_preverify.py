"""Copy install/preverify.py into install/install.sh and install/install.ps1.

The installers carry the checker inside them, so it comes from the installer you fetched and not
from the download it checks. validate.py fails when a copy is out of date.

    python tools/embed_preverify.py          # write the copies
    python tools/embed_preverify.py --check  # exit 1 if a copy is out of date
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "install" / "preverify.py"
BEGIN = "# BEGIN PREVERIFY: generated from install/preverify.py by tools/embed_preverify.py. Do not edit here.\n"
END = "# END PREVERIFY\n"


def block(target: str, code: str) -> str:
    if target.endswith(".sh"):
        assert "PYEOF" not in code
        # read, not $(cat <<...): bash 3.2 (macOS) misparses quotes in a heredoc inside $( ).
        return f"PREVERIFY=''\nIFS= read -r -d '' PREVERIFY <<'PYEOF' || true\n{code}PYEOF\n"
    assert not re.search(r"^'@", code, re.M)
    return f"$PreVerify = @'\n{code}'@\n"


def render(path: Path, code: str) -> str:
    text = path.read_text()
    i, j = text.index(BEGIN) + len(BEGIN), text.index(END)
    return text[:i] + block(path.name, code) + text[j:]


def outputs() -> dict[Path, str]:
    code = SRC.read_text()
    return {p: render(p, code) for p in (ROOT / "install" / "install.sh", ROOT / "install" / "install.ps1")}


if __name__ == "__main__":
    stale = [p for p, t in outputs().items() if p.read_text() != t]
    if "--check" in sys.argv:
        for p in stale:
            print(f"{p.relative_to(ROOT)}: preverify copy is out of date (run tools/embed_preverify.py)")
        sys.exit(1 if stale else 0)
    for p, t in outputs().items():
        p.write_text(t)
    print("Embedded install/preverify.py into install.sh and install.ps1.")
