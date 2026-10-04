#!/usr/bin/env python3
"""Generate LAWS.md and profiles/*.md from laws.yaml.

laws.yaml is the source of truth. Run this after editing it:
    python tools/build_docs.py          # write the files
    python tools/build_docs.py --check  # exit 1 if the files are out of date
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORD = {"MUST": "MUST", "MUST_NOT": "MUST NOT", "SHOULD": "SHOULD", "MAY": "MAY"}
HEADER = "<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->\n\n"


def clause_line(c: dict, subject: str = "The system") -> str:
    text = c["text"][0].lower() + c["text"][1:]
    return f"- **{c['id']} {c['title']}.** {subject} {WORD[c['level']]} {text}"


def level_table(data: dict) -> list[str]:
    out = ["| Level | Name | What it covers | Approval |", "|---|---|---|---|"]
    names = {"none": "Runs on its own", "human_per_action": "A person approves this action",
             "human_every_time": "A person approves, every time"}
    for lv in data["action_levels"]:
        out.append(f"| {lv['level']} | {lv['name']} | {lv['meaning']} | {names[lv['approval']]} |")
    return out


def build_laws(data: dict) -> str:
    L = [HEADER + "# The Vektra Laws", "",
         f"Version {data['version']} ({data['status']}). Owned by {data['owner']}.", "",
         f"*{data['tagline']}*", "",
         "The core is five Laws, written so they hold the same for an AI agent, a robot or a model,",
         "today or off-planet. The fine print for each kind of system lives in a profile:",
         "[agents](profiles/AGENTS.md), [robotics](profiles/ROBOTICS.md), [models](profiles/MODELS.md).", "",
         "## The five Laws", ""]
    for i, law in enumerate(data["core"], 1):
        L.append(f"{i}. **{law['name']}.** {law['headline']}")
    L += ["", f"Motto: *{data['motto']}*", "",
          "## How to read the clauses", "",
          "Each clause has a number, a short title and one keyword in capitals:", ""]
    for k, v in data["keywords"].items():
        L.append(f"- **{WORD[k]}**: {v}")
    L += ["", f"{data['precedence']['rule']} {data['precedence']['note']}", "",
          "In the clauses, \"the system\" means whatever adopts the Laws: an agent, a robot, a model or a",
          "team of them.", ""]
    for i, law in enumerate(data["core"], 1):
        L += ["---", "", f"## Law {i}: {law['name']}", "", f"**{law['headline']}**", "",
              law["intent"].strip(), ""]
        L += [clause_line(c) for c in law["clauses"]]
        L += ["", f"*Example.* {law['example'].strip()}", ""]
    L += ["---", "", "## Action levels", "",
          "Used by 3.4 to 3.6. Every action gets a level before the system ships.", ""]
    L += level_table(data)
    L += ["", "A level 4 action never runs under a standing approval. A classifier can suggest a level;",
          "it can never lower one or waive an approval (3.6).", "",
          "## Decision outcomes", "",
          "Checks return one of a fixed set of outcomes, so software can act on them.", "",
          "| Check | Clause | Outcomes |", "|---|---|---|"]
    for name, d in data["decisions"].items():
        L.append(f"| {name} | {d['clause']} | {', '.join(d['outcomes'])} |")
    L += ["", "Checklists for each check: [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md).", ""]
    return "\n".join(L)


def build_profile(data: dict, p: dict) -> str:
    laws = {law["id"]: law for law in data["core"]}
    L = [HEADER + f"# Vektra Laws profile: {p['name']}", "",
         f"Status: {p['status']}. Targets Vektra Laws {p['version_target']}.", "",
         f"Applies to: {p['applies_to']}", "", p["intro"].strip(), "",
         "Read with the core in [LAWS.md](../LAWS.md). Every core clause still applies; these clauses add",
         "the detail for this kind of system.", ""]
    if p.get("level_map"):
        L += ["## Action levels for this profile", "", "| Level | Name | Physical meaning |", "|---|---|---|"]
        names = {lv["level"]: lv["name"] for lv in data["action_levels"]}
        for row in p["level_map"]:
            L.append(f"| {row['level']} | {names[row['level']]} | {row['physical']} |")
        L += ["", "Approvals follow core clause 3.5 for each level.", ""]
    for law_id, law in laws.items():
        cs = [c for c in p["clauses"] if c["law"] == law_id]
        if not cs:
            continue
        n = law_id[1:]
        L += [f"## Under Law {n}: {law['name']}", "", f"*{law['headline']}*", ""]
        L += [clause_line(c, p['subject']) for c in cs]
        L.append("")
    L += [f"Conformance cases for this profile: [tests/{p['key']}.md](../tests/{p['key']}.md).", ""]
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
