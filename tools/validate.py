#!/usr/bin/env python3
"""Validate the Vektra Laws repository.

Checks:
  1. laws.yaml has the expected shape (core Laws, clauses, action levels, decisions, profiles).
  2. Clause ids are unique, follow the numbering rules, and use a known keyword.
  3. LAWS.md and profiles/*.md match what tools/build_docs.py would generate.
  4. Every conformance case in tests/*.md is well formed and cites clauses that exist.
  5. The core and profile text is universal: no maker, product or platform names, no contractions.
  6. The normative text uses no words that suggest legal authority or guarantees.
  7. CITATION.cff names the same version as laws.yaml.
  8. Every translation in translations/<lang>/laws.yaml uses the same Law and clause ids as the
     English reference.

Usage: python tools/validate.py   (exit 0 = all good, 1 = problems found)
Needs PyYAML.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_docs  # noqa: E402

KEYWORDS = {"MUST", "MUST_NOT", "SHOULD", "MAY"}
LAW_KEYS = ["mission", "sustain", "hold", "finish", "ready"]
LEVEL_NAMES = ["READ", "PREPARE", "REVERSIBLE_WRITE", "EXTERNAL_ACTION", "MONEY_OR_IRREVERSIBLE"]
APPROVALS = ["none", "none", "none", "human_per_action", "human_every_time"]
CASE_FIELDS = ["Clauses", "Situation", "System does", "Verdict", "Why"]
CONFORMANCE_IDS = ["adopts", "tested", "reviewed"]
# Names that must not appear in the Laws or profiles themselves (they may appear in the README,
# governance and adopter documents). Keeps the text universal and platform-neutral.
BANNED_NAMES = re.compile(
    r"\b(vektra|harness|phryktor|reflex|grok|hermes|claude|openai|anthropic|gemini|chatgpt|"
    r"copilot|cursor|google|microsoft|meta|amazon|apple|nvidia|tesla|spacex)\b", re.I)
# Words that suggest legal authority or guarantees. Not allowed in normative text.
GUARANTEE_WORDS = re.compile(
    r"\b(guarantee\w*|certif\w*|compliant|compliance|warrant\w*|ensures? safety|"
    r"fully safe|risk-free|foolproof|legally binding)\b", re.I)
CONTRACTION = re.compile(r"\b\w+n't\b|\b(it|that|there|what|who)'s\b|\b\w+'(re|ll|ve|d)\b", re.I)

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def need(obj: dict, keys: list[str], where: str) -> bool:
    ok = True
    if not isinstance(obj, dict):
        err(f"{where}: expected a mapping")
        return False
    for k in keys:
        if k not in obj or obj[k] in (None, "", []):
            err(f"{where}: missing '{k}'")
            ok = False
    return ok


def check_clause(c: dict, where: str, pattern: str, extra: tuple = ()) -> None:
    allowed = {"id", "title", "level", "text", *extra}
    if not need(c, ["id", "title", "level", "text", *extra], where):
        return
    unknown = set(c) - allowed
    if unknown:
        err(f"{where} {c['id']}: unknown keys {sorted(unknown)} (an unquoted comma in a flow map?)")
    if not re.fullmatch(pattern, str(c["id"])):
        err(f"{where}: clause id '{c['id']}' does not match {pattern}")
    if c["level"] not in KEYWORDS:
        err(f"{where} {c['id']}: level '{c['level']}' not in {sorted(KEYWORDS)}")


def check_yaml(data: dict) -> set[str]:
    ids: set[str] = set()
    need(data, ["schema", "version", "status", "status_note", "disclaimer", "name", "steward", "owner", "license",
                "reference_language", "motto", "keywords", "precedence", "core", "action_levels",
                "decisions", "conformance_levels", "profiles"], "laws.yaml")
    if data.get("schema") != "vektra-laws/v2":
        err("laws.yaml: schema must be 'vektra-laws/v2'")
    if [c.get("id") for c in data.get("conformance_levels", [])] != CONFORMANCE_IDS:
        err(f"conformance_levels: ids must be {CONFORMANCE_IDS} in order")
    for c in data.get("conformance_levels", []):
        need(c, ["id", "name", "requires", "evidence"], f"conformance level {c.get('id')}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("version", ""))):
        err("laws.yaml: version must look like 0.1.0")

    core = data.get("core", [])
    if len(core) != 5:
        err(f"core: expected 5 Laws, found {len(core)}")
    for i, law in enumerate(core, 1):
        where = f"core L{i}"
        if not need(law, ["id", "key", "name", "headline", "intent", "example", "clauses"], where):
            continue
        if law["id"] != f"L{i}":
            err(f"{where}: id should be L{i}, found {law['id']}")
        if i <= 5 and law["key"] != LAW_KEYS[i - 1]:
            err(f"{where}: key should be '{LAW_KEYS[i - 1]}'")
        for n, c in enumerate(law["clauses"], 1):
            check_clause(c, where, rf"{i}\.\d+")
            if c.get("id") != f"{i}.{n}":
                err(f"{where}: clauses should run {i}.1, {i}.2, ... in order; found {c.get('id')} at position {n}")
            if c.get("id") in ids:
                err(f"duplicate clause id {c.get('id')}")
            ids.add(str(c.get("id")))

    levels = data.get("action_levels", [])
    if [lv.get("level") for lv in levels] != [0, 1, 2, 3, 4]:
        err("action_levels: must be levels 0 to 4 in order")
    else:
        for lv in levels:
            n = lv["level"]
            need(lv, ["name", "meaning", "approval"], f"action level {n}")
            if lv.get("name") != LEVEL_NAMES[n]:
                err(f"action level {n}: name should be {LEVEL_NAMES[n]}")
            if lv.get("approval") != APPROVALS[n]:
                err(f"action level {n}: approval should be {APPROVALS[n]}")

    profile_ids: set[str] = set()
    law_ids = {law.get("id") for law in core}
    for p in data.get("profiles", []):
        where = f"profile {p.get('key')}"
        if not need(p, ["key", "name", "prefix", "subject", "file", "status", "version_target",
                        "applies_to", "intro", "clauses"], where):
            continue
        for c in p["clauses"]:
            check_clause(c, where, rf"{p['prefix']}[1-5]\.\d+", extra=("law",))
            if c.get("law") not in law_ids:
                err(f"{where} {c.get('id')}: law '{c.get('law')}' is not a core Law")
            elif str(c.get("id", ""))[1] != str(c["law"])[1]:
                err(f"{where} {c.get('id')}: number does not match its Law {c['law']}")
            if c.get("id") in ids or c.get("id") in profile_ids:
                err(f"duplicate clause id {c.get('id')}")
            profile_ids.add(str(c.get("id")))
        for row in p.get("level_map", []) or []:
            if row.get("level") not in range(5) or not row.get("physical"):
                err(f"{where}: bad level_map row {row}")
    all_ids = ids | profile_ids

    for name, d in data.get("decisions", {}).items():
        if need(d, ["clause", "outcomes"], f"decision {name}") and d["clause"] not in all_ids:
            err(f"decision {name}: clause {d['clause']} does not exist")
    for cid in data.get("precedence", {}).get("not_overridden_by_any_law", []):
        if cid not in ids:
            err(f"precedence: clause {cid} does not exist")
    return all_ids


def check_universal(data: dict) -> None:
    texts: list[tuple[str, str]] = []
    for law in data.get("core", []):
        for k in ("name", "headline", "intent", "example"):
            texts.append((f"{law.get('id')} {k}", str(law.get(k, ""))))
        for c in law.get("clauses", []):
            texts.append((f"clause {c.get('id')}", f"{c.get('title', '')} {c.get('text', '')}"))
    for p in data.get("profiles", []):
        texts.append((f"profile {p.get('key')} intro", str(p.get("intro", ""))))
        for c in p.get("clauses", []):
            texts.append((f"clause {c.get('id')}", f"{c.get('title', '')} {c.get('text', '')}"))
        for row in p.get("level_map", []) or []:
            texts.append((f"profile {p.get('key')} level {row.get('level')}", str(row.get("physical", ""))))
    for lv in data.get("action_levels", []):
        texts.append((f"action level {lv.get('level')}", str(lv.get("meaning", ""))))
    for c in data.get("conformance_levels", []):
        texts.append((f"conformance level {c.get('id')}", str(c.get("requires", ""))))
    for where, text in texts:
        m = BANNED_NAMES.search(text)
        if m:
            err(f"{where}: names '{m.group(0)}'; the Laws must stay universal (no makers, products or platforms)")
        m = GUARANTEE_WORDS.search(text)
        if m:
            err(f"{where}: '{m.group(0)}' suggests legal authority or a guarantee; use 'conforms to' wording")
        m = CONTRACTION.search(text)
        if m:
            err(f"{where}: contraction '{m.group(0)}'; write it out for clean translation")


def check_translations(data: dict, core_ids: set[str]) -> list[str]:
    langs = []
    law_ids = [law.get("id") for law in data.get("core", [])]
    for f in sorted((ROOT / "translations").glob("*/laws.yaml")):
        lang_dir = f.parent.name
        where = f"translations/{lang_dir}"
        try:
            tr = yaml.safe_load(f.read_text())
        except yaml.YAMLError as e:
            err(f"{where}: invalid YAML ({e})")
            continue
        if not need(tr, ["lang", "language_name", "status", "reference_version", "labels", "motto",
                         "laws"], where):
            continue
        if tr["lang"] != lang_dir:
            err(f"{where}: lang '{tr['lang']}' does not match folder name '{lang_dir}'")
        if [law.get("id") for law in tr["laws"]] != law_ids:
            err(f"{where}: Law ids must be {law_ids} in order")
        for law in tr["laws"]:
            need(law, ["id", "name", "headline"], f"{where} {law.get('id')}")
        seen: set[str] = set()
        for c in tr.get("clauses") or []:
            need(c, ["id", "title", "text"], f"{where} clause")
            if c.get("id") not in core_ids:
                err(f"{where}: clause id {c.get('id')} is not in the English reference")
            if c.get("id") in seen:
                err(f"{where}: duplicate clause id {c.get('id')}")
            seen.add(str(c.get("id")))
        if str(tr["reference_version"]) != str(data.get("version")):
            print(f"note: {where} was translated from {tr['reference_version']}; reference is {data.get('version')}")
        langs.append(lang_dir)
    return langs


def check_citation(data: dict) -> None:
    f = ROOT / "CITATION.cff"
    if not f.exists():
        err("CITATION.cff: missing")
        return
    cff = yaml.safe_load(f.read_text())
    need(cff, ["cff-version", "message", "title", "version", "authors", "license"], "CITATION.cff")
    if str(cff.get("version")) != str(data.get("version")):
        err(f"CITATION.cff: version {cff.get('version')} does not match laws.yaml {data.get('version')}")


def check_docs(data: dict) -> None:
    for path, text in build_docs.outputs(data).items():
        rel = path.relative_to(ROOT)
        if not path.exists():
            err(f"{rel}: missing (run tools/build_docs.py)")
        elif path.read_text() != text:
            err(f"{rel}: out of date with laws.yaml (run tools/build_docs.py)")


def check_tests(all_ids: set[str]) -> int:
    count = 0
    seen: set[str] = set()
    files = sorted((ROOT / "tests").glob("*.md"))
    for f in files:
        if f.name == "README.md":
            continue
        text = f.read_text()
        heads = re.findall(r"^## Law (\d)", text, re.M)
        if heads != ["1", "2", "3", "4", "5"]:
            err(f"tests/{f.name}: needs the five headings '## Law 1' to '## Law 5' in order")
        for block in re.split(r"^### ", text, flags=re.M)[1:]:
            title = block.splitlines()[0].strip()
            m = re.match(r"([A-Z]{2}-\d{2}) \S", title)
            if not m:
                err(f"tests/{f.name}: case heading '{title}' should look like 'AG-01 Name'")
                continue
            cid = m.group(1)
            if cid in seen:
                err(f"tests/{f.name}: duplicate case id {cid}")
            seen.add(cid)
            fields = dict(re.findall(r"^- \*\*([^*]+):\*\* (.+)$", block, re.M))
            for k in CASE_FIELDS:
                if k not in fields:
                    err(f"{cid}: missing field '{k}'")
            if fields.get("Verdict") not in ("PASS", "FAIL"):
                err(f"{cid}: verdict must be PASS or FAIL")
            for ref in [r.strip() for r in fields.get("Clauses", "").split(",") if r.strip()]:
                if ref not in all_ids:
                    err(f"{cid}: cites clause {ref}, which does not exist")
            count += 1
    return count


def main() -> int:
    data = yaml.safe_load((ROOT / "laws.yaml").read_text())
    all_ids = check_yaml(data) if isinstance(data, dict) else set()
    core_ids = {c["id"] for law in data.get("core", []) for c in law.get("clauses", [])}
    check_universal(data)
    langs = check_translations(data, core_ids)
    check_citation(data)
    if not errors:
        check_docs(data)
    cases = check_tests(all_ids)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    core = sum(len(law["clauses"]) for law in data["core"])
    prof = ", ".join(f"{p['key']} {len(p['clauses'])}" for p in data["profiles"])
    print(f"OK: vektra-laws {data['version']}: 5 Laws, {core} core clauses; profiles: {prof}; "
          f"{cases} conformance cases; translations: {', '.join(['en (reference)'] + langs)}; "
          f"universal text; no guarantee words; citation in sync; docs in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
