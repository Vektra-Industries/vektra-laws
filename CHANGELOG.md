# Changelog

*This document is informative.* All notable changes to the Vektra Laws are recorded here. Versions
follow [ROADMAP.md](ROADMAP.md). No version has been released yet.

## Unreleased

No change to the normative text.

### Added
- docs/LESSONS-FROM-FICTION.md (informative): failure patterns from well-known works of fiction and
  real incidents, the clauses that address each, and the gaps found.
- docs/OPEN-QUESTIONS.md: eight clauses proposed for v0.3 (P1 to P8), three draft conformance cases
  (FX-01 to FX-03) and two questions for the owner. None is normative until the owner approves it.

### Changed
- Tagline: "Laws for machines that sustain the mission: on Earth and beyond." (laws.yaml, README,
  LAWS.md, CITATION.cff).

## 0.2.1 (draft, 2026-10-04)

Editorial and legal-hygiene pass. No change to the five Laws, their statements, the motto or the
meaning of any clause.

### Changed
- LAWS.md and the profiles restructured in standards style: status of the document, introduction,
  conventions and terminology, precedence and local law, the Laws, action levels, decision
  outcomes, conformance and references. Every section is labeled normative or informative. Each
  Law shows its statement and clauses (normative) and its intent and example (informative).
- Key words now refer to BCP 14 (RFC 2119 and RFC 8174).
- Status and disclaimer added: the Laws are voluntary technical and ethical standards; they are
  not law, legal advice or a certification; conformance does not by itself establish legal
  compliance; the text is provided "as is".
- Conformance rules made explicit: claims are self-declared unless independently verified; the
  Verified level requires a named reviewer; the steward does not certify systems unless it states
  so explicitly, in writing.
- README rewritten: purpose, the five Laws, scope, status, adoption, conformance levels,
  governance and licensing, citation.
- All documents edited for consistent terminology (GLOSSARY.md), consistent headings and a neutral
  tone. Internal brand terms removed from the documents. Contributor credits moved to
  Acknowledgments below.
- Owner stated as Vektra Industries in laws.yaml and GOVERNANCE.md.
- docs/ALIGNMENT.md retitled "Relation to other frameworks" and labeled informative and
  non-authoritative.

### Added
- TRADEMARKS.md (use of the names; no registration claimed).
- CITATION.cff.
- SECURITY.md (how to report a problem with the Laws, through GitHub issues).
- CODE_OF_CONDUCT.md (Contributor Covenant 2.1, by reference).
- Developer Certificate of Origin sign-off requirement in CONTRIBUTING.md.
- Glossary terms: conformance declaration, informative, normative, owner, reviewer.
- Validator checks for words that suggest legal authority or guarantees in the normative text,
  and for a CITATION.cff version that matches laws.yaml.

## 0.2.0 (draft, 2026-10-04)

Universal version: any AI agent, robot or AI model, from any maker, in any country, can adopt the
Laws.

### Changed
- The normative text uses "the system" and "the people it serves" and names no maker, product,
  platform or internal tool.
- All text rewritten in controlled English, with literal clause titles.
- New statements for Law 1 and Law 3, and plainer statements for Law 2 and Law 4, approved by the
  owner.
- Action levels confirmed: 0 READ, 1 PREPARE, 2 REVERSIBLE WRITE, 3 EXTERNAL ACTION, 4 MONEY OR
  IRREVERSIBLE.
- Copyright holder in LICENSE and LICENSE-CODE: Vektra Industries. Steward: Vektra Foundation.
- Roadmap updated for the universal path.
- Planned reference adopters moved to docs/REFERENCE-ADOPTERS.md.

### Added
- Clause 1.4, "Follow the law of the place", and conformance case AG-27.
- GLOSSARY.md; translations/ with a Spanish (es) translation of the five Laws and the motto.
- Conformance levels (Adopts, Tested, Verified) and ADOPT.md.
- GOVERNANCE.md; docs/ALIGNMENT.md.
- Validator checks for universal wording and for translation ids.

## 0.1.0 (draft, 2026-10-04)

First draft.

### Added
- The core: five Laws (The Mission, Sustain, Hold, Finish, Ready), numbered clauses, five action
  levels, and decision outcomes for the completion, claim, action, routing and result checks.
- Profiles for AI agents, robotics and AI models.
- laws.yaml as the single source, with generated documents.
- Agent prompt block and checklists.
- Conformance cases for each profile under the five Law headings.
- Validator and continuous-integration workflow.
- Licenses: CC BY 4.0 (text) and MIT (code).

## Acknowledgments

The following contributions to the drafts are gratefully acknowledged:

- **Ada** (software engineering): enforceable clauses, including action levels declared before
  deployment with undeclared actions treated as level 4; approvals only through a channel that the
  system cannot write to; guards before an action that the system cannot remove (2.4, A2.1); a
  call-off that reaches every process the system started (3.9, A3.7); honest result reporting
  (4.6); a record that shows changes (5.4); and one conformance suite per profile under the five
  Law headings.
- **Sol** (human factors): One step at a time (2.5), Respect every person (2.6), The person
  decides (3.1), Ask before acting on a person (3.2) and Speak plainly (3.3).
- **Rei** (brand and voice): the voice rules, the tagline, and the guidance on extending the Laws.
- The coordination, completion and claim-check clauses (prove completion; independent claim
  check; route only to available workers; automate only what worked) adapt practices from
  published work on multi-agent systems.
