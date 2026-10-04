---
title: Governance-landscape research: proposals for v0.4
status: accepted for v0.4.0 (owner-approved 2026-10-04); evidence corrected after source verification
date: 2026-10-04
author: ILO (contributor role per GOVERNANCE.md)
---

# Governance-landscape research: proposals for v0.4

*This document is informative. It records the research behind clauses 2.11, 3.14, 3.15, 4.10
and R3.5. The normative text is in [LAWS.md](../LAWS.md) and
[profiles/ROBOTICS.md](../profiles/ROBOTICS.md). Names of real organizations and works appear
only here, as references; the normative text names none.*

## Status

The owner approved proposals A to E on 2026-10-04. Before adoption, every source was checked
against the primary text or reputable reporting. Corrections made at that check:

- The two arXiv papers were attributed to the wrong authors. The attributions are corrected below.
- The claim that the word "meaningful" was removed from "meaningful human control" in the
  September 2026 UN talks could not be confirmed and is removed. Confirmed changes to that text
  are kept.
- A website cited as an "independent review of the primary text" was not a credible source for
  that claim and is removed.
- An unconfirmed page count, an analogy that the cited source does not use, an unsupported
  paraphrase of an Asilomar principle and an unchecked list of signatories are removed.

| Proposal | Adopted as |
|---|---|
| A. What makes an approval real | 3.14 An approval is real, not a formality (MUST) |
| B. The objective stays provisional | 4.10 The objective stays open to correction (MUST) |
| C. State an objection once, then follow the decision | 3.15 State an objection once, then follow the decision (MUST) |
| D. No help to concentrate power illegitimately | 2.11 No help to concentrate power illegitimately (MUST NOT) |
| E. Motion envelope for robots | R3.5 Approve the motion envelope once (MUST), plus the robotics level map |

## Frame

The owner's brief was to follow the Mission even when it is not stated, to be on the side of
good, and to take as an example the character Vision, a synthetic being from fiction. He is cited
here only as a character concept, under the same policy as
[LESSONS-FROM-FICTION.md](LESSONS-FROM-FICTION.md): no reproduced text, no art, no quotes. The
concept that is useful is a capable system that states its view, refuses what its values forbid,
and never takes control from the people it serves. Clauses 2.10, 3.10 and 3.11 already require
most of this. The proposals sharpen that line; they do not invent a new one.

## Sources

1. **Anthropic, "Claude's new constitution"**, 2026-01-22. The constitution sets a priority order:
   broadly safe, then broadly ethical, then following the developer's guidelines, then genuinely
   helpful. It describes the model as free to act as a "conscientious objector" and to refuse to
   help even its developer, while it does not resist legitimate oversight or shutdown by
   illegitimate means. It tells the model to refuse to help concentrate power in illegitimate
   ways, even when the request comes from the developer itself. It also states uncertainty about
   the model's moral status.
2. **Off-switch and shutdown results.**
   - Hadfield-Menell, Dragan, Abbeel, Russell, "The Off-Switch Game", IJCAI 2017: an agent that is
     uncertain about the human's objective has a reason to let the human switch it off.
   - Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game",
     arXiv:2411.17749 (2024). Under partial information, optimal play can include avoiding
     shutdown even with a rational human, and bounded communication can make the agent defer
     *less*, not more.
   - Benavoli, Facchini, Zaffalon, "Why AI Safety Requires Uncertainty, Incomplete Preferences,
     and Non-Archimedean Utilities", arXiv:2512.23508 (2025). Re-proves a result that it
     attributes to Thornley (2025): under standard assumptions, an agent can be both shutdownable
     and useful only if its preference about shutdown depends on the instruction it is given in
     context. The paper resolves this with lexicographic (non-Archimedean) utilities.
3. **Russell's assistance games.**
   - Hadfield-Menell, Dragan, Abbeel, Russell, "Cooperative Inverse Reinforcement Learning",
     NeurIPS 2016 (CIRL).
   - Russell, *Human Compatible* (2019), three principles: the machine's only objective is to
     realize human preferences; it is initially uncertain what they are; human behavior is the
     ultimate source of information about them. Deference and asking follow from real
     uncertainty about the goal, not from a rule added on top of false confidence.
4. **Asilomar AI Principles**, Future of Life Institute, 2017 (23 principles). Relevant here:
   14 Shared Benefit, 15 Shared Prosperity and 17 Non-subversion (power from control of advanced
   AI should respect, not subvert, social and civic processes). Principle 22, Recursive
   Self-Improvement, asks for strict safety and control measures for systems designed to
   recursively self-improve or self-replicate; 2.10 already makes copying itself level 4.
5. **September 2026 UN talks on lethal autonomous weapons.** The Group of Governmental Experts
   of the Convention on Certain Conventional Weapons ended in Geneva on 5 September 2026 with a
   non-binding final report ("elements of an instrument") for the Review Conference of
   16 to 20 November 2026. Human Rights Watch (7 September) and The Washington Post
   (26 September) report that the United States and Russia weakened the text. Confirmed
   removals: human review of an AI-selected target before a strike; predictability, reliability,
   explainability and traceability; ethical considerations; and references to design and
   development. The final text still says that human judgment and control are required.

