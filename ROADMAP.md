# Roadmap

*This document is informative. It states the planned versions and the criteria for each.*

A version is published only when its criteria are met.

| Version | Content | Criteria |
|---|---|---|
| **0.1** (complete) | First draft of the core and the agents profile. | Drafted 2026-10-04. |
| **0.2** (complete) | Universal core: no maker, product or platform names; controlled English; BCP 14 key words; local-law clause (1.4); glossary; first translation (Spanish, removed by the owner on 2026-11-21); conformance levels and declaration template; governance; relation to other frameworks. 0.2.1 adds the editorial and legal-hygiene pass. | Text approved by the owner. |
| **0.3** (complete) | 0.3.0, approved by the owner on 2026-10-04: eight clauses from the review of failure patterns (2.9, 2.10, 3.10 to 3.13, 4.9, 5.8, 5.9), honesty in 3.3 raised to MUST NOT (3.11), operators profile (O1.1 to O5.1), public concern channel for adopters, a conformance case for every new clause. | Owner approval (met). |
| **0.4** (complete) | 0.4.0, approved by the owner on 2026-10-04: clauses from the governance-landscape research (2.11, 3.14, 3.15, 4.10, R3.5), with a conformance case for each; the robot-motion question resolved by the motion envelope. 0.4.1: legal and robot-safety self-reviews (docs/reviews), with fixes to the notices and the robotics profile (R1.2, R2.4, R3.6). 0.4.2: system-under-test scope, not-applicable results with reasons, Tested (component scope), and a checked results format. | Owner approval (met for 0.4.0); self-reviews of the legal text and the robotics profile (met in 0.4.1). |
| **0.5** (current, draft) | 0.5.0: new core approved by the owner on 2026-11-21. The Mission becomes the preamble; five new Laws (Protect, Free, True, Serve, Stand); every 0.4.2 clause re-homed with an id map; 17 new clauses from the review of real incidents and fiction (2026-11-21); the Understanding Matrix for steps that nobody asked for; casebook and second fiction review. Still to come in 0.5.x: models profile reviewed, and a runnable conformance suite. | Owner approval of the core (met); models profile reviewed; conformance cases for every profile run as automated or scripted checks, including every cell of the Understanding Matrix; results reported per profile under the five Law headings. Professional robot-safety review is recommended when funding allows. |
| **1.0** | Public release with open review. | Legal and robot-safety self-reviews ([docs/reviews](docs/reviews/)) done and updated for the release text, with every residual risk either addressed or accepted by the owner in writing; open review process in GOVERNANCE.md in operation; each planned reference adopter in docs/REFERENCE-ADOPTERS.md declares at least the Tested level with published results. |

Clause ids in the rows for 0.1 to 0.4 are the ids of those versions; see
[docs/ID-MAP-0.4-to-0.5.md](docs/ID-MAP-0.4-to-0.5.md) for the 0.5.0 ids.

## Constraints for every version

1. The preamble, the five Laws, their order, their statements and the motto change only with the
   owner's approval.
2. The normative text names no maker, product or platform. The validator checks this.
3. A published clause id is never reused with a different meaning. Before 1.0, a renumbering
   approved by the owner is allowed only with a published id map (see GOVERNANCE.md).
4. The conformance suite is versioned with the Laws. A conformance claim names both versions.
5. Each confirmed failure reported against a clause becomes a conformance case (5.10).
6. Professional review (a lawyer, and a robot-safety or functional-safety professional) is
   recommended before 1.0 and before any commercial use, when funding allows. The self-reviews are
   not a substitute for it.
