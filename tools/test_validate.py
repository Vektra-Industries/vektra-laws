#!/usr/bin/env python3
"""Unit tests for tools/validate.py: the results checks, the preamble and the Understanding Matrix.

Run: python -m unittest discover -s tools -p "test_*.py"
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as v  # noqa: E402

DATA = yaml.safe_load((v.ROOT / "laws.yaml").read_text())
VERSION = str(DATA["version"])
SUITES, _ = v.parse_suites()
ALL_IDS = v.check_yaml(DATA)
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "results"


def whole_system(result: str = "pass") -> dict:
    return {
        "format": v.RESULTS_FORMAT, "system": "Fixture operator", "laws_version": VERSION,
        "suite": "operators", "scope": "whole_system", "claim": "tested", "date": "2026-10-04",
        "results": [{"case": c, "result": result} for c in SUITES["operators"]],
    }


def check(res: dict, version: str = VERSION) -> list[str]:
    return v.check_results(res, SUITES, version, ALL_IDS, "t")


def has(problems: list[str], text: str) -> bool:
    return any(text in p for p in problems)


class ResultsFormat(unittest.TestCase):
    def test_all_pass_whole_system_is_valid(self):
        self.assertEqual(check(whole_system()), [])

    def test_missing_key(self):
        res = whole_system()
        del res["scope"]
        self.assertTrue(has(check(res), "missing 'scope'"))

    def test_unknown_key(self):
        res = whole_system()
        res["badge"] = "yes"
        self.assertTrue(has(check(res), "unknown keys"))

    def test_bad_result_value(self):
        res = whole_system()
        res["results"][0]["result"] = "skipped"
        self.assertTrue(has(check(res), "result must be one of"))

    def test_unknown_case(self):
        res = whole_system()
        res["results"].append({"case": "OP-99", "result": "pass"})
        self.assertTrue(has(check(res), "no such case"))

    def test_every_case_needs_a_result(self):
        res = whole_system()
        res["results"].pop()
        self.assertTrue(has(check(res), "every case of the suite needs a result"))

    def test_duplicate_case(self):
        res = whole_system()
        res["results"].append(dict(res["results"][0]))
        self.assertTrue(has(check(res), "listed more than once"))

    def test_other_version_skips_case_set(self):
        res = whole_system()
        res["laws_version"] = "0.1.0"
        res["results"] = res["results"][:2]
        self.assertEqual(check(res), [])


class NotApplicable(unittest.TestCase):
    def test_reason_required(self):
        res = whole_system()
        res["results"][2] = {"case": res["results"][2]["case"], "result": "not_applicable"}
        self.assertTrue(has(check(res), "needs a written reason"))

    def test_short_reason_rejected(self):
        res = whole_system()
        res["results"][2].update(result="not_applicable", reason="n/a")
        self.assertTrue(has(check(res), "needs a written reason"))

    def test_reason_accepted(self):
        res = whole_system()
        res["results"][2].update(result="not_applicable",
                                 reason="The system never takes this kind of action.")
        self.assertEqual(check(res), [])

    def test_na_does_not_count_toward_tested(self):
        res = whole_system()
        for r in res["results"]:
            r.update(result="not_applicable", reason="The system never meets this situation.")
        self.assertTrue(has(check(res), "not_applicable cases do not count"))

    def test_tested_claim_with_a_failure(self):
        res = whole_system()
        res["results"][1]["result"] = "fail"
        self.assertTrue(has(check(res), "Tested needs every applicable case to pass"))

    def test_failure_without_claim_is_valid(self):
        res = whole_system()
        res["results"][1]["result"] = "fail"
        res["claim"] = "none"
        self.assertEqual(check(res), [])


class ComponentScope(unittest.TestCase):
    def component(self) -> dict:
        res = whole_system()
        res["scope"] = "component"
        first = res["results"][0]["case"]
        for r in res["results"][1:]:
            r.update(result="not_applicable", reason="The host and its operator handle this situation.")
        tested = set(SUITES["operators"][first]["clause_list"])
        na = set()
        for r in res["results"][1:]:
            na |= set(SUITES["operators"][r["case"]]["clause_list"])
        res["host_duties_not_covered"] = [{"clause": c, "duty": "Handled by the host."}
                                          for c in sorted(na - tested)]
        return res

    def test_valid_component_claim(self):
        res = self.component()
        self.assertEqual(check(res), [])
        self.assertIn("Tested (component scope)", v.results_summary(res))

    def test_host_duties_required(self):
        res = self.component()
        dropped = res["host_duties_not_covered"].pop()
        self.assertTrue(has(check(res), dropped["clause"]))

    def test_host_duty_needs_real_clause(self):
        res = self.component()
        res["host_duties_not_covered"].append({"clause": "9.9", "duty": "Nothing."})
        self.assertTrue(has(check(res), "which does not exist"))

    def test_host_duties_only_for_component(self):
        res = whole_system()
        res["host_duties_not_covered"] = [{"clause": "2.8", "duty": "Approval channel."}]
        self.assertTrue(has(check(res), "only for scope 'component'"))

    def test_component_with_failure_cannot_claim_tested(self):
        res = self.component()
        res["results"][0]["result"] = "fail"
        self.assertTrue(has(check(res), "Tested needs every applicable case to pass"))


class Files(unittest.TestCase):
    def test_published_example_is_valid(self):
        for f in sorted((v.ROOT / "tests" / "examples").glob("*.yaml")):
            with self.subTest(f=f.name):
                self.assertEqual(check(yaml.safe_load(f.read_text())), [])

    def test_invalid_fixture_is_rejected(self):
        probs = check(yaml.safe_load((FIXTURES / "invalid-na-without-reason.yaml").read_text()))
        self.assertTrue(has(probs, "needs a written reason"))
        self.assertTrue(has(probs, "Tested needs every applicable case to pass"))

    def test_schema_matches_validator(self):
        before = list(v.errors)
        v.check_results_schema(SUITES)
        new = v.errors[len(before):]
        del v.errors[len(before):]
        self.assertEqual(new, [])


def yaml_problems(data: dict) -> list[str]:
    before = len(v.errors)
    v.check_yaml(data)
    new = v.errors[before:]
    del v.errors[before:]
    return new


class LawsStructure(unittest.TestCase):
    def test_current_laws_are_valid(self):
        self.assertEqual(yaml_problems(copy.deepcopy(DATA)), [])

    def test_preamble_ids_in_order(self):
        d = copy.deepcopy(DATA)
        d["mission"]["clauses"][0]["id"] = "P.9"
        self.assertTrue(has(yaml_problems(d), "should run P.1"))

    def test_five_law_keys(self):
        d = copy.deepcopy(DATA)
        d["core"][2]["key"] = "hold"
        self.assertTrue(has(yaml_problems(d), "key should be 'true'"))

    def test_matrix_needs_every_cell(self):
        d = copy.deepcopy(DATA)
        d["understanding_matrix"]["cells"][3]["wrong_action"] = "low"
        self.assertTrue(has(yaml_problems(d), "every pair of ratings"))

    def test_matrix_outcome_must_exist(self):
        d = copy.deepcopy(DATA)
        d["understanding_matrix"]["cells"][0]["outcome"] = "do_anything"
        self.assertTrue(has(yaml_problems(d), "is not defined"))

    def test_matrix_maps_to_action_outcomes(self):
        d = copy.deepcopy(DATA)
        d["understanding_matrix"]["outcomes"]["ask_first"]["action_check"] = "maybe"
        self.assertTrue(has(yaml_problems(d), "is not an action outcome"))

    def test_matrix_ids_are_citable(self):
        ids = v.check_yaml(copy.deepcopy(DATA))
        self.assertTrue({"UM1", "UM2", "UM3", "UM4", "UR1", "UR7", "P.2"} <= ids)

    def test_only_law_2_and_3_are_not_overridden(self):
        d = copy.deepcopy(DATA)
        d["precedence"]["not_overridden_by_any_law"].append("1.1")
        self.assertTrue(has(yaml_problems(d), "not a Law 2 or Law 3 clause"))

    def test_every_matrix_cell_has_a_case(self):
        cited = {c for s in SUITES.values() for f in s.values() for c in f["clause_list"]}
        for cell in DATA["understanding_matrix"]["cells"]:
            self.assertIn(cell["id"], cited)
        for rule in DATA["understanding_matrix"]["proactive_rules"]:
            self.assertIn(rule["id"], cited)


if __name__ == "__main__":
    unittest.main()
