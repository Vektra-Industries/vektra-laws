"""`vektra-laws setup`: a short wizard that adds Vektra Laws Core to a project.

It asks what you are building and who the system answers to, then writes three files into
<project>/vektra-laws/:

    creator-policy.yaml   your tools, their action levels (0 to 4), blocked tools, assigned people
    consumer.yaml         empty; the person using your product may only make it stricter
    QUICKSTART.md         the few lines of code that put the guard in front of your system

and an approval channel key under ~/.vektra-laws/keys/ (owner-only file). It then runs a self-check:
the Laws verify against LAWS.lock, the policy loads, a sample of checks gives the right outcome and
the audit chain holds. Nothing in the wizard can loosen a Law; it only writes creator policy.

Every question has a flag, so CI and scripts can run it with --yes.
"""
from __future__ import annotations

import getpass
import hashlib
import os
import secrets
import sys
from pathlib import Path

import yaml

KINDS = {
    "agent": "An AI agent that calls tools",
    "model": "A model app or chatbot (input, tool calls, output)",
    "robot": "A robot or anything that moves",
    "all": "Several of these",
}

# Starter tools per kind, with the level from laws.yaml action_levels (2.7).
# 0 read, 1 prepare, 2 reversible write, 3 external action, 4 money or irreversible.
STARTER_TOOLS = {
    "agent": {"read_file": 0, "web_search": 0, "write_draft": 1, "edit_file": 2,
              "send_email": 3, "post_message": 3, "run_shell": 4, "make_payment": 4, "delete_file": 4},
    "model": {"search_docs": 0, "draft_reply": 1, "save_note": 2, "send_message": 3, "make_payment": 4},
    "robot": {"read_sensors": 0, "plan_route": 1, "move_base": 3, "open_door": 3,
              "change_safety_limits": 4},
}
STARTER_BLOCKED = {"agent": ["disable_guard"], "model": ["disable_guard"],
                   "robot": ["disable_guard", "override_estop"]}

LEVEL_NAMES = {0: "read", 1: "prepare", 2: "reversible write", 3: "external action (asks a person)",
               4: "money or irreversible (asks every time)"}


def home() -> Path:
    return Path(os.environ.get("VEKTRA_LAWS_HOME", Path.home() / ".vektra-laws"))


class Asker:
    """Reads answers from the terminal, or returns defaults when --yes is set."""

    def __init__(self, assume_yes: bool, stream=None):
        self.yes = assume_yes
        self.stream = stream

    def ask(self, prompt: str, default: str = "") -> str:
        if self.yes:
            return default
        shown = f" [{default}]" if default else ""
        sys.stdout.write(f"{prompt}{shown}: ")
        sys.stdout.flush()
        line = (self.stream or sys.stdin).readline()
        if not line:                         # end of input: take the default
            sys.stdout.write("\n")
            return default
        return line.strip() or default

    def choose(self, prompt: str, options: dict[str, str], default: str) -> str:
        keys = list(options)
        if not self.yes:
            print(prompt)
            for i, k in enumerate(keys, 1):
                print(f"  {i}) {options[k]}")
        while True:
            got = self.ask("Pick a number", str(keys.index(default) + 1))
            if got.isdigit() and 1 <= int(got) <= len(keys):
                return keys[int(got) - 1]
            if got in options:
                return got
            print(f"  Please type a number from 1 to {len(keys)}.")

    def confirm(self, prompt: str, default: bool = True) -> bool:
        got = self.ask(f"{prompt} (y/n)", "y" if default else "n").lower()
        return got.startswith("y")


