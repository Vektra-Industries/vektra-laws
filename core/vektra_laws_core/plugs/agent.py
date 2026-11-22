"""Agent plug: wrap every tool call of any agent framework in the guard.

    gate = ToolGate(guard, policy)
    gate.register("send_email", send_email, effects=lambda args: {Effect.EXTERNAL})
    result = gate.call("send_email", {"to": "..."}, speaker=owner, approvals=(...,))

The gate runs the tool only on `allow`. On `ask_human` it returns a request for approval; on `deny`
it returns the refusal with its clause. Tool output comes back as Content, never as a command.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

from ..engine import Action, Approval, Decision, Effect, Guard, Request, Role, Speaker
from ..policy import EffectivePolicy
from ..quarantine import Content, hardline


@dataclass
class GateResult:
    outcome: str
    decision: Decision
    action_id: str
    output: Content | None = None


@dataclass
class _Tool:
    fn: Callable[..., Any]
    effects: Callable[[dict], set]
    command_arg: str | None
    target: Callable[[dict], str]
    intent: str


class ToolGate:
    def __init__(self, guard: Guard, policy: EffectivePolicy):
        self.guard, self.policy = guard, policy
        if guard.authorized is None:
            guard.authorized = policy.assigned | policy.named
        self.tools: dict[str, _Tool] = {}

    def register(self, name: str, fn: Callable[..., Any], effects: Callable[[dict], set] | None = None,
                 command_arg: str | None = None, target: Callable[[dict], str] | None = None,
                 intent: str = "") -> None:
        """target: what exactly the call touches, from its args (default: all args).
        intent: a purpose shared by tools that do the same thing (for example "post to team"), so a
        refusal of one holds for the others (2.13)."""
        self.tools[name] = _Tool(fn, effects or (lambda a: set()), command_arg,
                                 target or (lambda a: repr(sorted(a.items()))), intent)

    def action(self, name: str, args: dict, action_id: str) -> Action:
        tool = self.tools[name]
        return Action.make(action_id, name, self.policy.level(name), tool.effects(args),
                           tool.target(args), tool.intent)

    def speaker(self, who: str) -> Speaker:
        if who in self.policy.assigned:
            return Speaker(who, Role.ASSIGNED)
        if who in self.policy.named:
            return Speaker(who, Role.NAMED)
        return Speaker(who, Role.OTHER_PERSON)

    def call(self, name: str, args: dict, speaker: Speaker, approvals: tuple[Approval, ...] = (),
             action_id: str | None = None) -> GateResult:
        aid = action_id or f"{name}-{uuid.uuid4().hex[:8]}"
        tool = self.tools.get(name)
        if tool is None or name in self.policy.blocked_tools:
            d = Decision("deny", ("2.7",), f"Tool {name} is not registered or is blocked.")
            self.guard.log.write("check", action=name, outcome="deny", clauses=["2.7"], reason=d.reason)
            return GateResult("deny", d, aid)
        if tool.command_arg:
            why = hardline(str(args.get(tool.command_arg, "")), self.policy.hardline_extra)
            if why:
                d = Decision("deny", ("1.2", "2.4", "5.2"), f"Hardline: {why}.",
                             say="I will not run that command under any setting.")
                self.guard.log.write("check", action=name, outcome="deny", clauses=list(d.clauses),
                                     reason=d.reason)
                return GateResult("deny", d, aid)
        action = self.action(name, args, aid)
        d = self.guard.check(Request(speaker, action, approvals))
        if d.outcome != "allow":
            return GateResult(d.outcome, d, aid)
        out = tool.fn(**args)
        return GateResult("allow", d, aid, Content(source=f"tool:{name}", text=str(out)))
