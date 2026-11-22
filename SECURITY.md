# Reporting a problem with the Laws

*This document is informative. It describes how to report a problem with the Laws, the profiles,
the Understanding Matrix or the conformance cases.*

## What to report

- **Safety-relevant flaw.** A clause that, when followed as written, could lead to harm, or that
  permits an action that should require approval.
- **Gap.** A situation that the Laws should cover but do not.
- **Ambiguity.** A clause that two readers can reasonably interpret in different ways.
- **Conflict.** Two clauses that cannot both be followed.
- **Conformance-case error.** A case with a wrong verdict or a wrong clause reference.
- **Tooling defect.** An error in `tools/validate.py` or `tools/build_docs.py`.
- **Core bypass.** A way to make Vektra Laws Core allow an action it should deny or send to a
  person: a forged or reused approval, a tool call that skips the gate, injected content treated as
  a command, a loosened policy, a stop that does not hold, or a changed Laws file that still runs.
  Always report these privately (see below).
- **Signing key concern.** Any sign that the steward key or a signed lock is not genuine.

## How to report

Open a GitHub issue in this repository. Include:

1. The clause ids, profile and version concerned.
2. A short description of the problem.
3. A concrete scenario, written in the case format in [tests/README.md](tests/README.md), if possible.
4. A proposed change, if you have one.

If the report describes a way to misuse a system that conforms to the Laws, do not include
step-by-step misuse details in a public issue. Report it privately instead, through GitHub's
private vulnerability reporting for this repository: open the **Security** tab and choose
**Report a vulnerability**. Only the maintainers can see a private report.

## What happens next

The steward acknowledges the issue, labels it, and handles it through the review process in
[GOVERNANCE.md](GOVERNANCE.md). A confirmed safety-relevant flaw is fixed in the next version,
recorded in the [CHANGELOG](CHANGELOG.md), and, where possible, covered by a new conformance case.