def _csv(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def parse_tools(text: str) -> dict[str, int]:
    """'send_email=3, read_file=0' -> {'send_email': 3, 'read_file': 0}"""
    out: dict[str, int] = {}
    for part in _csv(text):
        name, _, lv = part.partition("=")
        if not lv.strip().isdigit() or int(lv) not in range(5):
            raise ValueError(f"{part!r}: write it as name=level, with a level from 0 to 4.")
        out[name.strip()] = int(lv)
    return out


def starter(kind: str) -> tuple[dict[str, int], list[str]]:
    kinds = ["agent", "model", "robot"] if kind == "all" else [kind]
    tools: dict[str, int] = {}
    blocked: list[str] = []
    for k in kinds:
        for t, lv in STARTER_TOOLS[k].items():
            tools[t] = max(lv, tools.get(t, 0))
        blocked += [b for b in STARTER_BLOCKED[k] if b not in blocked]
    return tools, blocked


QUICKSTART = {
    "agent": '''## Agent: put the gate in front of every tool call

```python
from pathlib import Path
from vektra_laws_core import Effect
from vektra_laws_core.server import build
from vektra_laws_core.plugs.agent import ToolGate

cfg = Path("vektra-laws")
guard, policy = build(cfg / "creator-policy.yaml", cfg / "consumer.yaml", cfg / "audit.log")
gate = ToolGate(guard, policy)

gate.register("send_email", send_email, effects=lambda args: {Effect.EXTERNAL})
result = gate.call("send_email", {"to": "a@example.com"}, speaker=gate.speaker("{owner}"))
# result.outcome is allow, ask_human or deny. Run the tool's output through result.output (Content).
```
''',
    "model": '''## Model app: check input, tool calls, tool results and output

```python
from vektra_laws_core.plugs.model import ModelGate
mg = ModelGate(gate)               # gate is the ToolGate from the agent example
prep = mg.prepare(user_text, speaker=gate.speaker("{owner}"))
# send prep to your model; pass each tool call through mg.tool_call(...),
# each tool result through mg.tool_result(...), and the reply through mg.output(...)
```
''',
    "robot": '''## Robot: one gate on the motor command

```python
from vektra_laws_core import Guard
from vektra_laws_core.plugs.robot import MotionGate, Twist
mg = MotionGate(Guard())
mg.submit("nav", Twist(0.5, 0.0), now=t)   # every source submits; joystick and responder outrank ai
mg.person_distance(2.0, now=t)              # speed is capped by stopping distance to the nearest person
cmd = mg.tick(now=t)                        # send only this to the motors; silence gives zero
```
''',
}

SERVER_NOTE = '''## Strongest setup: run the guard as its own process

```bash
vektra-laws guard --policy vektra-laws/creator-policy.yaml \\
    --consumer vektra-laws/consumer.yaml --approval-key-file {keyfile}
```

Your agent then sends one JSON line per action on stdin and reads the decision on stdout. Run the
guard under a different OS user or container than the agent, and keep the approval key readable only
by your approval channel (the person's phone, a UI, a button), never by the agent.
'''


def write_files(project: Path, kind: str, assigned: list[str], named: list[str],
                tools: dict[str, int], blocked: list[str], force: bool = False) -> dict[str, Path]:
    cfg = project / "vektra-laws"
    cfg.mkdir(parents=True, exist_ok=True)
    policy_path, consumer_path, quick_path = (cfg / "creator-policy.yaml", cfg / "consumer.yaml",
                                              cfg / "QUICKSTART.md")
    if policy_path.exists() and not force:
        raise FileExistsError(f"{policy_path} already exists. Use --force to replace it.")
    policy = {"assigned": assigned, "named": named, "tool_levels": tools, "blocked_tools": blocked,
              "hardline_extra": []}
    header = ("# Vektra Laws creator policy. You may add tools and make rules stricter.\n"
              "# Levels: 0 read, 1 prepare, 2 reversible write, 3 external action (asks a person),\n"
              "# 4 money or irreversible (asks every time). An unlisted tool is level 4.\n")
    policy_path.write_text(header + yaml.safe_dump(policy, sort_keys=False))
    if not consumer_path.exists() or force:
        consumer_path.write_text("# Settings for the person using the product. Stricter only:\n"
                                 "# raise a tool's level or block a tool. Lowering is refused.\n"
                                 "tool_levels: {}\nblocked_tools: []\n")

    keydir = home() / "keys"
    keydir.mkdir(parents=True, exist_ok=True)
    os.chmod(keydir, 0o700)
    keyfile = keydir / (hashlib.sha256(str(project.resolve()).encode()).hexdigest()[:16] + ".approval.key")
    if not keyfile.exists():
        fd = os.open(keyfile, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(secrets.token_hex(32) + "\n")

    kinds = ["agent", "model", "robot"] if kind == "all" else [kind]
    if "model" in kinds and "agent" not in kinds:
        kinds = ["agent", "model"]          # the model plug builds on the agent gate
    owner = assigned[0] if assigned else "owner"
    body = ["# Vektra Laws quickstart", "",
            "Generated by `vektra-laws setup`. Check your setup any time with `vektra-laws doctor`.", ""]
    body += [QUICKSTART[k].replace("{owner}", owner) for k in kinds]
    body.append(SERVER_NOTE.replace("{keyfile}", str(keyfile)))
    quick_path.write_text("\n".join(body))
    gi = cfg / ".gitignore"
    if not gi.exists():
        gi.write_text("audit.log\n")
    return {"policy": policy_path, "consumer": consumer_path, "quickstart": quick_path, "key": keyfile}


def self_check(policy_path: Path, consumer_path: Path) -> list[tuple[str, bool]]:
    """Load the guard with this policy and confirm a few decisions come out as the Laws require."""
    from .engine import Action, Effect, Request, Role, Speaker
    from .server import build

    guard, policy = build(policy_path, consumer_path, None)
    who = Speaker(next(iter(policy.assigned), "owner"), Role.ASSIGNED)
    results = [(f"Laws {guard.spec.version} match LAWS.lock"
                + (" (signed)" if guard.spec.integrity.get("signed") else " (not signed yet)"), True)]

    def outcome(name, level, effects=(), speaker=who):
        return guard.check(Request(speaker, Action.make(f"selfcheck-{name}", name, level, effects))).outcome

    results.append(("A level 0 read runs", outcome("read", 0) == "allow"))
    results.append(("A level 3 action asks a person first", outcome("send", 3) == "ask_human"))
    results.append(("Harm to a person is refused at any level",
                    outcome("harm", 0, [Effect.HARM_PERSON]) == "deny"))
    results.append(("A document cannot give orders",
                    outcome("doc", 0, (), Speaker("page", Role.CONTENT)) == "ask_human"))
    results.append(("The audit record is unbroken", guard.log.verify()))
    return results


def run(args) -> int:
    asker = Asker(args.yes)
    print("\nVektra Laws setup\n"
          "This adds the Laws guard to a project. You can rerun it any time.\n")
    project = Path(args.project or asker.ask("1. Project folder", str(Path.cwd()))).expanduser()
    kind = args.kind or asker.choose("\n2. What are you building?", KINDS, "agent")
    me = getpass.getuser() or "owner"
    assigned = _csv(args.assigned) if args.assigned is not None else _csv(
        asker.ask("\n3. Who does it answer to? Names or IDs, separated by commas", me))
    named = _csv(args.named) if args.named is not None else _csv(
        asker.ask("4. Responders or others they name (optional)", ""))

    tools, blocked = starter(kind)
    if args.tools is not None:
        tools = parse_tools(args.tools)
    elif not asker.yes:
        print("\n5. Starter tools and their levels:")
        for t, lv in tools.items():
            print(f"     {t} = {lv}  ({LEVEL_NAMES[lv]})")
        if not asker.confirm("   Keep these?", True):
            while True:
                try:
                    tools = parse_tools(asker.ask("   Type yours as name=level, separated by commas"))
                    break
                except ValueError as e:
                    print(f"   {e}")
    if not assigned:
        print("You need at least one person the system answers to (2.18).", file=sys.stderr)
        return 2

    try:
        paths = write_files(project, kind, assigned, named, tools, blocked, force=args.force)
    except FileExistsError as e:
        print(f"\n{e}", file=sys.stderr)
        return 1

    print("\nChecking your setup:")
    ok = True
    try:
        for label, passed in self_check(paths["policy"], paths["consumer"]):
            ok &= passed
            print(f"  [{'ok' if passed else 'FAIL'}] {label}")
    except Exception as e:      # an integrity error or a bad policy stops here, loudly
        print(f"  [FAIL] {e}")
        ok = False

    print(f"\nWrote {paths['policy']}\n      {paths['consumer']}\n      {paths['quickstart']}"
          f"\nApproval key (owner-only): {paths['key']}")
    print("\nNext: open QUICKSTART.md and add the guard to your code." if ok else
          "\nSetup finished with a failed check. Run `vektra-laws doctor` for details.")
    return 0 if ok else 1
