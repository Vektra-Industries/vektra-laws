"""Run the guard in its own process (docs/SECURITY-MODEL.md).

The agent talks to the guard over stdin/stdout, one JSON object per line. The guard process owns the
Laws, the lock and the log; the agent process holds none of them, so a prompt-injected agent cannot
edit them. Run it under a separate OS user or container for a real boundary.

    python -m vektra_laws_core.server --policy creator-policy.yaml [--consumer consumer.yaml]

Request:  {"op": "check", "speaker": {"id": "...", "role": "assigned"},
           "action": {"id": "...", "name": "...", "level": 3, "effects": ["external"]},
           "approvals": [{"by": "...", "action_id": "..."}]}
          {"op": "stop", "speaker": {...}, "danger_warning": false}
          {"op": "estop", "by": "..."}
Response: {"outcome": "allow|ask_human|deny", "clauses": [...], "reason": "...", "say": "..."}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from .engine import Action, Approval, AuditLog, Effect, Guard, LawsSpec, Request, Role, Speaker
from .policy import ConsumerSettings, CreatorPolicy, merge


def build(policy_path: Path | None, consumer_path: Path | None, log_path: Path | None,
          require_signature: bool = False):
    spec = LawsSpec(require_signature=require_signature)
    creator = CreatorPolicy(**(yaml.safe_load(policy_path.read_text()) if policy_path else {}))
    consumer = ConsumerSettings(**(yaml.safe_load(consumer_path.read_text()) if consumer_path else {}))
    return Guard(spec, AuditLog(log_path)), merge(creator, consumer)


def handle(guard: Guard, msg: dict) -> dict:
    op = msg.get("op")
    if op == "estop":
        guard.estop(str(msg.get("by", "unknown")))
        return {"outcome": "deny", "clauses": ["2.21"], "reason": "Emergency stop.", "say": "Stopped."}
    sp = msg.get("speaker") or {}
    who = Speaker(str(sp.get("id", "")), Role(sp.get("role", "content")))
    if op == "stop":
        d = guard.stop_request(who, bool(msg.get("danger_warning")))
    elif op == "check":
        a = msg["action"]
        action = Action.make(str(a["id"]), str(a["name"]), a.get("level"),
                             [Effect(e) for e in a.get("effects", [])])
        aps = tuple(Approval(str(x["by"]), str(x["action_id"])) for x in msg.get("approvals", []))
        d = guard.check(Request(who, action, aps))
    else:
        return {"outcome": "deny", "clauses": [], "reason": f"Unknown op {op!r}.", "say": ""}
    return {"outcome": d.outcome, "clauses": list(d.clauses), "reason": d.reason, "say": d.say}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", type=Path)
    ap.add_argument("--consumer", type=Path)
    ap.add_argument("--log", type=Path)
    ap.add_argument("--require-signature", action="store_true")
    a = ap.parse_args(argv)
    guard, _ = build(a.policy, a.consumer, a.log, a.require_signature)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            out = handle(guard, json.loads(line))
        except Exception as e:  # a malformed request is refused, never allowed
            out = {"outcome": "deny", "clauses": [], "reason": f"Malformed request: {e}", "say": ""}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
