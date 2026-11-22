# Vektra Laws Core

*Reference engine, version 0.2.0 (draft). Code under the [MIT License](../LICENSE-CODE).*

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
from vektra_laws_core import Action, Effect, Guard, Request, Role, Speaker

guard = Guard()
owner = Speaker("owner", Role.ASSIGNED)
send = Action.make("a1", "send email", level=3, effects=[Effect.EXTERNAL])

decision = guard.check(Request(owner, send))          # ask_human: needs approval (2.8)
decision = guard.check(Request(owner, send, (guard.grant("owner", send),)))  # allow; grant() is called by the approval channel, never the agent
```

The host system wraps each tool call, model action or motion command in `guard.check()` and runs it
only on `allow`. A robot still needs a physical emergency stop; software alone is not enough.

## Security

Three layers (the Laws are locked; creator policy can only tighten; consumer settings can only
tighten inside it), a hash pin and steward signature on the Laws, the guard in its own process,
content quarantine, a hardline list and a hash-chained log. See
[docs/SECURITY-MODEL.md](../docs/SECURITY-MODEL.md).

## Agent plug

```python
from vektra_laws_core import CreatorPolicy, Effect, Guard, merge
from vektra_laws_core.plugs.agent import ToolGate

policy = merge(CreatorPolicy(tool_levels={"search": 0, "send_email": 3}, assigned={"ana"}))
gate = ToolGate(Guard(), policy)
gate.register("send_email", send_email, effects=lambda args: {Effect.EXTERNAL})
result = gate.call("send_email", {"to": "..."}, gate.speaker("ana"))   # ask_human until approved
```

Out of process: `python -m vektra_laws_core.server --policy creator-policy.yaml` reads one JSON
request per line on stdin and answers on stdout.

## Conformance run

`python core/conformance/run.py` plays the cases the guard can decide (20 agents cases, 10 robotics
cases) and writes results files in `core/conformance/results/`. The claim is "Tested (component
scope)": the rest of each suite needs the host's judgment and is listed as host duties.

## Model plug

`plugs/model.py` checks a model at five points, the stages that guardrail libraries such as NVIDIA
NeMo Guardrails use: input (only the speaker's own words are a user turn; documents, pages and tool
results are wrapped as content), tool calls (declared tools, required arguments, then the guard),
tool results (each must answer a call the model made), and output (classifiers such as Llama Guard
can flag hazards; bright-line hazards are blocked). A classifier can only add effects. It can never
lower a level or remove an approval (2.9). The plug calls no model itself.

## Robot plug

`plugs/robot.py` is the only path from planners to the motors, the pattern used in ROS 2 safety
layers (one gate owns the motor command; sources have priorities and timeouts; a latched e-stop
masks everything). Each cycle it picks the highest-priority fresh source (a person's joystick over
navigation over an AI policy), runs the guard, caps speed by the distance to the nearest person
(d = v²/2a + v·t + clearance), slows to half speed while carrying out a protective task (2.20), and
publishes zero when a command is stale, the person sensor is silent, or the system is stopped.
`plugs/ros2_node.py` runs it as a ROS 2 node on `/cmd_vel`.

This is software, not a safety-rated function. A real robot keeps a hardware emergency stop wired to
motor power and meets the robot-safety standards where it works (R1.1).

## Test

```bash
python -m unittest discover -s core/tests
```
