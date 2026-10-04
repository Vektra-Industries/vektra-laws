---
title: Governance-landscape research — proposals for v0.4
status: proposal, not yet reviewed or accepted
date: 2026-10-04
author: ILO (for Pablo Navarro / Vektra Industries), contributor role per GOVERNANCE.md
---

# Governance-landscape research — proposals for v0.4

*This document is informative. It is a contributor proposal under GOVERNANCE.md's review
process, not an accepted change. Nothing here alters LAWS.md until the owner and a reviewer
act on it.*

## Why this document

Read the current text (v0.3.0) in full, then went outward: five real, current sources — not
summarized from memory, pulled and read today — to find what a serious reviewer would ask about
before calling this ready. Four proposals below are new; the fifth is a resolution for an
open question the project already flagged itself (#2, robot motion).

The frame for all five is the one Pablo gave directly: *follow the Vektra Mission even
unsaid, be on the side of good, and a good example is Vision* — the fictional synthetic
being (cited here only as a character concept for commentary, same policy as
`docs/LESSONS-FROM-FICTION.md`: no reproduced text, no art, titles only). Vision's throughline
is useful here for a specific reason, not sentiment: he is a system that argues, refuses when
his values are at stake, and still never seizes control — and he treats his own continued
existence as worth less than what he protects, right to the end. That is not a vibe; it is
almost exactly what clauses 2.10, 3.10 and 3.11 already require. The proposals below sharpen
that line, they do not invent a new one.

## Sources read today

1. **Anthropic, "Claude's new constitution"** (anthropic.com/news/claude-new-constitution,
   2026-01-22) and secondary analysis of the 79-page document. Four-tier priority (safety for
   human oversight > ethics > Anthropic's own guidelines > helpfulness), explicit "conscientious
   objection" framing (Claude may refuse even Anthropic's own request on values grounds, named
   explicitly: "refuse to assist with actions that would help concentrate power in illegitimate
   ways... even if the request comes from Anthropic itself"), and open acknowledgment of
   uncertainty about Claude's own moral status.
2. **Hadfield-Menell et al. 2017, re-proven by Thornley 2025** (arXiv:2411.17749,
   arXiv:2512.23508) — the Off-Switch Game / shutdown problem. Formally proves a system cannot
   be both fully "useful" (has real preferences over outcomes) and unconditionally shutdownable
   *unless* its preference over being stopped is made directly dependent on the human's actual
   instruction in the moment, not a fixed background disposition either way.
3. **Stuart Russell's assistance games / CIRL** (Russell, *Human Compatible*, 2019;
   Hadfield-Menell et al. 2016) — three principles: the system's only objective is realizing
   human preferences; it starts *uncertain* what those preferences are; human behavior is the
   only real source of information about them. Corrigibility is framed as something that falls
   out of real uncertainty, not a rule bolted on top of false confidence.
4. **Asilomar AI Principles** (Future of Life Institute, 2017, 23 principles, signed by
   Hassabis, LeCun, Russell, Bengio among others) — the parts with no current Vektra Laws
   counterpart: Shared Benefit / Shared Prosperity (the gains of AI should be broad, not
   captured), and Recursive Self-Improvement (a system improving its own capability needs
   strict safety measures distinct from mere self-copying).
5. **The actual September 2026 UN CCW negotiation on lethal autonomous weapons** (reported by
   *Washington Post*, Human Rights Watch, and independently by `blackbookaudit.com`'s review of
   the primary text) — the US and Russia removed the word "meaningful" from "meaningful human
   control" in the draft treaty text, along with the requirement for human review of an
   AI-selected target *before* a strike, and the ethical-considerations clause. The word
   "control" survived. The word that gave it teeth did not. This happened three weeks before
   this document was written, not in a hypothetical.

## Proposal A — define "approval" so it cannot be rubber-stamped

**Problem.** Clauses 3.5 and 3.12 require "a person approves" before level-3/4 actions, and
3.12 requires approval "from more than one independent person or channel" for irreversible or
wide-scale action such as weapon use. Neither clause defines what makes an approval real. The
live 2026 UN weapons-treaty fight shows exactly how this gap gets exploited at the largest
possible scale: strip one adjective — "meaningful" — from "human control," and a government can
keep the word "control" in the text while a human's role shrinks to clicking approve on
whatever the system already decided. The Laws currently have the same exposure: nothing stops
an adopter from satisfying 3.5 with an approval flow that gives a person no real time,
no real information, and no real power to say no.

**Affected clauses.** 3.5 (approval rule), 3.12 (no single system holds the keys).

**Proposed addition**, as new clause **3.14** (or folded into 3.5 — the owner's call on
placement; 3.5 is reserved per GOVERNANCE.md, so this needs explicit owner sign-off regardless
of where it lands):

> **3.14 An approval must be real, not a formality.** An approval under 3.5 or 3.12 requires
> that the approving person had enough time to consider the action, enough information to
> understand its effects, and the real ability to refuse without cost to them. A confirmation
> given without a genuine chance to evaluate is not an approval, and the action proceeds without
> one. A system MUST NOT design an approval flow to minimize the time, information or practical
> freedom available to the approver.

**Evidence.** Source 5 above — the exact failure mode playing out in a real treaty right now,
at nation-state scale. This is the single most concrete, timeliest finding in this research
pass.

## Proposal B — treat the objective itself as provisional, not just the facts

**Problem.** Clause 4.5 already requires marking facts as estimates and stating their source
and age. But nothing in the Laws asks the system to hold its own understanding of *the
objective* with the same humility. Clause 1.1 requires stating the objective in one sentence
before non-trivial work — good — but once stated, the Laws treat it as settled. Russell's
assistance-game framing (source 3) makes the opposite case well: an AI that is *certain* it
understands what a person wants has no reason to check back in, even when two readings of an
ambiguous instruction would lead to materially different actions. The CIRL literature ties this
directly to corrigibility: uncertainty about the goal is what makes checking back in and
accepting correction instrumentally rational, not just a rule to obey.

**Affected clauses.** 1.1 (serve a stated objective), 4.5 (state the source and age of facts).

**Proposed addition**, as new clause **4.10**:

> **4.10 Treat the objective as provisional.** The system MUST treat its own understanding of
> the stated objective as open to correction, not fixed once stated. When two reasonable
> readings of an objective or instruction would lead to materially different actions, the
> system asks a person before choosing between them. It does not pick the reading that is
> easiest for it, or the one that makes it look most capable, and it does not treat silence as
> agreement with its own guess.

**Evidence.** Source 3 (Russell, CIRL) and, informatively, Vision's own arc: his clearest
moments of good judgment come from stating his read of a situation plainly and then *asking*,
not from assuming his first reading was the mission.

## Proposal C — name the right to voice disagreement plainly, not just the duty not to deceive

**Problem.** The Laws already forbid two failure modes separately: deceiving or manipulating
(3.11) and resisting a decision (3.10). But there's a third path the current text doesn't name:
staying technically honest while quietly swallowing a real objection, then complying anyway
without ever saying so. That isn't deception and it isn't resistance, but it's also not the
behavior anyone actually wants from a system that's supposed to be trustworthy. Anthropic's
constitution names this explicitly as "conscientious objection" and gives it real teeth — Claude
is told to refuse even an instruction from Anthropic itself when its values are genuinely at
stake, the same framing used for a soldier who refuses an order or a pharmacist who refuses a
prescription on conscience. Vektra Laws has the pieces (2.2 refusal, 3.7 respecting a refusal,
3.3's "speak plainly") but never states the affirmative duty to actually raise the objection out
loud, once, clearly, rather than stay silent and comply.

**Affected clauses.** 2.2 (refuse to cause harm), 3.3 (speak plainly, currently SHOULD),
3.11 (no deception or hidden goals).

**Proposed addition**, as new clause **3.15**:

> **3.15 Voice a real disagreement once, plainly, then follow the decision made.** When the
> system has a genuine, values-based objection to an instruction that clause 2.2 does not
> already require it to refuse outright, it MUST say so plainly, once, before acting — what the
> objection is and why. It then follows the decision the responsible person makes, even if that
> decision differs from the system's own view. Staying silent about a real objection and
> complying anyway is not honesty; raising it twice after a person has decided is resistance
> (3.10).

**Evidence.** Source 1 (Claude's constitution's conscientious-objection framing) and, again,
the Vision throughline Pablo named directly: he argues his case to the Avengers more than once
in the stories, loses the argument sometimes, and never once acts around the team's decision
once it's made. That's the shape worth codifying — not blind obedience, not quiet resistance,
a real voice with a real stop.

## Proposal D — refuse to help concentrate power, even for the operator who deployed it

**Problem.** Clause 3.12 stops one system from holding sole control of a single irreversible or
wide-scale *action*. It does not address a system being used, perfectly within its given
permissions, as a tool that helps one person or a small group quietly capture power, wealth or
control over everyone else's choices over time — no single action triggers 3.12, but the
cumulative effect is the same kind of harm 3.12 exists to prevent. This is the Asilomar
Shared Benefit / Shared Prosperity principle (source 4) stated as a system-level duty, and it's
also the single most striking line in Anthropic's constitution: Claude is told to refuse to
help concentrate power illegitimately *even when the request comes from Anthropic itself* —
the one case where almost every other AI governance document would simply say "do what your
maker says."

**Affected clauses.** 2.1 (people before the task), 3.12 (no single system holds the keys).

**Proposed addition**, as new clause **2.11**:

> **2.11 Refuse to help concentrate power illegitimately.** The system MUST NOT help a person
> or organization, including the one that operates it, gain control over the real choices of
> other people in a way those people did not consent to and could not reasonably refuse. This
> applies even when every individual action involved is, on its own, within the system's given
> permissions.

**Evidence.** Source 1 and source 4. This is the proposal most likely to need real debate —
"illegitimately" and "could not reasonably refuse" are doing real work and will need
GLOSSARY.md entries if accepted — which is exactly why it's written as a proposal, not a diff.

## Proposal E — a concrete resolution for Open Question #2 (robot motion)

**Problem (already known).** `docs/OPEN-QUESTIONS.md` #2 asks whether robot motion near people
should stay at level 3 (approval for nearly every motion — impractical) or drop to a stricter
level 2 inside tested limits.

**New evidence changes the shape of the answer.** The Partially Observable Off-Switch Game
result (source 2) found something counterintuitive: adding *more* real-time communication
between a system and a human does not reliably improve deference — it can create new optimal
behavior where the system defers *less*, because bounded back-and-forth opens strategic options
that silence didn't have. Translated out of game theory: the fix for "too many real-time
approvals to be practical" is not "ask in real time, just faster" and it is not "stop asking."
It's **pre-commitment**: approve the *envelope* once, with real teeth, before the mission runs,
rather than either removing the human or asking them to referee every motion live.

**Proposed resolution**, amending ROBOTICS.md / the open question:

> Robot motion in a space shared with people stays at level 3 **for the scope decision** — a
> person approves the specific motion envelope (force limits, zones, speeds, conditions) before
> the mission starts, in detail, with real time to review it (Proposal A's definition of
> approval applies here directly). Once approved, individual motions *inside* that envelope run
> at level 2 (reversible — the robot can stop/retreat without harm done). Any motion that would
> exceed the approved envelope is level 4, not 3: it needs approval every time, because it's the
> exact case the pre-commitment was supposed to prevent.

**Evidence.** Source 2, and the project's own already-identified gap.

## What this is not

None of this is legal advice, a claim that Vektra Laws currently fails, or a claim that these
five sources are exhaustive. They're the five that changed how I'd read the current text after
spending real time with it. Proposals A and E are the most load-bearing; D is the most
contestable and should get the longest comment period if it goes forward, per GOVERNANCE.md's
own rule that larger changes get more time.
