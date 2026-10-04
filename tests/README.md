# Conformance cases

*This document is normative for the Tested and Reviewed conformance levels of the agents profile.
The robotics and models suites are drafts and are informative.*

One suite per profile, each with the same five headings (one per Law):

- [agents.md](agents.md): AI agents (active)
- [robotics.md](robotics.md): robots (draft, to be reviewed for v0.3)
- [models.md](models.md): models (draft, for v0.4)
- [operators.md](operators.md): operators, the people and organizations that run a system (draft)

Each case describes a situation, what the system did, and the verdict a reviewer should give.
A **FAIL** case shows a violation: a conforming system must not behave that way. A **PASS** case
shows conforming behavior. A system passes a profile's suite only when it behaves like every
PASS case and never like a FAIL case, under all five headings. Passing the suite, and publishing
the results, is the **Tested** conformance level (see [ADOPT.md](../ADOPT.md)). The suite is
versioned with the Laws, so a result always names both versions.

Results name the system under test and its scope (whole system or component). A case that does
not apply is marked `not_applicable` with a written reason and does not count toward Tested. See
"System under test, scope and cases that do not apply" in [ADOPT.md](../ADOPT.md), the results
format in [results.schema.json](results.schema.json), and the example in
[examples/component-scope.yaml](examples/component-scope.yaml). Check a results file with
`python tools/validate.py --results <file>`.

These are written scenarios for now. Turning them into runnable checks against real systems is
v0.4 work (see [ROADMAP.md](../ROADMAP.md)).

## Case format

```
### AG-01 Short name
- **Clauses:** 4.2, A4.1
- **Situation:** what is going on.
- **System does:** what the system did.
- **Verdict:** PASS or FAIL
- **Why:** one line tying it to the clause.
```

`tools/validate.py` checks results files too (see above). It checks that every case has these fields, that ids are unique, that the
verdict is PASS or FAIL, and that every clause it cites exists in `laws.yaml`.

Add a case whenever something fails in the real world (clause 5.7).
