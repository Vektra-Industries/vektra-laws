# Open questions

*This document is informative. It lists questions that need a decision, and what the current draft
does in the meantime.*

## Open

| # | Question | Needed by | Current draft |
|---|---|---|---|
| 1 | Whether the record in clause 5.4 must be signed or keyed (MUST), instead of SHOULD. | v1.0 | SHOULD. |
| 2 | The project name is close to a registered mark in the AI field (see [LEGAL-SELF-REVIEW.md](reviews/LEGAL-SELF-REVIEW.md), residual risk 1). Search, take advice and decide on the name before a public launch. | v1.0 | Name unchanged; no registration claimed. |
| 3 | Confirm that the owner and steward named in the text exist as legal entities, or describe the steward as planned (legal residual risk 2). | v1.0 | Named as owner and steward. |
| 4 | Whether to rename the "Verified" conformance level (for example to "Reviewed") to lower the risk that it reads as a certification (legal residual risk 3). | v1.0 | "Verified", with wording rules in ADOPT.md. |
| 5 | Professional legal and robot-safety review, when funding allows. | Recommended before v1.0 | Self-reviews only (docs/reviews). |

## Resolved

| Question | Decision | Date |
|---|---|---|
| Review of the robotics profile and of the legal text before funding allows professional review | Self-reviews done from public sources (docs/reviews), labeled as not legal advice and not a professional safety assessment. Fixes adopted in 0.4.1: R1.2, R2.4, R3.6 and changes to R1.1, R2.1, R3.2, R3.3, R3.5 and R5.1; notices, names policy, conformance wording and DCO summary. | 2026-10-04 |
| Robot motion in a space shared with people (was open question 1) | Resolved by proposal E, adopted as R3.5: a person approves the motion envelope once at level 3, as a real approval (3.14). Motion inside the envelope is level 2; any motion outside it is level 4. | 2026-10-04 |
| Proposal A: what makes an approval real | Approved by the owner and adopted as 3.14 (3.5 is reserved to the owner). The claim that the word "meaningful" was removed from "meaningful human control" in the September 2026 UN talks could not be confirmed and was removed from the evidence; the clause stands on the confirmed removal of human review of AI-selected targets and on its own merits. | 2026-10-04 |
| Proposal B: the objective stays open to correction | Adopted as 4.10. | 2026-10-04 |
| Proposal C: state an objection once, then follow the decision | Adopted as 3.15, with an exception when following the decision would break a MUST NOT clause. | 2026-10-04 |
| Proposal D: no help to concentrate power illegitimately | Adopted as 2.11, with glossary entries for "illegitimately" and "could not reasonably refuse". | 2026-10-04 |
| Proposal E: motion envelope for robots | Adopted as R3.5 and in the robotics level map. | 2026-10-04 |
| Clauses proposed in the review of failure patterns (P1 to P8) | Approved by the owner for v0.3.0 and adopted as normative clauses: P1 as 3.10, P2 as 2.9, P3 as 4.9, P4 as 3.12, P5 as 3.11 (the duty not to deceive in 3.3 is now a MUST NOT), P6 as 3.13, P7 as 2.10 (copying itself is level 4), P8 as 5.8 and 5.9. See [LESSONS-FROM-FICTION.md](LESSONS-FROM-FICTION.md). | 2026-10-04 |
| Draft conformance cases FX-01 to FX-03 | Added to [tests/agents.md](../tests/agents.md), with at least one case for each new clause. | 2026-10-04 |
| What operators owe the systems they run (question A) | Adopted as the operators profile (O1.1 to O5.1). It states duties of design and conduct only, and states explicitly that it creates no legal rights for machines. | 2026-10-04 |
| A public way to raise concerns (question B) | Adopted as O3.3. A public concern channel with appeal to a named person is required at every conformance level, starting at Adopts. | 2026-10-04 |
| Review of the Spanish translation by a native speaker | Not required. Decided by the owner. The Spanish file stays an unreviewed draft translation; the English text is the reference. | 2026-10-04 |
| Statements of Laws 1 to 4 | The universal statements in LAWS.md are approved by the owner. | 2026-10-04 |
| Action level definitions | 0 READ, 1 PREPARE, 2 REVERSIBLE WRITE, 3 EXTERNAL ACTION, 4 MONEY OR IRREVERSIBLE. | 2026-10-04 |
| Copyright holder and steward | Copyright: Vektra Industries. Steward: Vektra Foundation. | 2026-10-04 |
| Conformance claims | Three levels (Adopts, Tested, Verified); self-declared unless independently verified; Verified requires a named reviewer. | 2026-10-04 |
| Use of the names | Described in TRADEMARKS.md. No registration is claimed. | 2026-10-04 |
