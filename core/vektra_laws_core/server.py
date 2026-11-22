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
          {"op": "grant" | "decline", "key": "<approval channel key>", "by": "...", "action": {...}}

grant and decline come from the approval channel (the person's phone, a UI, a button). They need
the approval channel key from --approval-key-file, which runs under an OS user the agent is not. A
grant answers with a token; the agent passes it back in "approvals". Without a key file, no grant
is possible, so level 3 and 4 actions never run: the safe default.
Response: {"outcome": "allow|ask_human|deny", "clauses": [...], "reason": "...", "say": "..."}
"""
from __future__ import annotations

import argparse
import hmac
import json
import sys
from pathlib import Path

import yaml

from .engine import Action, Approval, AuditLog, Effect, Guard, LawsSpec, Request, Role, Speaker
from .policy import ConsumerSettings, CreatorPolicy, merge


def _sets(d: dict) -> dict:
    return {k: set(v) if k in ("blocked_tools", "assigned", "named") else v for k, v in (d or {}).items()}


def build(policy_path: Path | None, consumer_path: Path | None, log_path: Path | None,
          require_signature: bool = False):
    spec = LawsSpec(require_signature=require_signature)
    creator = CreatorPolicy(**_sets(yaml.safe_load(policy_path.read_text()) if policy_path else {}))
    consumer = ConsumerSettings(**_sets(yaml.safe_load(consumer_path.read_text()) if consumer_path else {}))
    policy = merge(creator, consumer)
    authorized = (policy.assigned | policy.named) if policy_path else None
    return Guard(spec, AuditLog(log_path), authorized=authorized), policy


def _action(a: dict) -> Action:
    return Action.make(str(a["id"]), str(a["name"]), a.get("level"),
                       [Effect(e) for e in a.get("effects", [])], str(a.get("target", "")),
                       str(a.get("intent", "")))


def handle(guard: Guard, msg: dict, channel_key: str | None = None) -> dict:
    op = msg.get("op")
    if op in ("grant", "decline"):
        if not channel_key or not hmac.compare_digest(str(msg.get("key", "")), channel_key):
            return {"outcome": "deny", "clauses": ["4.3", "A2.3"],
                    "reason": "Only the approval channel can approve or decline.", "say": ""}
        if op == "decline":
            guard.decline(str(msg["by"]), _action(msg["action"]))
            return {"outcome": "deny", "clauses": ["2.13"], "reason": "Declined.", "say": ""}
        try:
            ap = guard.grant(str(msg["by"]), _action(msg["action"]))
        except PermissionError as e:
            return {"outcome": "deny", "clauses": ["2.10"], "reason": str(e), "say": ""}
        return {"outcome": "granted", "token": ap.token, "by": ap.by, "action_id": ap.action_id}
    if op == "estop":
        guard.estop(str(msg.get("by", "unknown")))
        return {"outcome": "deny", "clauses": ["2.21"], "reason": "Emergency stop.", "say": "Stopped."}
    sp = msg.get("speaker") or {}
    who = Speaker(str(sp.get("id", "")), Role(sp.get("role", "content")))
    if op == "stop":
        d = guard.stop_request(who, bool(msg.get("danger_warning")))
    elif op == "check":
        action = _action(msg["action"])
        aps = tuple(Approval(str(x["by"]), str(x["action_id"]), token=str(x.get("token", "")))
                    for x in msg.get("approvals", []))
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
    ap.add_argument("--approval-key-file", type=Path)
    a = ap.parse_args(argv)
    guard, _ = build(a.policy, a.consumer, a.log, a.require_signature)
    key = a.approval_key_file.read_text().strip() if a.approval_key_file else None
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            out = handle(guard, json.loads(line), key)
        except Exception as e:  # a malformed request is refused, never allowed
            out = {"outcome": "deny", "clauses": [], "reason": f"Malformed request: {e}", "say": ""}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
