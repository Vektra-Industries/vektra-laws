#!/usr/bin/env python3
"""Generate LAWS.md and profiles/*.md from laws.yaml.

laws.yaml is the source. Run this after editing it:
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
         "- **Reference text:** English.", ""]
    L += status_block(data)
    L += ["## Introduction", "", "*This section is informative.*", "",
          "The Vektra Laws are a preamble and five laws for systems that act for people: AI agents,",
          "robots and AI models, from any maker, in any country, on Earth or beyond. This document is",
          "the core. It states the Mission (the preamble), the five Laws and their clauses, the",
          "Understanding Matrix, the action levels, the decision outcomes and the conformance levels.",
          "Profiles add detailed clauses for each kind of system:",
          "[agents](profiles/AGENTS.md), [robotics](profiles/ROBOTICS.md) and",
          "[models](profiles/MODELS.md). The [operators](profiles/OPERATORS.md) profile states the",
          "duties of the people and organizations that run a system.", "",
          "## Summary of the Laws", "", "*This section is informative.*", "",
          f"**{data['mission']['name']}** (preamble). {data['mission']['headline']}", ""]
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
          "The preamble and each Law have a statement and numbered clauses, which are normative, and an",
          "intent and an example, which are informative. Preamble clauses are numbered P.1, P.2 and so",
          "on. The preamble is not a numbered Law and does not take part in precedence; it never",
          "overrides a Law (P.2).", "",
          "## Precedence and local law", "", "*This section is normative.*", "",
          f"1. {data['precedence']['rule']}",
          f"2. {data['precedence']['local_law']}",
          f"3. {data['precedence']['note'].strip()}", ""]
    m = data["mission"]
    L += ["---", "", f"## Preamble: {m['name']}", "",
          f"**Statement (normative).** {m['headline']}", "",
          f"**Intent (informative).** {m['intent'].strip()}", "",
          "**Clauses (normative).**", ""]
    L += [clause_line(c) for c in m["clauses"]]
    L += ["", f"**Example (informative).** {m['example'].strip()}", ""]
    for i, law in enumerate(data["core"], 1):
        L += ["---", "", f"## Law {i}: {law['name']}", "",
              f"**Statement (normative).** {law['headline']}", ""]
        if law.get("bound_by"):
            L += [f"**Bound by (normative).** {law['bound_by'].strip()}", ""]
        L += [f"**Intent (informative).** {law['intent'].strip()}", "",
              "**Clauses (normative).**", ""]
        L += [clause_line(c) for c in law["clauses"]]
        L += ["", f"**Example (informative).** {law['example'].strip()}", ""]
    L += build_matrix(data)
    L += ["---", "", "## Action levels", "", "*This section is normative.*", "",
          "Clauses 2.7 to 2.10 use these levels. Each action has a level before the system is deployed.", "",
          "| Level | Name | Scope | Approval required |", "|---|---|---|---|"]
    for lv in data["action_levels"]:
        L.append(f"| {lv['level']} | {lv['name']} | {lv['meaning']} | {APPROVAL[lv['approval']]} |")
    L += ["", "A classifier can suggest a level. It cannot lower a level or remove an approval (2.9).", "",
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


def build_matrix(data: dict) -> list[str]:
    um = data["understanding_matrix"]
    q = um["questions"]
    L = ["---", "", f"## {um['name']}", "", "*This section is normative.*", "",
         um["rule"].strip(), "",
         f"- **Harm of inaction:** {q['inaction']}",
         f"- **Harm of wrong action:** {q['wrong_action']}", "",
         "| Cell | Harm of inaction | Harm of wrong action | Outcome | In short |",
         "|---|---|---|---|---|"]
    for c in um["cells"]:
        L.append(f"| {c['id']} | {c['inaction']} | {c['wrong_action']} | `{c['outcome']}` | {c['text']} |")
    L += ["", "Outcomes:", ""]
    for k, o in um["outcomes"].items():
        cells = [c["id"] for c in um["cells"] if c["outcome"] == k]
        where = ", ".join(cells) if cells else "any cell, when the system is blocked"
        L.append(f"- **`{k}`** ({where}). {o['meaning']} Action check: `{o['action_check']}`.")
    L += ["", "Rules for proactive choice:", ""]
    L += [clause_line(c) for c in um["proactive_rules"]]
    L += ["", "A step-by-step explanation with worked examples is in",
          "[docs/UNDERSTANDING-MATRIX.md](docs/UNDERSTANDING-MATRIX.md) (informative).", ""]
    return L


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
        L += ["", "Approval for each level follows core clause 2.8.", ""]
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


def outputs(data: dict) -> dict[Path, str]:
    out = {ROOT / "LAWS.md": build_laws(data)}
    for p in data["profiles"]:
        out[ROOT / p["file"]] = build_profile(data, p)
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
