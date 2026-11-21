#!/usr/bin/env python3
"""Generate LAWS.md, profiles/*.md and translations/*/LAWS.md from the YAML sources.

laws.yaml and translations/*/laws.yaml are the sources. Run this after editing them:
    python tools/build_docs.py          # write the files
    python tools/build_docs.py --check  # exit 1 if the files are out of date
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORD = {"MUST": "MUST", "MUST_NOT": "MUST NOT", "SHOULD": "SHOULD", "MAY": "MAY"}
APPROVAL = {"none": "None (runs inside the given permissions)",
            "human_per_action": "A person approves the specific action",
            "human_every_time": "A person approves the specific action, every time"}


def header(source: str) -> str:
    return f"<!-- Generated from {source} by tools/build_docs.py. Edit {source}, not this file. -->\n\n"


def clause_line(c: dict, subject: str = "The system") -> str:
    text = c["text"][0].lower() + c["text"][1:]
    return f"- **{c['id']} {c['title']}.** {subject} {WORD[c['level']]} {text}"


def status_block(data: dict) -> list[str]:
    return ["## Status of this document", "", "*This section is informative.*", "",
            f"This document is version {data['version']} of the {data['name']}. {data['status_note'].strip()}", "",
            data["disclaimer"].strip(), ""]


def build_laws(data: dict) -> str:
    L = [header("laws.yaml") + f"# {data['name']}", "",
         f"*{data['tagline']}*", "",
         f"- **Version:** {data['version']} ({data['status']})",
         f"- **Steward:** {data['steward']}",
         f"- **Copyright:** {data['owner']}, licensed under CC BY 4.0",
         "- **Reference text:** English. Translations are informative.", ""]
    L += status_block(data)
    L += ["## Introduction", "", "*This section is informative.*", "",
          "The Vektra Laws are five laws for systems that act for people: AI agents, robots and AI",
          "models, from any maker, in any country, on Earth or beyond. This document is the core. It",
          "states the five Laws and their clauses, the action levels, the decision outcomes and the",
          "conformance levels. Profiles add detailed clauses for each kind of system:",
          "[agents](profiles/AGENTS.md), [robotics](profiles/ROBOTICS.md) and",
          "[models](profiles/MODELS.md). The [operators](profiles/OPERATORS.md) profile states the",
          "duties of the people and organizations that run a system.", "",
          "## Summary of the Laws", "", "*This section is informative.*", ""]
    for i, law in enumerate(data["core"], 1):
        L.append(f"{i}. **{law['name']}.** {law['headline']}")
    L += ["", f"Motto: *{data['motto']}*", "",
          "## Conventions and terminology", "", "*This section is normative.*", "",
          data["keywords"]["note"].strip(), ""]
    for k, v in data["keywords"].items():
        if k != "note":
            L.append(f"- **{WORD[k]}**: {v}")
    L += ["",
          "\"The system\" means any AI agent, robot, AI model, or group of them, to which these Laws",
          "are applied. \"The people it serves\" means the people the system works for or affects.",
          "Other terms have the meanings given in [GLOSSARY.md](GLOSSARY.md).", "",
          "Each Law has a statement and numbered clauses, which are normative, and an intent and an",
          "example, which are informative.", "",
          "## Precedence and local law", "", "*This section is normative.*", "",
          f"1. {data['precedence']['rule']}",
          f"2. {data['precedence']['local_law']}",
          f"3. {data['precedence']['note'].strip()}", ""]
    for i, law in enumerate(data["core"], 1):
        L += ["---", "", f"## Law {i}: {law['name']}", "",
              f"**Statement (normative).** {law['headline']}", "",
              f"**Intent (informative).** {law['intent'].strip()}", "",
              "**Clauses (normative).**", ""]
        L += [clause_line(c) for c in law["clauses"]]
        L += ["", f"**Example (informative).** {law['example'].strip()}", ""]
    L += ["---", "", "## Action levels", "", "*This section is normative.*", "",
          "Clauses 3.4 to 3.6 use these levels. Each action has a level before the system is deployed.", "",
          "| Level | Name | Scope | Approval required |", "|---|---|---|---|"]
    for lv in data["action_levels"]:
        L.append(f"| {lv['level']} | {lv['name']} | {lv['meaning']} | {APPROVAL[lv['approval']]} |")
    L += ["", "A classifier can suggest a level. It cannot lower a level or remove an approval (3.6).", "",
          "## Decision outcomes", "", "*This section is normative.*", "",
          "Each check returns exactly one outcome from a fixed list.", "",
          "| Check | Clause | Outcomes |", "|---|---|---|"]
    for name, d in data["decisions"].items():
        L.append(f"| {name} | {d['clause']} | {', '.join(d['outcomes'])} |")
    L += ["", "Checklists for these checks are in [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md) (informative).", "",
          "## Conformance", "", "*This section is normative.*", "",
          "| Level | Requirements |", "|---|---|"]
    for c in data["conformance_levels"]:
        L.append(f"| {c['name']} | {c['requires']} |")
    L += ["",
          "1. A conformance claim names the system, its version, the profile, the version of the Laws,",
          "   the conformance level and, for Tested and Reviewed, the version of the conformance suite.",
          "2. A conformance claim is a self-declaration by the adopter unless an independent reviewer",
          "   has reviewed it. The Reviewed level requires a named reviewer.",
          "3. The steward does not certify systems. A statement by the steward about a specific system",
          "   is valid only when the steward makes it explicitly, in writing, for a named system and version.",
          "4. A conformance claim is a statement about these Laws only. It is not a statement of",
          "   compliance with any statute, regulation or standard.",
          "5. Results name the system under test and its scope: the whole system, or a component of a",
          "   larger system. A case that does not apply is marked not applicable, with a written reason.",
          "   Cases marked not applicable do not count toward the Tested level.",
          "6. A claim for a component states \"component scope\" and names every duty of the host that the",
          "   component does not cover. It is valid only when every applicable case passes.", "",
          "The declaration template is in [ADOPT.md](ADOPT.md).", "",
          "## References", "", "*This section is informative, except where marked.*", "",
          "- **Normative:** BCP 14: RFC 2119, \"Key words for use in RFCs to Indicate Requirement Levels\";",
          "  RFC 8174, \"Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words\".",
          "- **Normative:** [GLOSSARY.md](GLOSSARY.md).",
          "- [Profiles](profiles/), [conformance cases](tests/),",
          "  [alignment with other frameworks](docs/ALIGNMENT.md).", ""]
    return "\n".join(L)


def build_profile(data: dict, p: dict) -> str:
    laws = {law["id"]: law for law in data["core"]}
    L = [header("laws.yaml") + f"# Vektra Laws profile: {p['name']}", "",
         f"- **Profile status:** {p['status']}",
         f"- **Laws version:** {data['version']}",
         f"- **Applies to:** {p['applies_to']}", ""]
    L += status_block(data)
    L += ["## Introduction", "", "*This section is informative.*", "", p["intro"].strip(), "",
          "## Relation to the core", "", "*This section is normative.*", "",
          *(p.get("relation") or [
              "1. Every clause of the core ([LAWS.md](../LAWS.md)) applies to systems in this profile.",
              "2. The clauses below add requirements for this kind of system. When a clause here is",
              "   stricter than a core clause, the stricter clause applies."]),
          f"{len(p.get('relation') or [1, 2]) + 1}. Terms have the meanings given in [GLOSSARY.md](../GLOSSARY.md).", ""]
    if p.get("level_map"):
        names = {lv["level"]: lv["name"] for lv in data["action_levels"]}
        L += ["## Action levels for this profile", "", "*This section is normative.*", "",
              "| Level | Name | Physical scope |", "|---|---|---|"]
        for row in p["level_map"]:
            L.append(f"| {row['level']} | {names[row['level']]} | {row['physical']} |")
        L += ["", "Approval for each level follows core clause 3.5.", ""]
    L += ["## Clauses", "", "*This section is normative.*", ""]
    for law_id, law in laws.items():
        cs = [c for c in p["clauses"] if c["law"] == law_id]
        if not cs:
            continue
        L += [f"### Under Law {law_id[1:]}: {law['name']}", ""]
        L += [clause_line(c, p["subject"]) for c in cs]
        L.append("")
    L += ["## Conformance cases", "", "*This section is informative.*", "",
          f"Conformance cases for this profile: [tests/{p['key']}.md](../tests/{p['key']}.md).", ""]
    return "\n".join(L)


def build_translation(data: dict, tr: dict) -> str:
    lab = tr["labels"]
    src = f"translations/{tr['lang']}/laws.yaml"
    L = [header(src) + f"# {lab['title']}", "",
         f"{tr['language_name']} ({tr['lang']}). Status: {tr['status']}. "
         f"Reference version: {tr['reference_version']}.", "",
         lab["intro"].strip(), ""]
    for law in tr["laws"]:
        L.append(f"{law['id'][1:]}. **{law['name']}.** {law['headline']}")
    L += ["", f"{lab['motto']}: *{tr['motto']}*", ""]
    if tr.get("clauses"):
        L += ["---", ""]
        for c in tr["clauses"]:
            L.append(f"- **{c['id']} {c['title']}.** {c['text']}")
        L.append("")
    return "\n".join(L)


def load_translations() -> list[dict]:
    return [yaml.safe_load(f.read_text()) for f in sorted((ROOT / "translations").glob("*/laws.yaml"))]


def outputs(data: dict) -> dict[Path, str]:
    out = {ROOT / "LAWS.md": build_laws(data)}
    for p in data["profiles"]:
        out[ROOT / p["file"]] = build_profile(data, p)
    for tr in load_translations():
        out[ROOT / "translations" / tr["lang"] / "LAWS.md"] = build_translation(data, tr)
    return out


def main() -> int:
    data = yaml.safe_load((ROOT / "laws.yaml").read_text())
    check = "--check" in sys.argv
    stale = []
    for path, text in outputs(data).items():
        if check:
            if not path.exists() or path.read_text() != text:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        print("out of date (run tools/build_docs.py): " + ", ".join(map(str, stale)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
