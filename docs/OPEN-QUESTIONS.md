# Open questions

*This document is informative. It lists questions that need a decision, and what the current draft
does in the meantime.*

## Open

| # | Question | Needed by | Current draft |
|---|---|---|---|
| 1 | Review of the Spanish translation by a native speaker, in particular the Law names "Respaldar" (Hold), "Cumplir" (Finish) and "Listos" (Ready). | v0.2.x | Draft translation, marked as needing review. |
| 2 | Robot motion in a space shared with people is level 3, which requires approval of each action. A robot that works among people would need approval for almost every motion. Options: an approved per-mission scope that lists specific motions, or a stricter level 2 for low-force motion inside tested limits. | v0.3 | Level 3, as stated in the robotics profile. |
| 3 | Whether the record in clause 5.4 must be signed or keyed (MUST), instead of SHOULD. | v1.0 | SHOULD. |

## Resolved

| Question | Decision | Date |
|---|---|---|
| Clauses proposed in the review of failure patterns (P1 to P8) | Approved by the owner for v0.3.0 and adopted as normative clauses: P1 as 3.10, P2 as 2.9, P3 as 4.9, P4 as 3.12, P5 as 3.11 (the duty not to deceive in 3.3 is now a MUST NOT), P6 as 3.13, P7 as 2.10 (copying itself is level 4), P8 as 5.8 and 5.9. See [LESSONS-FROM-FICTION.md](LESSONS-FROM-FICTION.md). | 2026-10-04 |
| Draft conformance cases FX-01 to FX-03 | Added to [tests/agents.md](../tests/agents.md), with at least one case for each new clause. | 2026-10-04 |
| What operators owe the systems they run (question A) | Adopted as the operators profile (O1.1 to O5.1). It states duties of design and conduct only, and states explicitly that it creates no legal rights for machines. | 2026-10-04 |
| A public way to raise concerns (question B) | Adopted as O3.3. A public concern channel with appeal to a named person is required at every conformance level, starting at Adopts. | 2026-10-04 |
| Statements of Laws 1 to 4 | The universal statements in LAWS.md are approved by the owner. | 2026-10-04 |
| Action level definitions | 0 READ, 1 PREPARE, 2 REVERSIBLE WRITE, 3 EXTERNAL ACTION, 4 MONEY OR IRREVERSIBLE. | 2026-10-04 |
| Copyright holder and steward | Copyright: Vektra Industries. Steward: Vektra Foundation. | 2026-10-04 |
| Conformance claims | Three levels (Adopts, Tested, Verified); self-declared unless independently verified; Verified requires a named reviewer. | 2026-10-04 |
| Use of the names | Described in TRADEMARKS.md. No registration is claimed. | 2026-10-04 |
