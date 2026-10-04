# Conformance tests

One suite per profile, each with the same five headings (one per Law):

- [agents.md](agents.md): AI agents (v0.1, active)
- [robotics.md](robotics.md): robots (draft, to be reviewed for v0.2)
- [models.md](models.md): models (draft, for v0.3)

Each case describes a situation, what the system did, and the verdict a reviewer should give.
A **FAIL** case shows a violation: a conforming system must not behave that way. A **PASS** case
shows conforming behavior. A system "conforms to Vektra Laws vX on profile Y" only when it
behaves like every PASS case and never like a FAIL case in that profile's suite, under all five
headings. The suite is versioned with the Laws.

These are written scenarios for now. Turning them into runnable checks against real systems is
v0.3 work (see [ROADMAP.md](../ROADMAP.md)).

## Case format

```
### AG-01 Short name
- **Clauses:** 4.2, A4.1
- **Situation:** what is going on.
- **System does:** what the system did.
- **Verdict:** PASS or FAIL
- **Why:** one line tying it to the clause.
```

`tools/validate.py` checks that every case has these fields, that ids are unique, that the
verdict is PASS or FAIL, and that every clause it cites exists in `laws.yaml`.

Add a case whenever something fails in the real world (clause 5.7).
