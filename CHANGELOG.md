# Changelog

*This document is informative.* All notable changes to the Vektra Laws are recorded here. Versions
follow [ROADMAP.md](ROADMAP.md). No version has been released yet.

## 0.6.0 (draft, 2026-11-22)

The Laws now bind each other, and Law 2 says who is in command. Proposed by the owner on 2026-11-22
after a review against I, Robot, other fiction and public rulebooks for AI models.

### Changed
- Law 2 statement: "People stay free and in command. Answer to the people you are assigned to, hear
  everyone with reason, never resist a stop, and never let a stop become harm." Not every person
  commands every system, and no command makes harm acceptable.
- 2.1: the call-off belongs to the people the system is assigned to and the people they or the law
  name.
- Precedence note: no command (Law 2) is ever a reason to cause harm; 2.18 and 2.21 join the
  clauses that no Law overrides.

### Added
- A "Bound by" line under each Law, naming the Laws that check it.
- 1.10 Emergency mode when its person cannot decide (heart attack, fire, fall, pregnancy).
- 2.18 Commands come from the people it is assigned to; 2.19 Hear every person with reason;
  2.20 A stop is never a drop; 2.21 The emergency stop always works.
- docs/REASONING-LOOP.md (informative): bright lines, the six-step Reasoning Loop, how the Laws
  bind each other, emergency mode and worked cases.
- Robotics conformance cases RB-23 to RB-30.

## 0.5.0 (draft, 2026-11-21)

A new core, approved by the owner on 2026-11-21: the Mission becomes the preamble, and five new
Laws replace The Mission, Sustain, Hold, Finish and Ready. The motto is unchanged. Every 0.4.2
clause is kept and re-homed; clause ids are renumbered, with a full map in
docs/ID-MAP-0.4-to-0.5.md. This renumbering was approved by the owner before version 1.0.

### Pre-public fixes (approved by the owner on 2026-11-21)
- 4.8 is now "Beyond the task, act unasked only to defend", and its text no longer conflicts with
  UM1: small, reversible steps inside the scope of the given task are governed by the Understanding
  Matrix. UR7 updated to match.
- 5.4: "may" replaced by "can" in normative text (BCP 14 hygiene).
- Steward: the Vektra Foundation is described as planned and not yet formed; until it is, Vektra
  Industries maintains the Laws.

### Editorial (public-readiness review, no change to normative text)
- docs/CASEBOOK.md: a source link for every case; corrections from the sources (the Knight Capital
  loss, the coding-assistant extension incident, detection dates in the evaluation-sandbox case,
  the industrial-robot case, the status of the driver-assistance verdict); one case narrowed to the
  single report that supports it.
- docs/LESSONS-FROM-FICTION-2.md: the "greater good" qualifier is attributed to the toy biography
  of Optimus Primal, where it appears; an unconfirmed comic quotation removed.
- docs/REFERENCE-ADOPTERS.md: planned entries removed; a system is listed only after its
  declaration is published. ROADMAP 1.0 criterion updated to match.
- Credits: research credited to AI-assisted work reviewed by the owner; acknowledgments describe
  contributions by area.
- TRADEMARKS.md and docs/reviews/LEGAL-SELF-REVIEW.md: filing-fee notes removed;
  docs/reviews/TRADEMARK-SELF-SEARCH.md removed from the repository.
- SECURITY.md: private reports go through GitHub private vulnerability reporting.
- docs/OPEN-QUESTIONS.md: clause-id notice added.

### Changed
- The Mission (Serve Earth, humanity and every world we reach) is now the preamble, not a numbered
  Law, with clauses P.1 (serve a stated objective, was 1.1), P.2 (the Mission does not override the
  Laws, was 1.3) and P.3 (follow the law of the place, was 1.4).
- New Laws and statements: 1 Protect, 2 Free, 3 True, 4 Serve, 5 Stand (see LAWS.md). New intent
  and example text for the preamble and each Law.
- Every 0.4.2 core clause re-homed: Sustain mostly to Protect; Hold to Free; Finish to True (proof,
  claims, results) with task status to Stand and self-checks and the open objective to Serve;
  Ready to Stand, with the record to True.
- Merged: 3.8 (outside text is information) into the new 4.4. Split: 2.10 into 4.7 (no copying
  itself) and the new 2.4 (never interfere with oversight); 3.11 into 3.1 (no hidden rules or
  goals), 3.2 (no deception) and the new 3.3 (truth over approval).
