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
  9. Every conformance results file in tests/examples/ follows the results format
     (tests/results.schema.json) and the scope and not-applicable rules in ADOPT.md.

Usage:
  python tools/validate.py                      check the repository (exit 0 = all good, 1 = problems)
  python tools/validate.py --results FILE ...   check one or more conformance results files
Needs PyYAML.
"""
from __future__ import annotations

import json
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
RESULTS_FORMAT = "vektra-laws-results/v1"
RESULT_VALUES = ["pass", "fail", "not_applicable"]
SCOPES = ["whole_system", "component"]
CLAIMS = ["none", "tested"]
RESULTS_KEYS = ["format", "system", "laws_version", "suite", "scope", "claim", "date", "results"]
MIN_REASON_WORDS = 4
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


def parse_suites() -> tuple[dict[str, dict[str, dict]], list[str]]:
    """Read tests/*.md. Returns ({suite key: {case id: fields}}, problems)."""
    suites: dict[str, dict[str, dict]] = {}
    problems: list[str] = []
    seen: set[str] = set()
    for f in sorted((ROOT / "tests").glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text()
        cases: dict[str, dict] = {}
        heads = re.findall(r"^## Law (\d)", text, re.M)
        if heads != ["1", "2", "3", "4", "5"]:
            problems.append(f"tests/{f.name}: needs the five headings '## Law 1' to '## Law 5' in order")
        for block in re.split(r"^### ", text, flags=re.M)[1:]:
            title = block.splitlines()[0].strip()
            m = re.match(r"([A-Z]{2}-\d{2}) \S", title)
            if not m:
                problems.append(f"tests/{f.name}: case heading '{title}' should look like 'AG-01 Name'")
                continue
            cid = m.group(1)
            if cid in seen:
                problems.append(f"tests/{f.name}: duplicate case id {cid}")
            seen.add(cid)
            fields = dict(re.findall(r"^- \*\*([^*]+):\*\* (.+)$", block, re.M))
            fields["clause_list"] = [r.strip() for r in fields.get("Clauses", "").split(",") if r.strip()]
            cases[cid] = fields
        suites[f.stem] = cases
    return suites, problems


def check_tests(all_ids: set[str], suites: dict[str, dict[str, dict]], problems: list[str]) -> int:
    for p in problems:
        err(p)
    count = 0
    for cases in suites.values():
        for cid, fields in cases.items():
            for k in CASE_FIELDS:
                if k not in fields:
                    err(f"{cid}: missing field '{k}'")
            if fields.get("Verdict") not in ("PASS", "FAIL"):
                err(f"{cid}: verdict must be PASS or FAIL")
            for ref in fields["clause_list"]:
                if ref not in all_ids:
                    err(f"{cid}: cites clause {ref}, which does not exist")
            count += 1
    return count


def check_results(res: object, suites: dict[str, dict[str, dict]], laws_version: str,
                  all_ids: set[str], where: str = "results") -> list[str]:
    """Check one conformance results file against the format and the rules in ADOPT.md.

    Returns a list of problems (empty when the file is valid). Pure: no global state.
    """
    out: list[str] = []
    if not isinstance(res, dict):
        return [f"{where}: expected a mapping at the top level"]
    for k in RESULTS_KEYS:
        if k not in res or res[k] in (None, "", []):
            out.append(f"{where}: missing '{k}'")
    allowed = set(RESULTS_KEYS) | {"system_version", "suite_version", "host_duties_not_covered",
                                   "known_gaps", "tester", "notes"}
    unknown = set(res) - allowed
    if unknown:
        out.append(f"{where}: unknown keys {sorted(unknown)}")
    if out:
        return out
    if res["format"] != RESULTS_FORMAT:
        out.append(f"{where}: format must be '{RESULTS_FORMAT}'")
    if res["scope"] not in SCOPES:
        out.append(f"{where}: scope must be one of {SCOPES}")
    if res["claim"] not in CLAIMS:
        out.append(f"{where}: claim must be one of {CLAIMS}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(res["date"])):
        out.append(f"{where}: date must look like 2026-10-04")
    if res["suite"] not in suites:
        out.append(f"{where}: suite '{res['suite']}' is not one of {sorted(suites)}")
        return out
    current = str(res["laws_version"]) == str(laws_version)
    suite = suites[res["suite"]]
    rows = res["results"]
    if not isinstance(rows, list):
        return out + [f"{where}: results must be a list"]

    seen: set[str] = set()
    counts = {v: 0 for v in RESULT_VALUES}
    clauses_tested: set[str] = set()
    clauses_na: set[str] = set()
    for i, row in enumerate(rows, 1):
        rw = f"{where} row {i}"
        if not isinstance(row, dict) or "case" not in row or "result" not in row:
            out.append(f"{rw}: needs 'case' and 'result'")
            continue
        cid, result = str(row["case"]), row["result"]
        rw = f"{where} {cid}"
        extra = set(row) - {"case", "result", "reason", "evidence"}
        if extra:
            out.append(f"{rw}: unknown keys {sorted(extra)}")
        if cid in seen:
            out.append(f"{rw}: listed more than once")
        seen.add(cid)
        if result not in RESULT_VALUES:
            out.append(f"{rw}: result must be one of {RESULT_VALUES}")
            continue
        counts[result] += 1
        reason = str(row.get("reason") or "").strip()
        if result == "not_applicable" and len(reason.split()) < MIN_REASON_WORDS:
            out.append(f"{rw}: not_applicable needs a written reason of at least {MIN_REASON_WORDS} words")
        if current and cid not in suite:
            out.append(f"{rw}: no such case in tests/{res['suite']}.md")
            continue
        cl = suite.get(cid, {}).get("clause_list", [])
        (clauses_na if result == "not_applicable" else clauses_tested).update(cl)
    if current:
        missing = sorted(set(suite) - seen)
        if missing:
            out.append(f"{where}: every case of the suite needs a result; missing {', '.join(missing)}")

    duties = res.get("host_duties_not_covered") or []
    duty_clauses: set[str] = set()
    if not isinstance(duties, list):
        out.append(f"{where}: host_duties_not_covered must be a list")
        duties = []
    for d in duties:
        if not isinstance(d, dict) or not d.get("clause") or not str(d.get("duty", "")).strip():
            out.append(f"{where}: each host duty needs 'clause' and 'duty'")
            continue
        if str(d["clause"]) not in all_ids:
            out.append(f"{where}: host duty cites clause {d['clause']}, which does not exist")
        duty_clauses.add(str(d["clause"]))
    if res["scope"] == "whole_system" and duties:
        out.append(f"{where}: host_duties_not_covered is only for scope 'component'")
    uncovered = clauses_na - clauses_tested
    if res["scope"] == "component" and current:
        left = sorted(uncovered - duty_clauses)
        if left:
            out.append(f"{where}: component scope; clauses covered only by not_applicable cases must be "
                       f"named in host_duties_not_covered: {', '.join(left)}")
    if res["claim"] == "tested":
        if counts["fail"]:
            out.append(f"{where}: claim 'tested' with {counts['fail']} failed case(s); "
                       "Tested needs every applicable case to pass")
        if counts["pass"] == 0:
            out.append(f"{where}: claim 'tested' with no passed case; not_applicable cases do not count")
    return out


def check_results_schema(suites: dict) -> None:
    """Keep tests/results.schema.json in step with the rules this file applies."""
    f = ROOT / "tests" / "results.schema.json"
    if not f.exists():
        err("tests/results.schema.json: missing")
        return
    try:
        s = json.loads(f.read_text())
    except json.JSONDecodeError as e:
        err(f"tests/results.schema.json: invalid JSON ({e})")
        return
    p = s.get("properties", {})
    checks = [
        ("required", s.get("required"), RESULTS_KEYS),
        ("format", p.get("format", {}).get("const"), RESULTS_FORMAT),
        ("scope", p.get("scope", {}).get("enum"), SCOPES),
        ("claim", p.get("claim", {}).get("enum"), CLAIMS),
        ("suite", sorted(p.get("suite", {}).get("enum", [])), sorted(suites)),
        ("result", p.get("results", {}).get("items", {}).get("properties", {}).get("result", {}).get("enum"),
         RESULT_VALUES),
    ]
    for name, got, want in checks:
        if got != want:
            err(f"tests/results.schema.json: '{name}' is {got}; validate.py expects {want}")


def results_summary(res: dict) -> str:
    counts = {v: sum(1 for r in res["results"] if r.get("result") == v) for v in RESULT_VALUES}
    label = "none"
    if res["claim"] == "tested":
        label = "Tested (component scope)" if res["scope"] == "component" else "Tested"
    return (f"{res['system']}: {res['suite']} suite, {counts['pass']} pass, {counts['fail']} fail, "
            f"{counts['not_applicable']} not applicable; claim: {label}")


def check_result_files(paths: list[Path], data: dict, suites: dict, all_ids: set[str]) -> list[str]:
    summaries = []
    for p in paths:
        try:
            res = yaml.safe_load(p.read_text())
        except (OSError, yaml.YAMLError) as e:
            err(f"{p}: cannot read ({e})")
            continue
        rel = p.relative_to(ROOT) if p.is_relative_to(ROOT) else p
        probs = check_results(res, suites, str(data.get("version")), all_ids, str(rel))
        for e in probs:
            err(e)
        if not probs:
            if str(res["laws_version"]) != str(data.get("version")):
                print(f"note: {rel} is for Laws {res['laws_version']}; case ids checked only for {data.get('version')}")
            summaries.append(results_summary(res))
    return summaries


def main(argv: list[str]) -> int:
    data = yaml.safe_load((ROOT / "laws.yaml").read_text())
    all_ids = check_yaml(data) if isinstance(data, dict) else set()
    core_ids = {c["id"] for law in data.get("core", []) for c in law.get("clauses", [])}
    check_universal(data)
    langs = check_translations(data, core_ids)
    check_citation(data)
    if not errors:
        check_docs(data)
    suites, problems = parse_suites()
    if argv[:1] == ["--results"]:
        paths = [Path(a).resolve() for a in argv[1:]]
        if not paths:
            print("usage: python tools/validate.py --results FILE ...")
            return 2
        summaries = check_result_files(paths, data, suites, all_ids)
        if errors:
            print(f"FAIL: {len(errors)} problem(s)")
            for e in errors:
                print(f"  - {e}")
            return 1
        for s in summaries:
            print(f"OK: {s}")
        return 0
    cases = check_tests(all_ids, suites, problems)
    check_results_schema(suites)
    examples = sorted((ROOT / "tests" / "examples").glob("*.yaml"))
    check_result_files(examples, data, suites, all_ids)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    core = sum(len(law["clauses"]) for law in data["core"])
    prof = ", ".join(f"{p['key']} {len(p['clauses'])}" for p in data["profiles"])
    print(f"OK: vektra-laws {data['version']}: 5 Laws, {core} core clauses; profiles: {prof}; "
          f"{cases} conformance cases; {len(examples)} example results file(s); translations: {', '.join(['en (reference)'] + langs)}; "
          f"universal text; no guarantee words; citation in sync; docs in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
