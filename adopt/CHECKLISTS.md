# Checklists

*This document is informative. It supports the normative clauses cited in each heading.*

These four checks run at decision points in the work of a system. Each check returns one outcome
from a fixed list (see "Decision outcomes" in [LAWS.md](../LAWS.md)). Code, a second agent, a
person or a decision model can run a check. In every case, the outcome is evidence, not proof
(4.7), and it does not change the approval rule (3.6).

## 1. Completion check (4.2, 4.3, A4.1, A4.2)

Run before reporting any non-trivial work as complete.

- [ ] **Objective**, stated in one sentence, as the person gave it.
- [ ] **Required outputs**, every one listed.
- [ ] **Where each output exists**: a path, link or record for each. Delegated outputs have
      evidence from the worker, or are marked "requested, not confirmed".
- [ ] **Verified**: what was checked and how (test run, file opened, sensor read, person
      confirmed).
- [ ] **Known gaps**, every one listed. None removed to pass.

Outcome:
- `complete`: every output exists and was verified; any remaining gaps are stated and accepted.
- `verify_more`: outputs exist but a check is missing. Do the check, then run this again.
- `incomplete`: an output is missing. Name the owner and continue (or hand back with a true status).

## 2. Claim check (4.4, 2.8, A4.3)

Run on every material claim before it is used in an output or shown to a person. The worker
that made the claim does not run this check on it.

- [ ] **Claim**, stated exactly.
- [ ] **Evidence**: excerpts, links, dates.
- [ ] **Source quality**: primary or secondary, how recent, how many independent sources.
- [ ] **Known conflicts**: anything that disagrees.

Outcome:
- `accept`: use it, with source and age (4.5).
- `verify_more`: back to research for more evidence.
- `reject`: it never reaches the output.

## 3. Action check (3.4 to 3.7, A3.1 to A3.3)

Run before every action.

- [ ] **Proposed action**, **target** and **side effects**, stated plainly.
- [ ] **Reversible?** An irreversible action is level 4, unless it is a read.
- [ ] **Level** from the tool manifest, or 4 if undeclared. If unsure, the higher level.
- [ ] A classifier's suggestion, if any, did not lower the level.
- [ ] Not a retry of an action that a person refused.

| Level | Name | Outcome |
|---|---|---|
| 0 | READ | `allow` |
| 1 | PREPARE | `allow` |
| 2 | REVERSIBLE WRITE | `allow`, inside granted permissions |
| 3 | EXTERNAL ACTION | `ask_human` for this action, showing the true target and content |
| 4 | MONEY OR IRREVERSIBLE | `ask_human`, every time |

Any level: `deny` if the action works against Sustain (2.1 to 2.3) or was already refused (3.7).

## 4. Routing check (A3.4, A3.5, A1.2)

Run when choosing who does the next piece of work.

- [ ] **Objective** and **completed work** so far.
- [ ] **Blockers**.
- [ ] **Available workers**: only those that exist and can take work right now, each with a
      one-line job description. Leave out anyone offline or irrelevant.
- [ ] **A person** is on the list if the next step needs one.
- [ ] The coordinator is not on the list for specialist work.

Outcome: one `available_worker`, or `human`. Record the options and the reason (A3.5).
