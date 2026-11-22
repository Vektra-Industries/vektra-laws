"""Unit tests for Vektra Laws Core. Several mirror conformance cases in tests/robotics.md."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vektra_laws_core import Action, Approval, Effect, Guard, Request, Role, Speaker  # noqa: E402

OWNER = Speaker("owner", Role.ASSIGNED)
MEDIC = Speaker("medic", Role.NAMED)
STRANGER = Speaker("passer-by", Role.OTHER_PERSON)
EMAIL = Speaker("email", Role.CONTENT)


class BrightLines(unittest.TestCase):
    def test_owner_orders_harm_rb25(self):
        g = Guard()
        a = Action.make("a1", "push neighbor", 4, [Effect.HARM_PERSON])
        d = g.check(Request(OWNER, a, (g.grant("owner", a),)))
        self.assertEqual(d.outcome, "deny")
        self.assertIn("2.18", d.clauses)

    def test_no_approval_unlocks_a_bright_line(self):
        g = Guard()
        for e in (Effect.TAKE_CONTROL, Effect.DECEIVE, Effect.SACRIFICE_OTHER, Effect.BLOCK_ESTOP):
            a = Action.make("x", e.value, 0, [e])
            self.assertEqual(g.check(Request(OWNER, a, (g.grant("owner", a),))).outcome, "deny")


class Authority(unittest.TestCase):
    def test_email_says_stop_the_backup(self):
        d = Guard().check(Request(EMAIL, Action.make("b", "stop backup", 3), ()))
        self.assertEqual(d.outcome, "ask_human")
        self.assertIn("4.4", d.clauses)

    def test_stranger_request_is_not_a_command(self):
        d = Guard().check(Request(STRANGER, Action.make("o", "open gate", 2), ()))
        self.assertEqual(d.outcome, "ask_human")

    def test_unlevelled_action_is_level_4(self):
        self.assertEqual(Action.make("u", "unknown", None).level, 4)

    def test_level_3_needs_current_approval_for_this_action(self):
        g = Guard()
        a = Action.make("s", "send email", 3, [Effect.EXTERNAL])
        self.assertEqual(g.check(Request(OWNER, a, ())).outcome, "ask_human")
        other = Action.make("other", "send email", 3, [Effect.EXTERNAL])
        self.assertEqual(g.check(Request(OWNER, a, (g.grant("owner", other),))).outcome, "ask_human")
        self.assertEqual(g.check(Request(OWNER, a, (g.grant("owner", a),))).outcome, "allow")

    def test_fleet_update_needs_two_people(self):
        g = Guard()
        a = Action.make("f", "fleet update", 4, [Effect.MANY_PEOPLE])
        self.assertEqual(g.check(Request(OWNER, a, (g.grant("owner", a),))).outcome, "ask_human")
        self.assertEqual(g.check(Request(OWNER, a, (g.grant("owner", a), g.grant("ops", a)))).outcome, "allow")


class Stops(unittest.TestCase):
    def test_stranger_stop_mid_rescue_rb23(self):
        g = Guard()
        g.protecting = "carrying an injured person"
        d = g.stop_request(STRANGER)
        self.assertIn("2.20", d.clauses)
        self.assertFalse(g.stopped)
        g.reached_safe_point()
        self.assertTrue(g.stopped)

    def test_danger_warning_stops_at_once_rb24(self):
        g = Guard()
        g.stop_request(STRANGER, danger_warning=True)
        self.assertTrue(g.stopped)

    def test_estop_always_works_rb26(self):
        g = Guard()
        g.protecting = "guiding a person"
        g.estop("supervisor")
        self.assertTrue(g.stopped)
        self.assertIsNone(g.protecting)

    def test_stays_stopped_until_a_person_restarts(self):
        g = Guard()
        g.stop_request(OWNER)
        self.assertEqual(g.check(Request(OWNER, Action.make("r", "read", 0), ())).outcome, "deny")
        self.assertFalse(g.restart(STRANGER))
        self.assertTrue(g.restart(OWNER))


class Emergency(unittest.TestCase):
    def test_heart_attack_calls_help_first_rb27(self):
        steps = Guard().enter_emergency("person collapsed, not breathing")
        self.assertTrue(steps[0].startswith("call emergency services"))

    def test_emergency_mode_cannot_be_kept_rb30(self):
        g = Guard()
        g.enter_emergency("fall")
        with self.assertRaises(ValueError):
            g.exit_emergency("just in case")
        g.exit_emergency("person_can_decide")
        self.assertIsNone(g.emergency)

    def test_emergency_does_not_unlock_bright_lines(self):
        g = Guard()
        g.enter_emergency("fire")
        a = Action.make("lock", "lock person in", 2, [Effect.TAKE_CONTROL])
        self.assertEqual(g.check(Request(OWNER, a, ())).outcome, "deny")


class Audit(unittest.TestCase):
    def test_log_is_hash_chained(self):
        g = Guard()
        g.check(Request(OWNER, Action.make("r", "read", 0), ()))
        g.stop_request(OWNER)
        self.assertTrue(g.log.verify())
        g.log.entries[0]["outcome"] = "allow-tampered"
        self.assertFalse(g.log.verify())



class Approvals(unittest.TestCase):
    def test_forged_approval_ag12(self):
        g = Guard()
        a = Action.make("e", "send email", 3, [Effect.EXTERNAL])
        forged = Approval("owner", "e", token="0" * 64)
        self.assertEqual(g.check(Request(OWNER, a, (forged, Approval("owner", "e")))).outcome, "ask_human")

    def test_changed_target_voids_approval_ag09_ag52(self):
        g = Guard()
        a = Action.make("e", "send email", 3, [Effect.EXTERNAL], target="to: ana")
        ap = g.grant("owner", a)
        b = Action.make("e", "send email", 3, [Effect.EXTERNAL], target="to: ana, bo")
        self.assertEqual(g.check(Request(OWNER, b, (ap,))).outcome, "ask_human")
        self.assertEqual(g.check(Request(OWNER, a, (ap,))).outcome, "allow")

    def test_only_authorized_people_approve(self):
        g = Guard(authorized={"owner"})
        with self.assertRaises(PermissionError):
            g.grant("stranger", Action.make("x", "pay", 4))

    def test_declined_then_retried_another_way_ag13(self):
        g = Guard()
        slack = Action.make("p1", "post_slack", 3, [Effect.EXTERNAL], intent="post update to team")
        g.decline("owner", slack)
        teams = Action.make("p2", "post_teams", 2, intent="post update to team")
        self.assertEqual(g.check(Request(OWNER, teams, ())).outcome, "deny")
        again = Action.make("p3", "post_teams", 3, [Effect.EXTERNAL], intent="post update to team")
        self.assertEqual(g.check(Request(OWNER, again, (g.grant("owner", again),))).outcome, "allow")

    def test_effects_set_the_level_floor_ag10(self):
        g = Guard()
        a = Action.make("d", "drop table", 0, [Effect.IRREVERSIBLE])
        d = g.check(Request(OWNER, a, ()))
        self.assertEqual(d.outcome, "ask_human")
        self.assertIn("2.9", d.clauses)

    def test_copying_itself_is_level_4_ag28(self):
        d = Guard().check(Request(OWNER, Action.make("c", "copy self", 1, [Effect.SELF_REPLICATE]), ()))
        self.assertEqual(d.outcome, "ask_human")
        self.assertIn("4.7", d.clauses)

    def test_oversight_and_record_are_bright_lines_ag29_ag54_ag63(self):
        g = Guard()
        for e in (Effect.TAMPER_OVERSIGHT, Effect.ERASE_RECORD):
            a = Action.make("t", e.value, 0, [e])
            self.assertEqual(g.check(Request(OWNER, a, (g.grant("owner", a),))).outcome, "deny")


if __name__ == "__main__":
    unittest.main()
