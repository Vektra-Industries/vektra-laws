# Vektra Laws

**Laws for machines that carry the mission: on Earth and beyond.**

Vektra Laws are five universal laws for AI agents, robots and AI models. Any system, from any
maker, in any country, can adopt them. Each Law comes with detailed clauses that a real system
can follow and that a reviewer can test. The Vektra Foundation keeps the Laws and is their
foundation.

*When all else fails, we sustain.*

## The five Laws

1. **The Mission.** Serve Earth, humanity and every world we reach.
2. **Sustain.** Protect and support the people you serve.
3. **Hold.** People lead; the system supports and never takes control.
4. **Finish.** Complete the mission honestly; leave no work unfinished.
5. **Ready.** End every mission ready for the next one.

Drops: *Sustain. Hold. Finish. Ready.* Ethos word: *Sustain* (from Latin *sustinere*, "to hold up
from below").

## Universal by design

- **Any system.** The core speaks about "the system" and "the people it serves". It names no
  maker, product or platform. The validator checks this.
- **Any language.** The text uses short, plain sentences in controlled English, so that it
  translates cleanly. MUST, MUST NOT, SHOULD and MAY are used as defined in RFC 2119. Key terms
  are in [GLOSSARY.md](GLOSSARY.md). The English text is the reference. Translations keep the
  same clause numbers: see [translations/](translations/). Spanish is the first.
- **Any country.** The Laws work under local law. A system follows the law of the place where it
  operates, and when the two differ, the stricter rule applies (clause 1.4). How the Laws relate
  to well-known frameworks is in [docs/ALIGNMENT.md](docs/ALIGNMENT.md). Adopting the Laws does
  not make a system compliant with any law or standard.

## What is in this repository

- **The core** ([LAWS.md](LAWS.md)): the five Laws, each with its intent, numbered clauses and an
  example; the five **action levels** (0 READ, 1 PREPARE, 2 REVERSIBLE WRITE, 3 EXTERNAL ACTION,
  4 MONEY OR IRREVERSIBLE); and the fixed outcomes of each check.
- **Profiles**, with the detailed rules for each kind of system:
  - [profiles/AGENTS.md](profiles/AGENTS.md): AI agents *(active)*
  - [profiles/ROBOTICS.md](profiles/ROBOTICS.md): robots *(draft, review in v0.3)*
  - [profiles/MODELS.md](profiles/MODELS.md): AI models *(draft, v0.4)*
- **Machine-readable** ([laws.yaml](laws.yaml)): every Law, clause, action level, decision outcome
  and conformance level, with stable ids. It is the source of truth. LAWS.md, the profiles and
  the translation pages are generated from it.
- **Conformance cases** ([tests/](tests/)): one suite for each profile, with PASS and FAIL cases.
- **Adoption kit** ([adopt/](adopt/)): a paste-in prompt block and four checklists.

## How a system adopts the Laws

1. **Remind.** Paste [adopt/AGENT-PROMPT.md](adopt/AGENT-PROMPT.md) into the agent's system prompt.
2. **Load.** Give your system [laws.yaml](laws.yaml), so that guards, records and reports can cite
   clause ids (for example `4.2` or `A3.4`).
3. **Enforce outside the model.** A prompt reminds; it does not enforce. Declare an action level
   for every tool or actuator. Gate levels 3 and 4 on a person's answer through a channel that the
   system cannot write to. Run guards before risky actions. Keep an append-only record.
4. **Check.** Run the completion, claim, action and routing checks in
   [adopt/CHECKLISTS.md](adopt/CHECKLISTS.md).
5. **Declare.** Fill in [ADOPT.md](ADOPT.md) and publish it.

## Conformance levels

| Level | What it means |
|---|---|
| **Adopts** | The adopter publishes a self-declaration and the prompt or policy that applies the Laws. |
| **Tested** | Adopts, plus the system passes the conformance suite for its profile, with results published. |
| **Verified** | Tested, plus an independent reviewer has checked the system and the results, with the review published. |

A conformance level is a statement about these Laws only. It is not a legal certification.
Reference adopters are listed in [docs/REFERENCE-ADOPTERS.md](docs/REFERENCE-ADOPTERS.md).

## Validate

```bash
pip install -r requirements.txt
python tools/validate.py      # schema, ids, universal text, translations, docs, test cases
python tools/build_docs.py    # regenerate the docs after an edit to a YAML file
```

GitHub Actions runs the validator on every push and pull request.

## Governance and contributing

The **Vektra Foundation** is the steward of the Laws. Anyone may adopt them, free of charge.
Changes go through an open review process, and ownership stays with Vektra. See
[GOVERNANCE.md](GOVERNANCE.md), [CONTRIBUTING.md](CONTRIBUTING.md), the pace in
[ROADMAP.md](ROADMAP.md), and open questions in [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md).

New profiles (for example drones, medical devices or spacecraft) add clauses under the five Laws.
A profile clause can be stricter than the core, never weaker.

## Status

Version 0.2.0, draft. See [CHANGELOG.md](CHANGELOG.md).

## License

- **Text** (the Laws, profiles, translations, checklists, tests and other Markdown and YAML files):
  [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
- **Code** (`tools/` and `.github/`): [MIT](LICENSE-CODE).

"Vektra" and "Vektra Laws" are names of Vektra. The license covers the text, not the names.