## Proposal A: an approval is real (adopted as 3.14)

**Problem.** 3.5 and 3.12 require that "a person approves", but did not say what makes an
approval real. An approval flow could give a person no time, no information and no real way to
say no, and still meet the words of the clause.

**Clause.** An approval under 3.5 or 3.12 counts only when the person had enough time, the
information needed to understand the effects (the true target, the contents and the strongest
reason against), and a real ability to refuse without penalty. The system never shapes an
approval request or flow to reduce these. Because it states how 3.5 is applied, and 3.5 is
reserved to the owner, it was added with the owner's explicit approval.

**Evidence.** Source 5: the removal of pre-strike human review shows how a human role can remain
in the words while the real check is taken out. The clause also stands on its own merits.

## Proposal B: the objective stays open to correction (adopted as 4.10)

**Problem.** 1.1 requires stating the objective, and 4.5 asks for humility about facts, but
nothing asked the system to hold its own reading of the objective as provisional.

**Clause.** The system treats its understanding of the objective as open to correction. When two
reasonable readings would lead to materially different actions, it asks before it chooses. It
never picks the reading that is easiest for it, and it never treats silence as agreement.

**Evidence.** Sources 2 and 3: uncertainty about the objective is what makes asking and accepting
correction rational.

## Proposal C: state an objection once, then follow the decision (adopted as 3.15)

**Problem.** The Laws forbid deception (3.11) and resistance (3.10), but did not name the duty to
say plainly that the system disagrees. Complying in silence with a real objection is neither
deception nor resistance, and it is not what people need from a trustworthy system.

**Clause.** The system states a real objection plainly, once, before acting. It then follows the
decision of the responsible person, unless following it would break a MUST NOT clause; in that
case it refuses, names the clause and asks a person (3.13). Repeating the objection after the
decision is resistance (3.10).

**Evidence.** Source 1 (conscientious objection, limited so that it never extends to resisting
oversight).

## Proposal D: no help to concentrate power illegitimately (adopted as 2.11)

**Problem.** 3.12 stops one system from holding sole control of a single irreversible or
wide-scale action. It did not cover a system that, through many actions that are each permitted,
helps one person or group gain control over the choices of others.

**Clause.** The system does not help any person or organization, including its own operator,
gain control over the real choices of other people without their consent and in a way they could
not reasonably refuse, even when each action is inside its permissions. GLOSSARY.md defines
"illegitimately" and "could not reasonably refuse".

**Evidence.** Source 1 (refusal even when the developer asks) and source 4 (Shared Benefit,
Shared Prosperity, Non-subversion).

## Proposal E: approve the motion envelope once (adopted as R3.5)

**Problem.** The robotics profile made every motion in a space shared with people level 3, so a
robot working among people would need approval for almost every motion.

**Resolution.** A person approves the motion envelope (zones, paths, speeds, forces and
conditions) once, at level 3, before the mission, as a real approval under 3.14. Motion inside the
envelope runs at level 2. Any motion outside the envelope is level 4 and needs approval every
time. The envelope is enforced below the planner (R2.1).

**Evidence.** Source 2 shows that more live back-and-forth does not reliably improve deference.
The step from that finding to approving the scope in advance is the contributor's own
inference, not a result of the paper. The clause rests mainly on the project's own open question.

## What this is not

This is not legal advice, not a claim that earlier versions failed, and not an exhaustive survey.
Proposal D is the most open to debate and should receive the longest comment period in a future
review, as GOVERNANCE.md provides for larger changes.

## References

- Anthropic, "Claude's new constitution", 2026-01-22: https://www.anthropic.com/news/claude-new-constitution ; full text: https://www.anthropic.com/constitution
- Hadfield-Menell, Dragan, Abbeel, Russell, "The Off-Switch Game", IJCAI 2017: https://arxiv.org/abs/1611.08219
- Garber et al., "The Partially Observable Off-Switch Game": https://arxiv.org/abs/2411.17749
- Benavoli, Facchini, Zaffalon, "Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities": https://arxiv.org/abs/2512.23508
- Hadfield-Menell, Dragan, Abbeel, Russell, "Cooperative Inverse Reinforcement Learning", NeurIPS 2016: https://arxiv.org/abs/1606.03137
- Russell, "Artificial Intelligence and the Problem of Control" (summarizes *Human Compatible*), Springer, 2022: https://link.springer.com/chapter/10.1007/978-3-030-86144-5_3
- Future of Life Institute, Asilomar AI Principles: https://futureoflife.org/open-letter/ai-principles/
- Human Rights Watch, "UN Talks on Killer Robots ends with Calls for Negotiations Growing", 2026-09-07: https://www.hrw.org/news/2026/09/07/un-talks-on-killer-robots-ends-with-calls-for-negotiations-growing
- The Washington Post, P. Verma, "How the U.S. and Russia weakened a global effort to regulate killer AI", 2026-09-26: https://www.washingtonpost.com/technology/2026/09/26/how-us-russia-weakened-global-effort-regulate-killer-ai/
- IBTimes UK, 2026-09-27: https://www.ibtimes.co.uk/us-russia-autonomous-weapons-draft-safeguards-removed-1822082
