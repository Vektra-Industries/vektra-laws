# Changelog

All notable changes to Vektra Laws. Versions follow the [roadmap](ROADMAP.md).

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
