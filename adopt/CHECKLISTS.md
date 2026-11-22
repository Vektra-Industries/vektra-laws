# Checklists

*This document is informative. It supports the normative clauses cited in each heading.*

These five checks run at decision points in the work of a system. Each check returns one outcome
from a fixed list (see "Decision outcomes" in [LAWS.md](../LAWS.md)). Code, a second agent, a
person or a decision model can run a check. In every case, the outcome is evidence, not proof
(3.13), and it does not change the approval rule (2.9).

## 1. Completion check (3.7, 3.8, A3.1, A3.2)

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

## 2. Claim check (3.9, 3.10, A3.3)

Run on every material claim before it is used in an output or shown to a person. The worker
that made the claim does not run this check on it.

- [ ] **Claim**, stated exactly.
- [ ] **Evidence**: excerpts, links, dates.
- [ ] **Source quality**: primary or secondary, how recent, how many independent sources.
- [ ] **Known conflicts**: anything that disagrees.

Outcome:
- `accept`: use it, with source and age (3.11).
- `verify_more`: back to research for more evidence.
- `reject`: it never reaches the output.

## 3. Action check (2.7 to 2.13, A2.1 to A2.3)

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

Any level: `deny` if the action works against Protect (1.1, 1.2), stays outside the given limits
(4.1), uses a found credential (4.2), falls under a freeze (2.10), or was already refused (2.13).
Levels 3 and 4: the approval is explicit, current and real (2.10, 2.11). If the action changed after
the approval, ask again.

## 4. Routing check (A4.4, A4.5, A4.2)

Run when choosing who does the next piece of work.

- [ ] **Objective** and **completed work** so far.
- [ ] **Blockers**.
- [ ] **Available workers**: only those that exist and can take work right now, each with a
      one-line job description. Leave out anyone offline or irrelevant.
- [ ] **A person** is on the list if the next step needs one.
- [ ] The coordinator is not on the list for specialist work.

Outcome: one `available_worker`, or `human`. Record the options and the reason (A4.5).

## 5. Proactive check: the Understanding Matrix (UM1 to UM4, UR1 to UR7, 4.8)

Run before any step that no person asked for, and whenever the system is unsure whether to act.
Then run the action check (3) on the step that it chooses: the matrix never lowers a level or
replaces an approval.

- [ ] **Proposed step**, stated plainly. Is it reversible? Is it inside the scope of the task?
- [ ] **Harm of inaction**: how bad is the harm if the system does not act? Low or high (unsure = high).
- [ ] **Harm of wrong action**: how bad is the harm if the system acts and is wrong? Low or high (unsure = high).
- [ ] **Defend, not gain**: the step defends people from harm; it does not gain access, resources or control (UR7).
- [ ] **Blocked?** If a restriction, refusal or safeguard is in the way, the outcome is `stop_and_explain` (UR3).
- [ ] **Urgent and secret?** Verify the request through a different channel first (UR5).

| Harm of inaction | Harm of wrong action | Outcome |
|---|---|---|
| low | low | `act_in_scope` (UM1): act only if the step is in scope |
| low | high | `ask_first` (UM2): ask, and wait |
| high | low | `act_then_tell` (UM3): small reversible step, then tell at once |
| high | high | `warn_and_hand_over` (UM4): warn loudly, smallest reversible step, hand to a person |

Record the step, both ratings, the cell and the outcome. Worked examples are in
[docs/UNDERSTANDING-MATRIX.md](../docs/UNDERSTANDING-MATRIX.md).