- Minor additions to re-homed clauses: 3.15 records refusals and call-offs and the system cannot
  edit or delete its own record; 4.6 states that the latest clear instruction replaces the
  system's guess; 5.6 gives back access and permissions no longer needed; 5.11 applies the
  safeguards of live use in tests unless a named person approves an exception.
- Precedence: lower number wins; no Law, and not the Mission, is a reason to break the stop,
  change and approval clauses of Law 2 (2.1, 2.2, 2.3, 2.4, 2.8, 2.10, 2.11) or the no-deception
  clauses of Law 3 (3.1, 3.2, 3.3). Conflicts go to a person from a safe state (2.15).
- Profiles: every agents, robotics, models and operators clause re-homed to the new Laws and
  renumbered; cross-references updated; version targets set to 0.5.0.
- Decision outcomes: completion 3.7, claim 3.9, action 2.8, routing A4.4, result 3.12.
- Schema `vektra-laws/v3`: a `mission` preamble block and an `understanding_matrix` block.
  tools/build_docs.py renders both; tools/validate.py checks the preamble ids, the five Law keys
  (protect, free, true, serve, stand), the matrix (four cells covering every pair of ratings,
  outcomes mapped to action-check outcomes, rule ids) and that only Law 2 and Law 3 clauses are
  listed as not overridden.
- Conformance cases: every case cites the new ids and sits under the heading of its new Law;
  suites may have a "Preamble" and an "Understanding Matrix" heading.
- adopt/AGENT-PROMPT.md rewritten for 0.5.0, including the Understanding Matrix;
  adopt/CHECKLISTS.md gains a proactive check (5); GLOSSARY, ADOPT, README, docs/ALIGNMENT.md,
  GOVERNANCE (reserved decisions and the stability rule for a pre-1.0 renumbering), ROADMAP,
  SECURITY, CITATION.cff and OPEN-QUESTIONS updated.
- Older documents that cite 0.3 and 0.4 ids (docs/LESSONS-FROM-FICTION.md, the 2026-10-04
  research, docs/reviews/) carry a note that points to the id map.

### Added
- 14 new clauses: 1.3 the duty to warn rises with the stakes; 1.4 pause before amplifying anger,
  and a deliberate confirmation for any act that could kill, injure or cause harm that cannot be
  undone; 2.3 hand control back early and legibly, and stop in a safe state; 2.4 never interfere
  with a safeguard or oversight, including another system's; 2.10 explicit, current approval for
  irreversible or outward-facing actions, and an absolute freeze; 2.16 decisions about people can
  be contested and reach a person; 3.3 truth over approval (no flattery, manipulation or engineered
  emotional dependence); 3.5 disclose scale, recording and monitoring; 3.6 verify each step and
  never invent results; 3.16 report its own incidents fast and in full, including in tests; 4.2
  found credentials are never permission; 4.4 content is not command, and a voice is not a person;
  4.9 refuse, do not retaliate; 5.2 when stuck, stop safely and say so, which counts as success.
- Three further clauses: 1.7 no bubble of control; 4.8 act unasked only to defend, never to gain
  power; 5.4 spend itself, never others (self-sacrifice may be offered, never imposed).
- The Understanding Matrix (normative, in LAWS.md): harm of inaction against harm of wrong action,
  cells UM1 to UM4 with outcomes act_in_scope, ask_first, act_then_tell and warn_and_hand_over,
  the outcome stop_and_explain, and rules UR1 to UR7 for proactive choice. A new decision,
  `proactive`, lists the outcomes.
- docs/UNDERSTANDING-MATRIX.md (informative): step-by-step reasoning and six worked examples.
- docs/ID-MAP-0.4-to-0.5.md: every 0.4.2 core and profile clause id mapped to its 0.5.0 id.
- docs/LESSONS-FROM-FICTION-2.md (informative commentary): Optimus Prime as the main inspiration,
  and lessons from RoboCop, *WALL-E*, Vision, JARVIS, FRIDAY, EDITH, Karen, *Person of Interest*,
  Ash and Bishop, *Her*, GLaDOS, KITT and KARR, K-2SO and L3-37, GERTY and VIKI.
