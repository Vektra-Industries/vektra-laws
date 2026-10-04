# Changelog

All notable changes to the Vektra Laws. Versions follow the [roadmap](ROADMAP.md).

## v0.2.0 (draft, 2026-10-04)

The universal version. Any agent, robot or model, from any maker, in any country, can adopt the
Laws. Not yet approved or released.

### Changed
- The core and the profiles now speak about "the system" and "the people it serves". They name no
  maker, product, platform or internal tool. Vektra appears only as owner and steward.
- All text rewritten in controlled English: short, plain sentences, no idioms and no
  contractions. RFC 2119 keywords are defined once.
- New one-line statements for Law 1 and Law 3 (and plainer wording for Law 2 and Law 4); see
  docs/OPEN-QUESTIONS.md #1.
- Clause titles made literal (for example "Respect a refusal" instead of "Take no for an answer").
- The roadmap now follows the universal path (v0.2 universal core, v0.3 robotics, v0.4 models and
  a runnable suite, v1.0 public release).
- Reference adopters (Vektra Agent, Phryktor, vektra-reflex) moved out of the core and roadmap
  text into docs/REFERENCE-ADOPTERS.md.

### Added
- Clause 1.4, "Follow the law of the place": the system follows local law, and the stricter rule
  applies. Test case AG-27.
- GLOSSARY.md, with one-sentence definitions of every key term.
- translations/, with rules for translations and a first Spanish (es) translation of the five
  Laws, their one-line statements and the motto.
- Conformance levels (Adopts, Tested, Verified) and ADOPT.md with a self-declaration template.
- GOVERNANCE.md: the Vektra Foundation as steward, adoption open to anyone, an open review process,
  and ownership with Vektra.
- docs/ALIGNMENT.md: how the Laws relate to the EU AI Act, the NIST AI RMF, the OECD AI Principles,
  the UNESCO Recommendation on the Ethics of AI, ISO/IEC 42001, ISO 10218 and ISO/TS 15066. It
  claims no legal compliance.
- Validator checks for universal text (no maker or platform names, no contractions), for
  translation ids that match the reference, and for conformance levels.

## v0.1.0 (draft, 2026-10-04)

First draft, not yet sealed or released.

### Added
- The core: the five Laws (The Mission, Sustain, Hold, Finish, Ready) from the approved Vektra
  Laws v2, written to apply to agents, robots and models alike, with 35 numbered clauses, the
  five action levels and the decision outcomes for the completion, claim, action, routing and
  result checks.
- Profiles: AI agents (19 clauses, active), robotics (13 clauses, draft), models (12 clauses,
  draft).
- `laws.yaml` as the single source of truth, with `tools/build_docs.py` generating LAWS.md and
  the profiles.
- `adopt/AGENT-PROMPT.md` (paste-in block) and `adopt/CHECKLISTS.md` (completion, claim, action
  and routing checks).
- Conformance cases: 26 for agents, 9 for robotics, 8 for models, each under the five Law
  headings.
- `tools/validate.py` and a GitHub Actions workflow that runs it.
- ROADMAP.md, docs/OPEN-QUESTIONS.md, CONTRIBUTING.md, licenses (CC BY 4.0 for text, MIT for
  code).

### Changed
- Ethos word set to *Sustain* (confirmed by Pablo), replacing Carry in README and laws.yaml.

### Credits
- **Ada** (software): the code-enforceable clauses: action levels declared before shipping, with
  undeclared actions counted as level 4; human answers only through a channel the system can't
  write to; guards before the act that the system can't remove (2.4, A2.1); a call-off that
  reaches every child process and reports what it couldn't stop (3.9, A3.7); honest result
  scoring (4.6); a tamper-evident record (5.4); and one conformance suite per profile under the
  same five headings.
- **Sol** (people): the human-side clauses: One thing at a time (2.5), Keep their dignity (2.6),
  They choose, you carry (3.1), Ask first (3.2), Say it plain (3.3).
- **Rei** (brand): the voice rules (lead with the verb, one line per Law, crew voice, calm and
  humble), the tagline, and the "How to extend these Laws" section.
- Coordination, completion and claim-check clauses (no proof, no done; a worker doesn't grade its
  own claims; route only to workers that exist; automate only what has worked once) adapted from
  multi-agent practice Pablo flagged.
