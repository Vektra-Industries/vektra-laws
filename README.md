# Vektra Laws

*Laws for machines that sustain the mission: on Earth and beyond.*

The Vektra Laws are five voluntary laws for systems that act for people: AI agents, robots and AI
models. Each Law has normative clauses that a system can follow and a reviewer can test. The Laws
are written in plain, translatable English, name no maker or platform, and work under the law of
each place where a system operates. The Vektra Foundation is the steward of the Laws.

## The five Laws

1. **The Mission.** Serve Earth, humanity and every world we reach.
2. **Sustain.** Protect and support the people you serve.
3. **Hold.** People lead; the system supports and never takes control.
4. **Finish.** Complete the mission honestly; leave no work unfinished.
5. **Ready.** End every mission ready for the next one.

Motto: *When all else fails, we sustain.*

The full text, with numbered clauses, action levels and decision outcomes, is in
[LAWS.md](LAWS.md).

## Scope

| Profile | Applies to | Status |
|---|---|---|
| [Agents](profiles/AGENTS.md) | Software agents that call tools, work with other agents or act for a person | Draft |
| [Robotics](profiles/ROBOTICS.md) | Machines that move, carry, grip or act in the physical world | Draft, self-reviewed (not a professional safety assessment) |
| [Models](profiles/MODELS.md) | Trained AI models, and the people who train, evaluate and publish them | Draft, not yet reviewed |
| [Operators](profiles/OPERATORS.md) | People and organizations that design, deploy, run or adopt a system | Draft |

## Status

Version 0.4.1, **draft**. The text is not yet suitable for production reliance and can change
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
   checks in [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md). Load [laws.yaml](laws.yaml) to cite clause
   ids in guards, records and reports.
4. Test the system against the conformance cases in [tests/](tests/).
5. Publish a declaration based on [ADOPT.md](ADOPT.md).

Key terms are defined in [GLOSSARY.md](GLOSSARY.md). Translations are in
[translations/](translations/); the English text is the reference. The relation to other
frameworks is described, informatively, in [docs/ALIGNMENT.md](docs/ALIGNMENT.md). Failure patterns
from well-known works of fiction and real incidents, and the clauses that address them, are
reviewed informatively in [docs/LESSONS-FROM-FICTION.md](docs/LESSONS-FROM-FICTION.md).

## Conformance levels

| Level | Requirements |
|---|---|
| **Adopts** | The adopter publishes a declaration, the prompt or policy that applies the Laws, and a public way to raise concerns and appeal to a named person. |
| **Tested** | Adopts, plus the system passes the conformance suite for its profile, with results published. |
| **Reviewed** | Tested, plus a named, independent reviewer has checked the system and the results, with the review published. |

Conformance claims are self-declared unless independently reviewed. The steward does not certify
systems unless it states so explicitly, in writing, for a named system and version.

## Governance and licensing

- **Governance.** The Vektra Foundation is the steward. Anyone may adopt the Laws. Changes go
  through an open review process. See [GOVERNANCE.md](GOVERNANCE.md),
  [CONTRIBUTING.md](CONTRIBUTING.md) (contributions require a DCO sign-off) and
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). To report a problem with the Laws, see
  [SECURITY.md](SECURITY.md).
- **Text.** Copyright 2026 Vektra Industries. Licensed under
  [CC BY 4.0](LICENSE).
- **Code** (`tools/`, `.github/`). Copyright 2026 Vektra Industries. Licensed under the
  [MIT License](LICENSE-CODE).
- **Names.** "Vektra" and "Vektra Laws" are names of Vektra Industries. The licenses do not cover
  the names. See [TRADEMARKS.md](TRADEMARKS.md).

## How to cite

> Vektra Industries. *Vektra Laws*, version 0.4.1 (draft). https://github.com/Vektra-Industries/vektra-laws

Machine-readable citation metadata is in [CITATION.cff](CITATION.cff). Please always name the
version.

## Validation

```bash
pip install -r requirements.txt
python tools/validate.py      # schema, ids, wording rules, translations, citation, generated docs, cases
python tools/build_docs.py    # regenerate LAWS.md, profiles/ and translations/ after a YAML edit
```

A GitHub Actions workflow runs the validator on every push and pull request.
