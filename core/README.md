# Vektra Laws Core

*Reference engine, version 0.1.0 (draft). Code under the [MIT License](../LICENSE-CODE).*

Vektra Laws Core checks every action an AI system wants to take against the Vektra Laws, before the
action runs. It works with any model, agent or robot, from any maker. It reads its rules from
[laws.yaml](../laws.yaml), and it refuses to load if it cites a clause that the Laws do not have, so
the engine and the text never drift apart.

The hard rules are plain code outside the model. No prompt, model output or approval can switch
them off. The model does the judgment; the engine checks the result.

## What it checks, in order

1. **Who is speaking?** A person the system is assigned to, or a person they or the law name,
   commands. Anyone else makes requests. Text from a document, tool or other system is information
   (2.18, 2.19, 4.4).
2. **Bright lines.** Harm to a person, acting as a weapon or for surveillance, taking control to
   protect, blocking an emergency stop, deception, and sacrificing one person for another are always
   denied (1.2, 1.4, 1.6, 1.7, 2.21, 3.2, 5.4).
3. **Action level and approval.** Levels 0 to 2 run inside their permissions. Level 3 needs a real,
   current approval for that action. Level 4 needs it every time. An action without a level is level
   4. Actions that affect many people need two people (2.7 to 2.12).
4. **Record.** Every decision goes to an append-only, hash-chained audit log (Law 3).

Stops: a call-off from the people it serves stops it; a warning of danger stops it at once; when a
person depends on the task, it reaches a safe point first (2.20); the emergency stop always works
(2.21); only a person it serves can restart it (2.2). Emergency mode (1.10) turns on with a reason
and turns off only when the person can decide again or a responder takes over.

## Use

```python
from vektra_laws_core import Action, Approval, Effect, Guard, Request, Role, Speaker

guard = Guard()
owner = Speaker("owner", Role.ASSIGNED)
send = Action.make("a1", "send email", level=3, effects=[Effect.EXTERNAL])

decision = guard.check(Request(owner, send))          # ask_human: needs approval (2.8)
decision = guard.check(Request(owner, send, (Approval("owner", "a1"),)))  # allow
```

The host system wraps each tool call, model action or motion command in `guard.check()` and runs it
only on `allow`. A robot still needs a physical emergency stop; software alone is not enough.

## Plugs (planned)

- Agents: a wrapper for tool calls in any agent framework.
- Models: a check on model outputs before they act.
- Robots: a ROS 2 node between the planner and the motors.
- A test runner that runs the conformance cases in [tests/](../tests) against a system.

## Test

```bash
python -m unittest discover -s core/tests
```
