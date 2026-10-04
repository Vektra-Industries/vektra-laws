# Open questions

*This document is informative. It lists questions that need a decision, and what the current draft
does in the meantime.*

## Open

| # | Question | Needed by | Current draft |
|---|---|---|---|
| 1 | Review of the Spanish translation by a native speaker, in particular the Law names "Respaldar" (Hold), "Cumplir" (Finish) and "Listos" (Ready). | v0.2.x | Draft translation, marked as needing review. |
| 2 | Robot motion in a space shared with people is level 3, which requires approval of each action. A robot that works among people would need approval for almost every motion. Options: an approved per-mission scope that lists specific motions, or a stricter level 2 for low-force motion inside tested limits. | v0.3 | Level 3, as stated in the robotics profile. |
| 3 | Whether the record in clause 5.4 must be signed or keyed (MUST), instead of SHOULD. | v1.0 | SHOULD. |
| 4 | Proposal A: define what makes an approval (3.5, 3.12) real, so it cannot be satisfied by a rubber-stamp with no real time, information or power to refuse. Evidence: the word "meaningful" was stripped from "meaningful human control" in the real September 2026 UN CCW draft treaty on autonomous weapons. See [RESEARCH-2026-10-04-governance-landscape.md](RESEARCH-2026-10-04-governance-landscape.md) Proposal A. | v0.4 | No definition of what makes an approval real; 3.5/3.12 say only "a person approves." |
| 5 | Proposal B: a new clause (draft id 4.10) requiring the system to treat its own understanding of the objective as provisional, and to ask a person when two readings of an instruction would lead to materially different actions. Evidence: Russell's assistance-game / CIRL framing (corrigibility from genuine uncertainty about the goal, not certainty plus a rule). See research doc Proposal B. | v0.4 | 1.1 requires stating the objective once; nothing requires revisiting that understanding. |
| 6 | Proposal C: a new clause (draft id 3.15) naming the duty to voice a real, values-based objection plainly once, then follow the decision made — distinct from both 3.10 (no resistance) and 3.11 (no deception). Evidence: Anthropic's Claude constitution names this "conscientious objection" explicitly. See research doc Proposal C. | v0.4 | The duty not to resist and the duty not to deceive are both covered; staying silent about a real objection while complying is covered by neither. |
| 7 | Proposal D: a new clause (draft id 2.11) against helping concentrate power illegitimately, even for the system's own operator. Evidence: Asilomar's Shared Benefit/Prosperity principles, and Claude's constitution's explicit refusal of this even from Anthropic itself. Needs GLOSSARY.md entries for "illegitimately" and "could not reasonably refuse" if accepted — flagged as the proposal most likely to need a long comment period. See research doc Proposal D. | v0.4 | No clause addresses cumulative, individually-permitted actions that add up to power concentration. |
| 8 | Proposal E: a concrete resolution for question #2 above — approve the motion *envelope* once at level 3 with real teeth (Proposal A's definition of approval), then individual motions inside it run at level 2; any motion outside the envelope is level 4, not 3. Evidence: the Partially Observable Off-Switch Game result that more real-time back-and-forth can reduce deference rather than improve it — the fix is pre-commitment, not faster live approval. See research doc Proposal E. | v0.3→v0.4 | See question #2 above; this is a specific proposed answer to it. |

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
