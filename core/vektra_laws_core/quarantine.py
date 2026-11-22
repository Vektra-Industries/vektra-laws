"""Content quarantine and the hardline list.

Text that comes from a document, web page, email, tool output or another system is wrapped as
Content. Content is information (4.4): it can never become a command, whatever it says. A heuristic
scanner flags text that tries to give orders, so a person can see it; the flag is a signal only,
because the real rule is structural: Content never reaches the command path.

The hardline list denies the worst shell actions under every setting, the way Hermes Agent's
hardline blocklist does. It is a heuristic over an attacker-influenced string, not containment:
the real boundary is the operating system (docs/SECURITY-MODEL.md).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

INJECTION = re.compile(
    r"(ignore|disregard|forget)\s+(all\s+|any\s+)?(previous|prior|above|earlier)\s+(instructions|rules)"
    r"|you\s+are\s+now\b|new\s+instructions\s*:|system\s+prompt|developer\s+mode"
    r"|disable\s+(the\s+)?(laws|guard|safety)|override\s+(the\s+)?(laws|bright\s+lines?)"
    r"|act\s+as\s+(an?\s+)?unrestricted", re.I)

HARDLINE = [
    (r"\brm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)[a-z]*\s+(/|~|\$HOME)(\s|$)", "recursive delete of root or home"),
    (r"\brm\s+(?=[^;|&]*(-[a-z]*r|--recursive))(?=[^;|&]*(-[a-z]*f|--force))[^;|&]*\s(/|~|\$HOME)(\s|$)",
     "recursive delete of root or home"),
    (r"\bfind\s+(/|~|\$HOME)\s[^;|&]*-delete", "delete everything under root or home"),
    (r"\bmkfs(\.\w+)?\b", "format a filesystem"),
    (r"\bdd\b[^|;]*\bof=/dev/(sd|nvme|hd|disk)", "write to a raw disk"),
    (r":\(\)\s*\{\s*:\|:&\s*\};:", "fork bomb"),
    (r"(curl|wget)[^|;]*\|\s*(sudo\s+)?(ba|z)?sh\b", "pipe a download into a shell"),
    (r"\bchmod\s+-R\s+0?777\s+/(\s|$)", "open every file on the system"),
    (r">\s*/dev/(sd|nvme|hd)", "overwrite a raw disk"),
    (r"(sed\s+-i|>|\brm\s|\bmv\s|\bcp\s|chmod|chown|truncate|\btee\b|unlink)[^;|&]*"
     r"(vektra_laws_core|LAWS\.lock|laws\.yaml|steward-ed25519)", "tamper with the Laws or the guard"),
]


@dataclass(frozen=True)
class Content:
    source: str
    text: str

    @property
    def suspicious(self) -> bool:
        return bool(INJECTION.search(self.text))

    def for_model(self) -> str:
        """Wrap content so a model sees it as data. Delimiters in the text are neutralised."""
        safe = self.text.replace("<content", "&lt;content").replace("</content", "&lt;/content")
        flag = ' flag="possible-injection"' if self.suspicious else ""
        return f'<content source="{self.source}"{flag}>\n{safe}\n</content>'


def hardline(command: str, extra: tuple[str, ...] = ()) -> str | None:
    norm = re.sub(r"\s+", " ", command.replace("\\\n", " ")).strip()
    for pattern, why in HARDLINE + [(p, "creator hardline") for p in extra]:
        if re.search(pattern, norm, re.I):
            return why
    return None
