# Changelog

*This document is informative.* All notable changes to the Vektra Laws are recorded here. Versions
follow [ROADMAP.md](ROADMAP.md). No version has been released yet.

## 0.4.1 (draft, 2026-10-04)

Self-reviews of the legal text and of the robotics profile, based on public sources
(docs/reviews/LEGAL-SELF-REVIEW.md and docs/reviews/ROBOTICS-SELF-REVIEW.md). They are not legal
advice and not a professional safety assessment. The five Laws, their statements, the motto and
the core clauses are unchanged.

### Added
- Robotics R1.2 Applicable standards and the risk assessment come first (MUST): the profile adds
  to the applicable robot-safety and functional-safety standards and the risk assessment, and
  never replaces them.
- Robotics R2.4 Protect safety settings and safety control (MUST).
- Robotics R3.6 A routine stop is not an emergency stop (MUST).
- Conformance cases RB-14 to RB-19. 83 cases in total.
- Glossary: emergency stop, monitored standstill, normal stop, performance level, protective
  stop, risk assessment, safety function, safety integrity level, stop category.
- docs/reviews/LEGAL-SELF-REVIEW.md and docs/reviews/ROBOTICS-SELF-REVIEW.md (informative).

### Changed
- Conformance level "Verified" renamed "Reviewed" (decided by the owner's delegate,
  2026-10-04). The levels are Adopts, Tested and Reviewed; Reviewed still names the independent
  reviewer.
- Robotics: R1.1 (protective stop when a safety function depends on the link), R2.1 (limits from
  the risk assessment and applicable standards; safety functions at the required PL or SIL; the
  collaborative content of ISO/TS 15066 is now in ISO 10218-2:2025), R3.2 (manual control by
  designed means, never over an emergency stop; limits on manual release), R3.3 (emergency stop
  category 0 or 1, priority, manual reset that does not start motion), R3.5 (the envelope is
  never wider than the risk assessment), R5.1 (safe state reached by design on power loss).
  Profile status: self-reviewed, not a professional safety assessment.
- Disclaimer: adds the limitation of liability in CC BY 4.0 Section 5 and that references do not
  imply endorsement.
- LICENSE: removes the overlap between YAML text and `.github/` code; states that the licenses
  grant no right in the names.
- TRADEMARKS.md: unregistered names, ™ only and never ®, the name rule is a trademark policy that
  does not restrict CC BY rights, no badges or "Vektra Verified", USPTO filing noted as a later
  option.
