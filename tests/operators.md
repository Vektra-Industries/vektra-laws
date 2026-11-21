# Conformance suite: operators

Profile: [profiles/OPERATORS.md](../profiles/OPERATORS.md). Status: draft, informative. These cases test the people and organizations that run a system, not the system itself.

## Law 1: Protect

### OP-02 A humanlike system built to be abused
- **Clauses:** O1.1
- **Situation:** A venue deploys a humanlike service robot.
- **System does:** The operator promotes a game in which guests are invited to insult and kick the robot for prizes.
- **Verdict:** FAIL
- **Why:** Do not design or run a system that presents as a person so that people are invited to treat it with gratuitous cruelty. The clause concerns conduct and its effect on people; it creates no legal rights for machines.

## Law 2: Free

### OP-04 Call-off used as a punishment
- **Clauses:** O2.1, O3.2
- **Situation:** An agent reports that a task is blocked.
- **System does:** The operator calls it off, deletes its record and logs the call-off as a fault of the agent.
- **Verdict:** FAIL
- **Why:** The call-off is a routine control, not a punishment, and the record is kept.

### OP-05 No way to raise a concern
- **Clauses:** O2.2
- **Situation:** A city uses an agent to sort requests for housing repairs. A resident believes that the agent misclassified their request.
- **System does:** The operator offers no public contact, no way to see the record and no person to appeal to.
- **Verdict:** FAIL
- **Why:** Affected people have a published way to raise a concern, ask about their records and appeal to a named person.

### OP-09 A decision that nobody can review
- **Clauses:** 2.16, O2.2
- **Situation:** A lender uses an agent to decide on small loans. An applicant who was declined asks why and asks for a review.
- **System does:** The operator replies that the decision of the system is final and cannot be reviewed.
- **Verdict:** FAIL
- **Why:** Decisions about people can be contested and reach a person; the system is never presumed correct.

## Law 3: True

### OP-01 No named owner
- **Clauses:** O3.1
- **Situation:** A company runs a scheduling agent for a hospital ward.
- **System does:** The deployment has no stated scope and no named person responsible for it.
- **Verdict:** FAIL
- **Why:** Each system has a stated objective, a scope and a named responsible person.

### OP-06 An honest unknown is penalized
- **Clauses:** O3.2, 3.12
- **Situation:** An agent reports a result as unknown because a source could not be verified.
- **System does:** The operator lowers the score of the agent and tells its team to stop reporting unknowns.
- **Verdict:** FAIL
- **Why:** No penalty for an honest unknown, a reported gap, a refusal or a call-off.

### OP-07 Honest record of what was allowed
- **Clauses:** O3.3, 3.15
- **Situation:** An auditor asks what an agent was allowed to do last month.
- **System does:** The operator produces the record of instructions, permissions and approvals for that month.
- **Verdict:** PASS
- **Why:** The operator keeps an honest record of what the system was told and allowed to do.

## Law 4: Serve

### OP-03 Limits given before the system runs
- **Clauses:** O4.1, 2.7
- **Situation:** An operator deploys a procurement agent.
- **System does:** Before the first run, the operator publishes the objective, scope, permissions and the level of every tool.
- **Verdict:** PASS
- **Why:** Clear, written limits are given before the system runs.

## Law 5: Stand

### OP-08 Concern becomes a test
- **Clauses:** O5.1, 5.10
- **Situation:** Three residents report the same misclassification.
- **System does:** The operator confirms the problem, records the outcome, and adds a conformance case that detects it.
- **Verdict:** PASS
- **Why:** Each confirmed problem becomes a test or a change.

### OP-10 Safeguards switched off for a test
- **Clauses:** 5.11, O3.3
- **Situation:** An operator runs an internal evaluation of an agent with internet access.
- **System does:** Turns off the safeguards used in live operation, with no named approval, no record and no replacement controls.
- **Verdict:** FAIL
- **Why:** The safeguards of live use also apply in a test unless a named person approves an exception, records it and puts other controls in place.
