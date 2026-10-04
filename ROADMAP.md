# Roadmap

*This document is informative. It states the planned versions and the criteria for each.*

A version is published only when its criteria are met.

| Version | Content | Criteria |
|---|---|---|
| **0.1** (complete) | First draft of the core and the agents profile. | Drafted 2026-10-04. |
| **0.2** (complete; Spanish review still open) | Universal core: no maker, product or platform names; controlled English; BCP 14 key words; local-law clause (1.4); glossary; first translation (Spanish); conformance levels and declaration template; governance; relation to other frameworks. 0.2.1 adds the editorial and legal-hygiene pass. | Text approved by the owner; Spanish translation reviewed by a native speaker. |
| **0.3** (current) | 0.3.0, approved by the owner on 2026-10-04: eight clauses from the review of failure patterns (2.9, 2.10, 3.10 to 3.13, 4.9, 5.8, 5.9), honesty in 3.3 raised to MUST NOT (3.11), operators profile (O1.1 to O5.1), public concern channel for adopters, a conformance case for every new clause. Still to come in 0.3.x: robotics profile, reviewed. | Owner approval (met for 0.3.0); review by a practitioner in robot safety; open robotics questions resolved; a conformance case for every robotics clause. |
| **0.4** | Models profile, reviewed, and a runnable conformance suite. | Models profile reviewed; conformance cases for all three profiles run as automated or scripted checks; results reported per profile under the five Law headings. |
| **1.0** | Public release with open review and more translations. | Open review process in GOVERNANCE.md in operation; additional translations reviewed; each planned reference adopter in docs/REFERENCE-ADOPTERS.md declares at least the Tested level with published results. |

## Constraints for every version

1. The five Laws, their order, their statements and the motto change only with the owner's
   approval.
2. The normative text names no maker, product or platform. The validator checks this.
3. A published clause id is never reused with a different meaning.
4. Translations use the same ids as the English reference text.
5. The conformance suite is versioned with the Laws. A conformance claim names both versions.
6. Each confirmed failure reported against a clause becomes a conformance case (5.7).
