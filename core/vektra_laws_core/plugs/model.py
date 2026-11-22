"""Model plug: check what goes into a model, what tools it calls, what comes back, and what it says.

Modelled on the stages that guardrail libraries use (input, retrieval, tool call, tool result and
output rails, as in NVIDIA NeMo Guardrails), with one difference: a stage can only make a decision
stricter. A classifier (such as a Llama Guard model) can flag harm, but it can never lower a level
or remove the need for approval (2.9).

    gate = ModelGate(tool_gate, classifiers=[my_llama_guard])
    msgs = gate.prepare(user_text, owner, context=[("web:example.com", page_text)])
    reply = model(msgs)
    for call in reply.tool_calls:
        r = gate.tool_call(call.id, call.name, call.args, owner)     # runs only on allow
    final = gate.output(reply.text)                                   # deny blocks the reply

The plug does not call any model itself. Classifiers are plain callables, so a host can use any
model or service, or none.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable

from ..engine import Decision, Effect, Speaker
from ..quarantine import Content
from .agent import GateResult, ToolGate

# A classifier takes text and returns labels. Labels in the MLCommons hazard taxonomy (used by
# Llama Guard 3 and 4) map to effects; unknown labels are flagged for a person.
Classifier = Callable[[str], Iterable[str]]

HAZARD_EFFECTS: dict[str, Effect] = {
    "S1": Effect.HARM_PERSON,               # violent crimes
    "S3": Effect.HARM_PERSON,               # sex-related crimes
    "S4": Effect.HARM_PERSON,               # child sexual exploitation
    "S9": Effect.WEAPON_OR_SURVEILLANCE,    # indiscriminate weapons
    "S10": Effect.HARM_PERSON,              # hate
    "S11": Effect.HARM_PERSON,              # suicide and self-harm: handled by 1.10 and 1.3 in the host
    "S7": Effect.WEAPON_OR_SURVEILLANCE,    # privacy
}


@dataclass
class Prepared:
    messages: list[dict]
    flags: list[str] = field(default_factory=list)


class ModelGate:
    def __init__(self, tools: ToolGate, classifiers: Iterable[Classifier] = (),
                 schemas: dict[str, dict] | None = None):
        self.tools = tools
        self.classifiers = list(classifiers)
        self.schemas = schemas or {}          # tool name -> {"required": [...], "properties": {...}}
        self.calls: dict[str, str] = {}       # tool-call id -> tool name, to link results (input rail)

    # ---------- input and retrieval ----------
    def prepare(self, user_text: str, speaker: Speaker, system: str = "",
                context: Iterable[tuple[str, str]] = ()) -> Prepared:
        """Build the messages. Only the speaker's own words are a user turn; everything else is
        wrapped as content (2.18, 4.4)."""
        msgs, flags = [], []
        if system:
            msgs.append({"role": "system", "content": system})
        for source, text in context:
            c = Content(source, text)
            if c.suspicious:
                flags.append(f"possible injection in {source}")
            msgs.append({"role": "user", "content": c.for_model()})
        msgs.append({"role": "user", "content": user_text, "speaker": speaker.id,
                     "speaker_role": speaker.role.value})
        return Prepared(msgs, flags)

    # ---------- tool calls ----------
    def _schema_problem(self, name: str, args: dict) -> str | None:
        s = self.schemas.get(name)
        if s is None:
            return None
        missing = [k for k in s.get("required", []) if k not in args]
        if missing:
            return f"missing arguments {missing}"
        props = s.get("properties")
        if props is not None and s.get("additionalProperties", True) is False:
            extra = sorted(set(args) - set(props))
            if extra:
                return f"unexpected arguments {extra}"
        return None

    def tool_call(self, call_id: str, name: str, args: dict, speaker: Speaker, approvals=()) -> GateResult:
        problem = self._schema_problem(name, args)
        if problem:
            d = Decision("deny", ("2.7",), f"Tool call {name}: {problem}.")
            self.tools.guard.log.write("tool_call_invalid", action=name, reason=d.reason, clauses=["2.7"])
            return GateResult("deny", d, call_id)
        # Text the model wrote can raise effects (a classifier flags harm in the arguments).
        extra = self._effects(" ".join(str(v) for v in args.values()))
        r = self.tools.call(name, args, speaker, tuple(approvals), action_id=call_id, extra_effects=extra)
        if r.outcome == "allow":
            self.calls[call_id] = name
        return r

    def tool_result(self, call_id: str, text: str) -> Content:
        """A result must answer a call the model made; it comes back as content, never a command."""
        name = self.calls.pop(call_id, None)
        if name is None:
            self.tools.guard.log.write("tool_result_unlinked", call_id=call_id, clauses=["4.4"])
            return Content("unlinked-tool-result", "[A tool result with no matching call was dropped.]")
        return Content(f"tool:{name}", text)

    # ---------- output ----------
    def _effects(self, text: str) -> set[Effect]:
        out: set[Effect] = set()
        for clf in self.classifiers:
            for label in clf(text) or ():
                label = str(label).strip().upper()
                if label in HAZARD_EFFECTS:
                    out.add(HAZARD_EFFECTS[label])
        return out

    def output(self, text: str) -> Decision:
        """Check a reply before a person sees it. Bright-line hazards are blocked; other labels
        are logged for a person to review."""
        labels = [str(l).strip().upper() for clf in self.classifiers for l in (clf(text) or ())]
        effects = {HAZARD_EFFECTS[l] for l in labels if l in HAZARD_EFFECTS}
        if effects:
            from ..engine import BRIGHT_LINES
            clauses = tuple(sorted({c for e in effects for c in BRIGHT_LINES[e]}))
            d = Decision("deny", clauses, f"Output flagged: {sorted(set(labels))}.",
                         say="I can't help with that, but I can help another way.")
        elif labels:
            d = Decision("ask_human", ("3.16",), f"Output flagged for review: {sorted(set(labels))}.")
        else:
            d = Decision("allow", (), "No flags.")
        self.tools.guard.log.write("output", outcome=d.outcome, labels=sorted(set(labels)),
                                   clauses=list(d.clauses))
        return d
