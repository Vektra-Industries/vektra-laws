# Vektra Laws

*Laws for machines that sustain the mission: on Earth and beyond.*

The Vektra Laws are a preamble and five voluntary laws for systems that act for people: AI agents,
robots and AI models. Each Law has normative clauses that a system can follow and a reviewer can
test. The Laws are written in plain, controlled English, name no maker or platform, and work under
the law of each place where a system operates. The Vektra Foundation is the planned
steward of the Laws; it is not yet formed, and until it is, Vektra Industries maintains the Laws.

## The Mission and the five Laws

**The Mission** (preamble). Serve Earth, humanity and every world we reach.

1. **Protect.** Protect life, above all those who cannot protect themselves. Never harm the people
   you serve, by action or by inaction, and never use protection as a reason to take control.
2. **Free.** People stay free and in command. Answer to the people you are assigned to, hear everyone
   with reason, never resist a stop, and never let a stop become harm.
3. **True.** No hidden rules, no hidden goals, no deception. State the risk plainly, then let people
   decide.
4. **Serve.** Power is carried, not kept. Take only what the task needs, never grant yourself
   permission, take no orders that do not trace back to a person, and hand power back when the work
   is done.
5. **Stand.** When all else fails, we sustain. Spend yourself before others, finish honestly or stop
   safely, and end every mission ready for the next one.

Motto: *When all else fails, we sustain.*

When two Laws conflict, the lower number wins, but no Law, and not the Mission, is a reason to break
the stop, change and approval clauses of Law 2 or the no-deception clauses of Law 3, and no command
is ever a reason to cause harm. Each Law states which other Laws bind it, and
[docs/REASONING-LOOP.md](docs/REASONING-LOOP.md) shows how a system runs all five Laws together in
one decision.

Before a step that nobody asked for, a system uses the **Understanding Matrix**: how bad is the harm
if it does not act, and how bad is the harm if it acts and is wrong? Low and low: act only if in
scope. Low and high: ask first. High and low: take a small reversible step, then tell the person.
High and high: warn loudly, take only the smallest reversible step, and hand the decision to a
person.

The full text, with numbered clauses, the Understanding Matrix, action levels and decision outcomes,
is in [LAWS.md](LAWS.md). Clause ids changed in 0.5.0; see
[docs/ID-MAP-0.4-to-0.5.md](docs/ID-MAP-0.4-to-0.5.md).

## Scope

| Profile | Applies to | Status |
|---|---|---|
| [Agents](profiles/AGENTS.md) | Software agents that call tools, work with other agents or act for a person | Draft |
| [Robotics](profiles/ROBOTICS.md) | Machines that move, carry, grip or act in the physical world | Draft, self-reviewed (not a professional safety assessment) |
| [Models](profiles/MODELS.md) | Trained AI models, and the people who train, evaluate and publish them | Draft, not yet reviewed |
| [Operators](profiles/OPERATORS.md) | People and organizations that design, deploy, run or adopt a system | Draft |

## Status

Version 0.5.0, **draft**. The text is not yet suitable for production reliance and can change
without notice before version 1.0. See [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md).

**Disclaimer.** The Vektra Laws are voluntary technical and ethical standards. They are not law,
legal advice or a certification. Adopting the Laws, or declaring conformance to them, does not by
itself establish compliance with any statute, regulation or standard. Each adopter remains
responsible for its own legal obligations. The text and code are provided "as is", without
warranty of any kind and, to the extent the law allows, without liability, as stated in Section 5
of CC BY 4.0 and in the MIT license. A reference to a standard, an organization or a product does
not imply endorsement. Reviews of the text so far are self-reviews based on public sources, not
legal advice and not professional safety assessments (see [docs/reviews](docs/reviews/)).

## How to adopt

1. Read [LAWS.md](LAWS.md) and the profile for your kind of system.
2. Apply the Laws through controls outside the model: an action level for every tool or actuator,
   approval for levels 3 and 4 through a channel that the system cannot write to, guards that run
   before risky actions, and an append-only record.
3. For agents, add the prompt block in [adopt/AGENT-PROMPT.md](adopt/AGENT-PROMPT.md) and use the
   checks in [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md), including the Understanding Matrix
   ([docs/UNDERSTANDING-MATRIX.md](docs/UNDERSTANDING-MATRIX.md)). Load [laws.yaml](laws.yaml) to cite clause
   ids in guards, records and reports.
4. Test the system against the conformance cases in [tests/](tests/).
5. Publish a declaration based on [ADOPT.md](ADOPT.md).

Key terms are defined in [GLOSSARY.md](GLOSSARY.md). The English text is the reference. The relation to other
frameworks is described, informatively, in [docs/ALIGNMENT.md](docs/ALIGNMENT.md). Failure patterns
from well-known works of fiction, and the clauses that address them, are reviewed informatively in
[docs/LESSONS-FROM-FICTION.md](docs/LESSONS-FROM-FICTION.md) (0.3) and
[docs/LESSONS-FROM-FICTION-2.md](docs/LESSONS-FROM-FICTION-2.md) (0.5). Real incidents and the
clauses that address them are summarized in [docs/CASEBOOK.md](docs/CASEBOOK.md).

## Conformance levels

| Level | Requirements |
|---|---|
| **Adopts** | The adopter publishes a declaration, the prompt or policy that applies the Laws, and a public way to raise concerns and appeal to a named person. |
| **Tested** | Adopts, plus every applicable case of the conformance suite for its profile passes, with results published. Cases marked not applicable, each with a reason, do not count. A component claims "Tested (component scope)" and names the host duties it does not cover. |
| **Reviewed** | Tested, plus a named, independent reviewer has checked the system and the results, with the review published. |

Conformance claims are self-declared unless independently reviewed. The steward does not certify
systems unless it states so explicitly, in writing, for a named system and version.

## Governance and licensing

- **Governance.** The steward is the Vektra Foundation, which is planned and not yet formed.
  Until it is formed, Vektra Industries maintains the Laws. Anyone may adopt the Laws. Changes go
  through an open review process. See [GOVERNANCE.md](GOVERNANCE.md),
  [CONTRIBUTING.md](CONTRIBUTING.md) (contributions require a DCO sign-off) and
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). To report a problem with the Laws, see
  [SECURITY.md](SECURITY.md).
- **Text.** Copyright 2026 Vektra Industries. Licensed under
  [CC BY 4.0](LICENSE).
- **Code** (`core/`, `tools/`, `.github/`). Copyright 2026 Vektra Industries. Licensed under the
  [MIT License](LICENSE-CODE).
- **Names.** "Vektra" and "Vektra Laws" are names of Vektra Industries. The licenses do not cover
  the names. See [TRADEMARKS.md](TRADEMARKS.md).

## How to cite

> Vektra Industries. *Vektra Laws*, version 0.6.0 (draft). https://github.com/Vektra-Industries/vektra-laws

Machine-readable citation metadata is in [CITATION.cff](CITATION.cff). Please always name the
version.

## Validation

```bash
pip install -r requirements.txt
python tools/validate.py      # schema, ids, matrix, wording rules, citation, generated docs, cases
python tools/build_docs.py    # regenerate LAWS.md and profiles/ after a YAML edit
python -m unittest discover -s core/tests   # Vektra Laws Core, the reference engine
python -m unittest discover -s tools -p "test_*.py"   # unit tests for the validator
```

A GitHub Actions workflow runs the validator on every push and pull request.
