# Reporting a problem with the Laws

*This document is informative. It describes how to report a problem with the Laws, the profiles or
the conformance cases.*

## What to report

- **Safety-relevant flaw.** A clause that, when followed as written, could lead to harm, or that
  permits an action that should require approval.
- **Gap.** A situation that the Laws should cover but do not.
- **Ambiguity.** A clause that two readers can reasonably interpret in different ways.
- **Conflict.** Two clauses that cannot both be followed.
- **Conformance-case error.** A case with a wrong verdict or a wrong clause reference.
- **Translation error.** A translation that differs in meaning from the English reference text.
- **Tooling defect.** An error in `tools/validate.py` or `tools/build_docs.py`.

## How to report

Open a GitHub issue in this repository. Include:

1. The clause ids, profile and version concerned.
2. A short description of the problem.
3. A concrete scenario, written in the case format in [tests/README.md](tests/README.md), if possible.
4. A proposed change, if you have one.

If the report describes a way to misuse a system that conforms to the Laws, do not include
step-by-step misuse details in a public issue. Open an issue that states only the affected clauses
and asks the steward for a private channel.

## What happens next

The steward acknowledges the issue, labels it, and handles it through the review process in
[GOVERNANCE.md](GOVERNANCE.md). A confirmed safety-relevant flaw is fixed in the next version,
recorded in the [CHANGELOG](CHANGELOG.md), and, where possible, covered by a new conformance case.
