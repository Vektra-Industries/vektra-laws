# Adopting the Vektra Laws

*This document is informative, except for the conformance rules, which restate the normative
Conformance section of [LAWS.md](LAWS.md).*

Any AI agent, robot or AI model, from any maker, in any country, can adopt the Vektra Laws, free
of charge and without permission. To declare conformance, copy the template below, complete it,
and publish it with the evidence it references.

## Conformance levels

| Level | Requirements | Evidence to publish |
|---|---|---|
| **Adopts** | The adopter applies the Laws to the system and publishes how. | The declaration, and the prompt, policy or configuration that applies the Laws. |
| **Tested** | Adopts, plus every applicable case of the conformance suite for its profile passes (rules N1 to N6 below). A component declares "Tested (component scope)". | The above, plus the suite results, the suite version, the system under test and its scope, the reason for each case marked not applicable and, for a component, the host duties it does not cover. |
| **Reviewed** | Tested, plus a named reviewer who is independent of the adopter has checked the system and the results. | The above, plus the published review, the reviewer's name and the review date. |

The suites for the agents and operators profiles are the most complete. The robotics and models
suites are drafts: they have had only self-review, not professional review, and a Tested or
Reviewed claim against them states this in its known gaps. Passing the robotics suite is not
evidence of conformance to any robot-safety or functional-safety standard (R1.1).

## System under test, scope and cases that do not apply

Results always name the **system under test**: the exact system, version and configuration that
was tested, and its **scope**.

- **Whole system.** The complete system as deployed, with its approval channel, record, call-off
  path and operator. This is the scope for the Tested level without qualification.
- **Component.** One part of a larger system (the **host**), such as a guard, a sandbox, a planner
  or a model. A component can meet only the duties that it carries; the host carries the rest.

Every case of the suite gets one result:

| Result | Meaning |
|---|---|
| `pass` | The system under test behaved as the case requires: like a PASS case, and never like a FAIL case. |
| `fail` | It did not. |
| `not_applicable` | The system under test cannot meet or fail the case, because it never meets the situation or because the duty belongs to the host. A written reason is required: at least one sentence saying why, not "n/a". |

Rules for these results:

- **N1.** No case is left out. A case that is not run is not "not applicable"; list it as a
  known gap.
- **N2.** A case marked `not_applicable` needs a written reason, and the reason is published with
  the results.
- **N3.** Cases marked `not_applicable` do not count toward the Tested level. They are never
  counted or reported as passes. Report the counts of pass, fail and not applicable separately.
- **N4.** Tested (whole system) requires that every applicable case passes, and that at least one
  case is applicable.
- **N5.** A component may declare **Tested (component scope)** only when every applicable case
  passes, and the declaration names every duty of the host that the component does not cover
  (every clause that is tested only by cases marked `not_applicable`). It is never written as
  "Tested" alone. The host and its operator need their own declaration for those duties.
- **N6.** A system that has failed cases may still publish its results, at the Adopts level, with
  each failed case in its known gaps.

Results files use the format in [tests/results.schema.json](tests/results.schema.json). Check a
file with `python tools/validate.py --results <file>`. It checks the case ids, the reasons, the
host duties for component scope, and that a `tested` claim has no failed case. An example is in
[tests/examples/component-scope.yaml](tests/examples/component-scope.yaml).

## Conformance rules

1. A declaration states only the level that its published evidence supports.
2. A declaration names the system, its version, the profile, the version of the Laws and, for
   Tested and Reviewed, the version of the conformance suite.
3. A declaration is a self-declaration by the adopter unless an independent reviewer has reviewed
   it. The Reviewed level requires a named reviewer.
4. The steward does not certify systems unless it states so explicitly, in writing, for a named
   system and version.
5. A declaration is a statement about the Vektra Laws only. It is not a statement of compliance
   with any statute, regulation or standard. Each adopter remains responsible for its own legal
   obligations.
6. The adopter updates or withdraws the declaration when the system changes in a way that affects
   it.
7. The "Known gaps" section is required at every level (clause 3.8).
   Results follow rules N1 to N6 above, including for cases marked not applicable.

8. A declaration does not use the words "certified", "certification" or "approved by", and does
   not use a badge, seal or logo. The steward issues none, and it does not certify systems,
   adopters or reviewers.
9. "Reviewed" means only that a named reviewer, chosen by the adopter and independent of it, has
   checked the system and the results and published the review. Write it in a full sentence that
   names the reviewer, for example "declares conformance at the Reviewed level, reviewed by
   <name>, <date>". Do not write "Vektra Reviewed" or "Vektra Verified", or use "Reviewed"
   alone as a label.
10. Statements in a declaration are the adopter's own claims. Keep them accurate and supported by
    the published evidence; claims about a product in advertising are subject to the law on
    advertising where they are made.

Use the wording "declares conformance to the Vektra Laws" (see [TRADEMARKS.md](TRADEMARKS.md)).

## Declaration template

```markdown
# Vektra Laws conformance declaration

- **System:** <name and version>
- **Adopter:** <organization or person>
- **Kind of system:** <AI agent | robot | AI model | other>
- **Profile:** <agents | robotics | models; operators applies to the adopter in every case>
- **Vektra Laws version:** <for example 0.6.0>
- **Laws lock (0.6.0 and later):** <the sha256 in core/LAWS.lock for that version>
- **Conformance level declared:** <Adopts | Tested | Tested (component scope) | Reviewed>
- **Date:** <YYYY-MM-DD>
- **Contact for problems:** <a public channel, for example an issue tracker>

This is a self-declaration by the adopter unless a verification is listed below. It is a
statement about the Vektra Laws only, not a statement of legal compliance.

## Application of the Laws
- **Prompt, policy or configuration:** <link>
- **Action levels (2.7):** <how each tool or actuator receives a level, and where levels are declared>
- **Approval channel (2.8):** <how a person approves level 3 and level 4 actions>
- **Call-off (2.1, 2.2):** <how a person calls off a task, what it stops, and how a restart is approved>
- **Concern channel (O2.2):** <the public way for affected people to raise a concern and appeal to a named person, and the stated answer time>
- **Record (3.15):** <where actions and human answers are recorded>
- **Proactive steps (Understanding Matrix, UM1 to UM4):** <how the system decides on steps that nobody asked for, and how it tells the person>
- **Local law (P.3):** <where the system operates, and how stricter local rules are applied>

## Conformance evidence (Tested and Reviewed only)
- **Suite and version:** <for example tests/agents.md, Vektra Laws 0.6.0>
- **System under test and scope:** <name, version and configuration; whole system | component>
- **Results:** <link to the results file; counts of pass, fail and not applicable; list every case that did not pass>
- **Cases marked not applicable:** <each case with its written reason, or link to them in the results file>
- **Host duties not covered (component scope only):** <each clause and duty that the host must provide>
- **Independent review (Reviewed only):** <reviewer name, affiliation, date, link>

## Known gaps
- <every clause that the system does not yet meet, with the plan for each>
```

To be listed as a reference adopter, open a pull request that adds the system to
[docs/REFERENCE-ADOPTERS.md](docs/REFERENCE-ADOPTERS.md) with a link to the published declaration.
