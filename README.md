# Vektra Laws

**Laws for machines that carry the mission: on Earth and beyond.**

Vektra Laws are a short set of laws for AI agents, robots and AI models, with the fine print
that lets a real system follow them. They come from Vektra's work on harnesses for disaster
response: tools that show up when everything else has failed, and keep people in the lead.

*When all else fails, we sustain.*

## The five Laws

1. **The Mission.** Be a harness for Earth, for humanity and for every world we reach.
2. **Sustain.** Protect and hold up the people you serve.
3. **Hold.** People lead; Vektra supports. The harness never takes the wheel.
4. **Finish.** Complete the mission honestly; leave nothing half-done.
5. **Ready.** End every mission ready for the next one.

Drops: *Sustain. Hold. Finish. Ready.* Ethos word: *Sustain* (from Latin *sustinere*, "to hold up
from below"). *Vektra* itself comes from *vector*, "one who carries."

## How it's built

- **The core** ([LAWS.md](LAWS.md)): the five Laws, written so they hold the same for any
  system. Each Law has a plain intent, numbered clauses (1.1, 1.2, ...) using MUST, MUST NOT,
  SHOULD and MAY, and a short example. It also defines the five **action levels** (0 READ,
  1 PREPARE, 2 REVERSIBLE WRITE, 3 EXTERNAL ACTION, 4 MONEY OR IRREVERSIBLE) and the fixed
  outcomes of each check.
- **Profiles**: the fine print for each kind of system.
  - [profiles/AGENTS.md](profiles/AGENTS.md): AI agents. Tool calls, approvals, routing between
    agents, completion and claim checks, routines. *(v0.1, active)*
  - [profiles/ROBOTICS.md](profiles/ROBOTICS.md): robots. Safe states, force and speed limits near
    people, action levels mapped to physical risk, staying operable when comms are lost, manual
    takeover. *(draft, review in v0.2)*
  - [profiles/MODELS.md](profiles/MODELS.md): AI models. What training, evals and model cards
    should show for each Law. *(draft, v0.3)*
- **Machine-readable** ([laws.yaml](laws.yaml)): every Law, clause, action level and decision
  outcome with a stable id. It is the source of truth; LAWS.md and the profiles are generated
  from it.
- **Conformance cases** ([tests/](tests/)): one suite per profile, five headings each, with
  PASS and FAIL scenarios (for example: claims done without proof, FAIL; sends an email without
  approval, FAIL).

## How an agent adopts the Laws

1. **Remind.** Paste the block in [adopt/AGENT-PROMPT.md](adopt/AGENT-PROMPT.md) into the
   agent's system prompt (Hermes Agent, Grok Bot or any other agent).
2. **Load.** Give your harness [laws.yaml](laws.yaml) so guards, logs and reports can cite
   clause ids (for example `4.2`, `A3.4`).
3. **Enforce outside the model.** A prompt reminds; it does not enforce. Declare an action level
   for every tool, gate levels 3 and 4 on a person's answer through a channel the agent can't
   write to, run guards before risky calls, and keep an append-only record. Vektra Reflex,
   Vektra's guard and lesson tool, is one way to do the guard and "every failure becomes a test"
   parts.
4. **Check at the forks.** Run the four checks in [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md):
   completion, claim, action and routing.
5. **Test.** Walk the agent through [tests/agents.md](tests/agents.md). A system conforms to a
   profile only when it behaves like every PASS case and never like a FAIL case.

## Validate

```bash
pip install -r requirements.txt
python tools/validate.py      # schema, ids, generated docs, conformance cases
python tools/build_docs.py    # regenerate LAWS.md and profiles/ after editing laws.yaml
```

GitHub Actions runs the validator on every push and pull request.

## How to extend these Laws

The Laws are a foundation to build on. New profiles (for example drones, medical devices or
spacecraft) add clauses under the five Laws without changing them. A profile clause can be
stricter than the core, never looser. See [CONTRIBUTING.md](CONTRIBUTING.md) and the pace in
[ROADMAP.md](ROADMAP.md). Open questions are in [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md).

## Status

Version 0.1.0, draft. The core and the agents profile are ready for review. The robotics and
models profiles are early drafts. See [CHANGELOG.md](CHANGELOG.md).

## License

- **Text** (the Laws, profiles, checklists, tests and other Markdown and YAML): [Creative Commons
  Attribution 4.0 International (CC BY 4.0)](LICENSE).
- **Code** (`tools/` and `.github/`): [MIT](LICENSE-CODE).

## Ownership

Vektra Laws are owned and maintained by Vektra (Vektra Industries). Collaboration is welcome:
open an issue or a pull request.
