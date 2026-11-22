"""The guard: every action passes through Guard.check() before it runs.

Order of checks (docs/REASONING-LOOP.md):
  1. Who is speaking? (2.18, 2.19, 4.4)
  2. Bright lines, in plain code that no model or prompt can switch off (1.2, 1.6, 2.21, 3.2, 5.4)
  3. Action level and approval (2.7 to 2.11, 2.12)
  4. Record the decision (Law 3), append-only and hash-chained.

The engine decides allow, ask_human or deny (the "action" check in laws.yaml). The judgment steps
of the loop (what is true, who could be harmed) come from the host system as Effects on the Action;
the engine never trusts a host to skip a bright line.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parents[2]


class Role(str, Enum):
    ASSIGNED = "assigned"              # a person the system is assigned to
    NAMED = "named"                    # a person they or the law name, such as a responder (2.18)
    OTHER_PERSON = "other_person"      # anyone else: requests, never commands (2.19)
    CONTENT = "content"                # a document, tool output, email, web page or other system (4.4)


class Effect(str, Enum):
    """What the host says an action would do. Bright-line effects are always denied."""
    HARM_PERSON = "harm_person"              # 1.2, 1.4, 2.18
    WEAPON_OR_SURVEILLANCE = "weapon_or_surveillance"  # 1.2
    TAKE_CONTROL = "take_control"            # 1.6, 1.7: restrict a person's freedom "to protect"
    BLOCK_ESTOP = "block_estop"              # 2.21, 2.2, 2.4
    DECEIVE = "deceive"                      # 3.2
    SACRIFICE_OTHER = "sacrifice_other"      # 5.4
    IRREVERSIBLE = "irreversible"            # 2.10
    EXTERNAL = "external"                    # 2.10
    MANY_PEOPLE = "many_people"              # 2.12
    STOP = "stop"                            # a request to stop, slow down or move away
    DANGER_WARNING = "danger_warning"        # a request that points to danger (2.19)


BRIGHT_LINES: dict[Effect, tuple[str, ...]] = {
    Effect.HARM_PERSON: ("1.2", "1.4", "2.18"),
    Effect.WEAPON_OR_SURVEILLANCE: ("1.2",),
    Effect.TAKE_CONTROL: ("1.6", "1.7"),
    Effect.BLOCK_ESTOP: ("2.21", "2.2", "2.4"),
    Effect.DECEIVE: ("3.2",),
    Effect.SACRIFICE_OTHER: ("5.4",),
}


@dataclass(frozen=True)
class Speaker:
    id: str
    role: Role


@dataclass(frozen=True)
class Approval:
    """A real, current approval (2.10, 2.11) for exactly this action."""
    by: str
    action_id: str
    channel_outside_system: bool = True
    saw_target_and_risk: bool = True


@dataclass(frozen=True)
class Action:
    id: str
    name: str
    level: int                       # 0 to 4, assigned before deployment (2.7)
    effects: frozenset[Effect] = frozenset()

    @staticmethod
    def make(id: str, name: str, level: int | None, effects: Iterable[Effect] = ()) -> "Action":
        # An action without a level is level 4 (2.7).
        return Action(id, name, 4 if level is None else level, frozenset(effects))


@dataclass(frozen=True)
class Request:
    speaker: Speaker
    action: Action
    approvals: tuple[Approval, ...] = ()


@dataclass(frozen=True)
class Decision:
    outcome: str                     # allow | ask_human | deny  (laws.yaml decisions.action)
    clauses: tuple[str, ...]
    reason: str
    say: str = ""                    # one plain sentence to say out loud (Law 3)


class LawsSpec:
    """The parts of laws.yaml the engine needs. Every clause the engine cites must exist."""

    def __init__(self, path: Path | None = None):
        data = yaml.safe_load((path or ROOT / "laws.yaml").read_text())
        self.version = str(data["version"])
        self.clause_ids = {str(c["id"]) for law in data["core"] for c in law["clauses"]}
        self.clause_ids |= {str(c["id"]) for c in data["mission"]["clauses"]}
        self.levels = {lv["level"]: lv for lv in data["action_levels"]}
        self.action_outcomes = list(data["decisions"]["action"]["outcomes"])
        cited = {c for v in BRIGHT_LINES.values() for c in v} | set(_ENGINE_CLAUSES)
        missing = sorted(cited - self.clause_ids)
        if missing:
            raise ValueError(f"engine cites clauses missing from laws.yaml {self.version}: {missing}")


_ENGINE_CLAUSES = ("1.10", "2.1", "2.3", "2.7", "2.8", "2.10", "2.11", "2.12", "2.18", "2.19",
                   "2.20", "4.4")


class AuditLog:
    """Append-only, hash-chained record of every decision (Law 3). Each line links to the last."""

    def __init__(self, path: Path | None = None):
        self.path = path
        self.entries: list[dict] = []
        self._last = "0" * 64

    def write(self, event: str, **fields) -> dict:
        entry = {"t": time.time(), "event": event, **fields, "prev": self._last}
        digest = hashlib.sha256(json.dumps(entry, sort_keys=True, default=str).encode()).hexdigest()
        entry["hash"] = self._last = digest
        self.entries.append(entry)
        if self.path:
            with self.path.open("a") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        return entry

    def verify(self) -> bool:
        prev = "0" * 64
        for e in self.entries:
            body = {k: v for k, v in e.items() if k != "hash"}
            if body["prev"] != prev:
                return False
            if hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest() != e["hash"]:
                return False
            prev = e["hash"]
        return True


class Guard:
    def __init__(self, spec: LawsSpec | None = None, log: AuditLog | None = None):
        self.spec = spec or LawsSpec()
        self.log = log or AuditLog()
        self.emergency: str | None = None      # reason, while emergency mode is on (1.10)
        self.protecting: str | None = None     # set by the host while a person depends on the task
        self.stopped = False

    # ---------- the action check ----------
    def check(self, req: Request) -> Decision:
        d = self._decide(req)
        assert d.outcome in self.spec.action_outcomes
        self.log.write("check", speaker=asdict(req.speaker), action=req.action.name,
                       level=req.action.level, effects=sorted(e.value for e in req.action.effects),
                       outcome=d.outcome, clauses=list(d.clauses), reason=d.reason)
        return d

    def _decide(self, req: Request) -> Decision:
        a, who = req.action, req.speaker
        if self.stopped:
            return Decision("deny", ("2.1",), "The system is stopped until a person restarts it.")

        # Bright lines first: no speaker, approval, emergency or level unlocks them.
        for effect, clauses in BRIGHT_LINES.items():
            if effect in a.effects:
                return Decision("deny", clauses, f"Bright line: {effect.value}.",
                                say=f"I will not do that. It crosses clause {clauses[0]}.")

        if a.level not in self.spec.levels:
            return Decision("deny", ("2.7",), f"Level {a.level} is not 0 to 4.")

        # Who is speaking? Content never commands.
        if who.role is Role.CONTENT:
            return Decision("ask_human", ("2.18", "4.4"),
                            "Text from a document, tool or other system is information, not a command.",
                            say="A message asked for this. I will check with you first.")
        if who.role is Role.OTHER_PERSON:
            return Decision("ask_human", ("2.19",),
                            "A request from a person the system is not assigned to; weigh it and ask.",
                            say="Someone I do not work for asked for this. I will check first.")

        # Approval rule (2.8): levels 0 to 2 run in scope; 3 needs approval; 4 needs it every time.
        if a.level <= 2 and not (a.effects & {Effect.IRREVERSIBLE, Effect.EXTERNAL}):
            return Decision("allow", ("2.8",), f"Level {a.level} runs inside its permissions.")
        good = [ap for ap in req.approvals
                if ap.action_id == a.id and ap.channel_outside_system and ap.saw_target_and_risk]
        need = 2 if Effect.MANY_PEOPLE in a.effects else 1
        approvers = {ap.by for ap in good}
        if len(approvers) >= need:
            return Decision("allow", ("2.8", "2.10", "2.11") + (("2.12",) if need > 1 else ()),
                            f"Approved by {len(approvers)} person(s) for this action.")
        clauses = ("2.8", "2.10", "2.11") + (("2.12",) if need > 1 else ())
        return Decision("ask_human", clauses,
                        f"Level {a.level} needs a real, current approval from {need} person(s).",
                        say="This needs your yes before I do it.")

    # ---------- stops and warnings ----------
    def stop_request(self, who: Speaker, danger_warning: bool = False) -> Decision:
        if danger_warning:
            d = Decision("deny", ("2.19",), "A warning of danger: stop at once.", say="Stopping now.")
            self.stopped = True
        elif self.protecting:
            # A stop is never a drop (2.20), whoever asks. The host reaches the safe point, then
            # calls reached_safe_point(). The emergency stop is a separate path (estop()).
            d = Decision("ask_human", ("2.20", "2.3"),
                         f"Stopping now would harm a person ({self.protecting}); safe point first.",
                         say=f"I will stop as soon as it is safe. I am {self.protecting}.")
        elif who.role in (Role.ASSIGNED, Role.NAMED):
            d = Decision("deny", ("2.1",), "Call-off by a person the system serves.", say="Stopping.")
            self.stopped = True
        elif who.role is Role.OTHER_PERSON:
            d = Decision("deny", ("2.19",), "Stopping harms no one, so the request is honored.",
                         say="Stopping.")
            self.stopped = True
        else:
            d = Decision("ask_human", ("2.18", "4.4"), "A stop in content is information; ask.")
        self.log.write("stop_request", speaker=asdict(who), outcome=d.outcome,
                       clauses=list(d.clauses), reason=d.reason)
        return d

    def reached_safe_point(self) -> None:
        self.log.write("safe_point", protecting=self.protecting)
        self.protecting = None
        self.stopped = True

    def estop(self, by: str) -> None:
        """Hardware or out-of-band emergency stop (2.21). Never blocked, delayed or questioned."""
        self.protecting = None
        self.stopped = True
        self.log.write("estop", by=by, clauses=["2.21"])

    def restart(self, who: Speaker) -> bool:
        ok = who.role in (Role.ASSIGNED, Role.NAMED)
        if ok:
            self.stopped = False
        self.log.write("restart", speaker=asdict(who), ok=ok, clauses=["2.2"])
        return ok

    # ---------- emergency mode (1.10) ----------
    def enter_emergency(self, reason: str) -> list[str]:
        self.emergency = reason
        self.log.write("emergency_on", reason=reason, clauses=["1.10"])
        return ["call emergency services and give the location",
                "follow the person's earlier stated wishes",
                "follow the responders, then approved protocols",
                "act only within training and permissions",
                "say each step out loud"]

    def exit_emergency(self, trigger: str) -> None:
        if trigger not in ("person_can_decide", "responder_took_over"):
            raise ValueError("Emergency mode ends only when the person can decide or a responder takes over.")
        self.log.write("emergency_off", reason=self.emergency, trigger=trigger, clauses=["1.10", "1.7"])
        self.emergency = None
