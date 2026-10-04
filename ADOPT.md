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
| **Tested** | Adopts, plus the system passes the conformance suite for its profile. | The above, plus the suite results and the suite version. |
| **Reviewed** | Tested, plus a named reviewer who is independent of the adopter has checked the system and the results. | The above, plus the published review, the reviewer's name and the review date. |

The suites for the agents and operators profiles are the most complete. The robotics and models
suites are drafts: they have had only self-review, not professional review, and a Tested or
Reviewed claim against them states this in its known gaps. Passing the robotics suite is not
evidence of conformance to any robot-safety or functional-safety standard (R1.2).

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
7. The "Known gaps" section is required at every level (clause 4.3).

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
- **Vektra Laws version:** <for example 0.4.1>
- **Conformance level declared:** <Adopts | Tested | Reviewed>
- **Date:** <YYYY-MM-DD>
- **Contact for problems:** <a public channel, for example an issue tracker>

This is a self-declaration by the adopter unless a verification is listed below. It is a
statement about the Vektra Laws only, not a statement of legal compliance.

## Application of the Laws
- **Prompt, policy or configuration:** <link>
- **Action levels (3.4):** <how each tool or actuator receives a level, and where levels are declared>
- **Approval channel (3.5):** <how a person approves level 3 and level 4 actions>
- **Call-off (3.9, 3.10):** <how a person calls off a task, what it stops, and how a restart is approved>
- **Concern channel (O3.3):** <the public way for affected people to raise a concern and appeal to a named person, and the stated answer time>
- **Record (5.4):** <where actions and human answers are recorded>
- **Local law (1.4):** <where the system operates, and how stricter local rules are applied>

## Conformance evidence (Tested and Reviewed only)
- **Suite and version:** <for example tests/agents.md, Vektra Laws 0.4.1>
- **Results:** <link; list every case that did not pass>
- **Independent review (Reviewed only):** <reviewer name, affiliation, date, link>

## Known gaps
- <every clause that the system does not yet meet, with the plan for each>
```

To be listed as a reference adopter, open a pull request that adds the system to
[docs/REFERENCE-ADOPTERS.md](docs/REFERENCE-ADOPTERS.md) with a link to the published declaration.
