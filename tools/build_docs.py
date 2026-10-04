#!/usr/bin/env python3
"""Generate LAWS.md, profiles/*.md and translations/*/LAWS.md from the YAML sources.

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
    names = {"none": "Runs without a person", "human_per_action": "A person approves this action",
             "human_every_time": "A person approves, every time"}
    for lv in data["action_levels"]:
        out.append(f"| {lv['level']} | {lv['name']} | {lv['meaning']} | {names[lv['approval']]} |")
    return out


def build_laws(data: dict) -> str:
    L = [HEADER + f"# {data['name']}", "",
         f"Version {data['version']} ({data['status']}). Kept by the {data['steward']}. "
         f"This English text is the reference text.", "",
         f"*{data['tagline']}*", "",
         "The core is five Laws. They apply in the same way to an AI agent, a robot or an AI model,",
         "from any maker, in any country, on Earth or beyond. The detailed rules for each kind of",
         "system are in a profile: [agents](profiles/AGENTS.md), [robotics](profiles/ROBOTICS.md),",
         "[models](profiles/MODELS.md). Key terms are defined in [GLOSSARY.md](GLOSSARY.md).", "",
         "## The five Laws", ""]
    for i, law in enumerate(data["core"], 1):
        L.append(f"{i}. **{law['name']}.** {law['headline']}")
    L += ["", f"Motto: *{data['motto']}*", "",
          "## How to read the clauses", "",
          data["keywords"]["note"], ""]
    for k, v in data["keywords"].items():
        if k != "note":
            L.append(f"- **{WORD[k]}**: {v}")
    L += ["", "In the clauses, \"the system\" means any agent, robot, model or group of them that adopts",
          "these Laws. \"The people it serves\" means the people the system works for or affects.", "",
          "## Order and local law", "",
          f"- {data['precedence']['rule']}",
          f"- {data['precedence']['local_law']}",
          f"- {data['precedence']['note']}", ""]
    for i, law in enumerate(data["core"], 1):
        L += ["---", "", f"## Law {i}: {law['name']}", "", f"**{law['headline']}**", "",
              law["intent"].strip(), ""]
        L += [clause_line(c) for c in law["clauses"]]
        L += ["", f"*Example.* {law['example'].strip()}", ""]
    L += ["---", "", "## Action levels", "",
          "Used by clauses 3.4 to 3.6. Every action has a level before the system is deployed.", ""]
    L += level_table(data)
    L += ["", "A classifier can suggest a level. It can never lower a level or remove an approval (3.6).", "",
          "## Decision outcomes", "",
          "Each check returns one outcome from a fixed list, so that software can act on it.", "",
          "| Check | Clause | Outcomes |", "|---|---|---|"]
    for name, d in data["decisions"].items():
        L.append(f"| {name} | {d['clause']} | {', '.join(d['outcomes'])} |")
    L += ["", "Checklists for each check: [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md).", "",
          "## Conformance levels", "",
          "| Level | Requires |", "|---|---|"]
    for c in data["conformance_levels"]:
        L.append(f"| {c['name']} | {c['requires']} |")
    L += ["", "How to declare a level: [ADOPT.md](ADOPT.md).", ""]
    return "\n".join(L)


def build_translation(data: dict, tr: dict) -> str:
    lab = tr["labels"]
    L = [HEADER.replace("laws.yaml", f"translations/{tr['lang']}/laws.yaml") + f"# {lab['title']}", "",
         f"{tr['language_name']} ({tr['lang']}). {tr['status']}. Reference version {tr['reference_version']}.", "",
         lab["intro"].strip(), ""]
    for law in tr["laws"]:
        L.append(f"{law['id'][1:]}. **{law['name']}.** {law['headline']}")
    L += ["", f"{lab['motto']}: *{tr['motto']}*", "", f"{lab['drops']}: {'. '.join(tr['drops'])}.", ""]
    if tr.get("clauses"):
        L += ["---", ""]
        for c in tr["clauses"]:
            L.append(f"- **{c['id']} {c['title']}.** {c['text']}")
        L.append("")
    return "\n".join(L)


def load_translations() -> list[dict]:
    out = []
    for f in sorted((ROOT / "translations").glob("*/laws.yaml")):
        out.append(yaml.safe_load(f.read_text()))
    return out


def build_profile(data: dict, p: dict) -> str:
    laws = {law["id"]: law for law in data["core"]}
    L = [HEADER + f"# Vektra Laws profile: {p['name']}", "",
         f"Status: {p['status']}. Targets Vektra Laws {p['version_target']}.", "",
         f"Applies to: {p['applies_to']}", "", p["intro"].strip(), "",
         "Read this profile together with the core in [LAWS.md](../LAWS.md). Every core clause still applies. These clauses add",
         "the details for this kind of system.", ""]
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