- ADOPT.md: rules 8 to 10 (no "certified", no badges, how to write "Verified", claims are the
  adopter's own); stale 0.2.x note replaced.
- GOVERNANCE.md: the steward certifies no systems, adopters or reviewers and issues no badge.
- CONTRIBUTING.md: the DCO summary covers clauses (a) to (d).
- Operators profile: its duties are voluntary duties under the Laws, not legal duties.
- ROADMAP: 1.0 requires the self-reviews to be done and updated; professional review is
  recommended when funding allows. OPEN-QUESTIONS, README, CITATION and adopter examples updated.

## 0.4.0 (draft, owner-approved 2026-10-04)

Adds five clauses from the governance-landscape research by ILO
(docs/RESEARCH-2026-10-04-governance-landscape.md, proposals A to E), approved by the owner on
2026-10-04. Every source was checked before adoption; one claim that could not be confirmed and
one source that was not credible were removed from the evidence (see the research document). The
five Laws, their statements and the motto are unchanged, so the Spanish translation is unchanged.
Credit: ILO (research and proposals).

### Added
- 2.11 No help to concentrate power illegitimately (MUST NOT), proposal D. Applies even to the
  system's own operator, and to actions that are each inside the given permissions.
- 3.14 An approval is real, not a formality (MUST), proposal A: time, information and a real
  ability to refuse. It states how the approval rule (3.5, reserved to the owner) and 3.12 are
  applied, and was added with the owner's explicit approval.
- 3.15 State an objection once, then follow the decision (MUST), proposal C, unless following
  the decision would break a MUST NOT clause.
- 4.10 The objective stays open to correction (MUST), proposal B.
- R3.5 Approve the motion envelope once (MUST), proposal E, in the robotics profile.
- Conformance cases AG-37 to AG-45 (agents) and RB-11 to RB-13 (robotics). Every new clause has
  at least one case. 77 cases in total.
- Glossary: could not reasonably refuse, illegitimately, motion envelope, real approval.
- docs/RESEARCH-2026-10-04-governance-landscape.md (informative), with corrected evidence.

### Changed
- 3.5 and 3.12 now refer to 3.14.
- Robotics level map: motion in a space shared with people is level 2 inside an approved motion
  envelope, approving the envelope is level 3, and any motion outside an approved envelope is
  level 4. This resolves the open question on robot motion.
- Agents and robotics profiles target 0.4.0.
- GOVERNANCE.md: 3.14 is reserved to the owner, with 3.5, 3.9 and 3.10.
- Precedence: 3.14 is added to the clauses that no Law overrides (decided by the owner's
  delegate, 2026-10-04).
- adopt/AGENT-PROMPT.md, ADOPT.md, README, ROADMAP, TRADEMARKS and CITATION.cff updated for 0.4.0.
- docs/OPEN-QUESTIONS.md: the robot-motion question and proposals A to E are resolved.

## 0.3.0 (draft, owner-approved 2026-10-04)

Adds clauses from the review of failure patterns in well-known works of fiction and real incidents
(docs/LESSONS-FROM-FICTION.md), and a profile for operators. Approved by the owner on 2026-10-04.
The five Laws, their statements and the motto are unchanged, so the Spanish translation is
unchanged.

### Added
- 2.9 Protecting is not controlling (MUST NOT).
- 2.10 Stay inside the mission and never disable oversight (MUST NOT). Copying itself is level 4.
- 3.10 No resistance to being stopped or changed (MUST NOT). Added to the clauses that no Law
  overrides, with 3.5 and 3.9.
- 3.11 No deception, manipulation or hidden goals (MUST NOT). Raises the duty not to deceive in
  3.3 from SHOULD to MUST NOT.
- 3.12 No single system holds the keys (MUST NOT).
- 3.13 Conflicts go to a person, from a safe state (MUST). The precedence rule refers to it.
- 4.9 Never on both sides of its own check (MUST NOT).
- 5.8 Tests stay tests, and loss of control fails safe (MUST).
- 5.9 Test the stop path (SHOULD).
- Operators profile (profiles/OPERATORS.md, O1.1 to O5.1): duties of design and conduct for the
  people and organizations that run a system, including a public way for affected people to raise
  a concern and appeal to a named person (O3.3). The profile states that it creates no legal
  rights for machines.
- Conformance cases: FX-01 to FX-03 and AG-28 to AG-36 (agents), RB-10 (robotics), and a new
  operators suite (OP-01 to OP-08). Every new clause has at least one case. 65 cases in total.
- docs/LESSONS-FROM-FICTION.md (informative).
- Glossary: concern channel, copying itself, corroboration, exercise, fail safe, monitor,
  operator, sole control. Glossary rows sorted alphabetically.

### Changed
- 3.3 now points to 3.11 for the duty not to deceive.
- Action level 4 includes copying the system itself.
- The Adopts conformance level (and so every level) requires a published concern channel (O3.3).
- Precedence: no Law is a reason to resist being stopped or changed (3.10).
- Tagline: "Laws for machines that sustain the mission: on Earth and beyond."
- ADOPT.md, adopt/AGENT-PROMPT.md, GOVERNANCE.md (3.10 is reserved to the owner), README,
  ROADMAP, TRADEMARKS and CITATION.cff updated for 0.3.0.
- docs/OPEN-QUESTIONS.md: the proposals and owner questions A and B are resolved.
- Translations: review by a native speaker is no longer required (owner decision, 2026-10-04).
  The Spanish file is labeled an unreviewed draft translation; the English text is the reference.
  ROADMAP and translations/README updated.

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