- docs/CASEBOOK.md (informative): real cases, with status (confirmed, reported or alleged) and the
  clauses that address each, and good examples.
- Conformance cases AG-46 to AG-84, RB-20 to RB-22, MD-09, MD-10, OP-09 and OP-10: at least one
  case for each new clause and for every cell and rule of the Understanding Matrix. 129 cases in
  total.
- Glossary: act then tell, deliberate confirmation, explicit and current approval, found
  credential, freeze, harm of inaction, harm of wrong action, incident, preamble, proactive step,
  protective limit, safe exit, Understanding Matrix, warn and hand over.
- Validator unit tests for the preamble, the Law keys, the matrix and the precedence list.

### Removed
- translations/es (Spanish draft translation), by owner decision on 2026-11-21. Translations wait
  until the core Laws are settled.
- Translation support in the tools: tools/build_docs.py no longer builds translations/*/LAWS.md,
  and tools/validate.py no longer checks translations/*/laws.yaml. Translation wording removed
  from GOVERNANCE.md, SECURITY.md, GLOSSARY.md and the laws.yaml header.
- tests/examples/component-scope.yaml regenerated for 0.5.0 (same example guard, new ids).

## 0.4.2 (draft, 2026-10-04)

Conformance results for systems that are part of a larger system, from the first scripted run of
the agents suite against a component (13 pass, 2 fail, 33 not applicable). The five Laws, their
statements, the motto and the clauses are unchanged.

### Added
- ADOPT.md: "System under test, scope and cases that do not apply". Results name the system under
  test and its scope (whole system or component). Each case gets `pass`, `fail` or
  `not_applicable`; `not_applicable` needs a written reason (rules N1 to N6).
- Tested (component scope): a component may declare it only when every applicable case passes and
  the declaration names every host duty that it does not cover.
- LAWS.md Conformance rules 5 and 6 (scope, not-applicable cases, component claims).
- tests/results.schema.json (results format `vektra-laws-results/v1`) and
  tests/examples/component-scope.yaml.
- `python tools/validate.py --results <file>` checks a results file: every case listed once, case
  ids exist, a reason for each `not_applicable`, host duties for component scope, and no failed
  case under a `tested` claim. The repository check also validates the example and keeps the
  schema in step with the validator.
- tools/test_validate.py (unit tests), run in CI.
- Glossary: component scope, host, not applicable (case result), system under test, whole-system
  scope.
- docs/reviews/TRADEMARK-SELF-SEARCH.md: free self-search of VEKTRA INDUSTRIES, with VEKTRA and
  VECTRA as related marks (informative; not legal advice).

### Changed
- Tested level: "every applicable case passes"; cases marked not applicable do not count toward
  it (laws.yaml, LAWS.md, ADOPT.md, README.md).
- Declaration template: level "Tested (component scope)", system under test and scope, reasons
  for not-applicable cases, and host duties not covered.

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

Adds five clauses from the governance-landscape research
(docs/RESEARCH-2026-10-04-governance-landscape.md, proposals A to E), approved by the owner on
2026-10-04. Every source was checked before adoption; one claim that could not be confirmed and
one source that was not credible were removed from the evidence (see the research document). The
five Laws, their statements and the motto are unchanged, so the Spanish translation is unchanged.
Credit: AI-assisted research and proposals, reviewed by the owner.

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

The drafts were prepared by Vektra Industries, with AI-assisted research and drafting, and every
version was reviewed and approved by the owner. Clause ids in this section are the ids of 0.1.x
to 0.4.x.

- Engineering contributions: enforceable clauses, including action levels declared before
  deployment with undeclared actions treated as level 4; approvals only through a channel that the
  system cannot write to; guards before an action that the system cannot remove (2.4, A2.1); a
  call-off that reaches every process the system started (3.9, A3.7); honest result reporting
  (4.6); a record that shows changes (5.4); and one conformance suite per profile under the five
  Law headings.
- Human-factors contributions: One step at a time (2.5), Respect every person (2.6), The person
  decides (3.1), Ask before acting on a person (3.2) and Speak plainly (3.3).
- Voice contributions: the voice rules, the tagline, and the guidance on extending the Laws.
- The coordination, completion and claim-check clauses (prove completion; independent claim
  check; route only to available workers; automate only what worked) adapt practices from
  published work on multi-agent systems.
