# Roadmap

The pace for Vektra Laws. Each step ships only when its check passes (Law 4: no proof, no done).

| Version | What ships | Done when |
|---|---|---|
| **v0.1** (now) | The core (five Laws, action levels, decision outcomes) and the AI agents profile, with paste-in prompt, checklists, agent conformance cases and the validator. | Pablo has read and sealed the text; the repo is public. |
| **v0.2** | The robotics profile, reviewed. | Someone with hands-on robot safety experience has reviewed it; the open robotics questions are answered; robotics cases cover every clause. |
| **v0.3** | The models profile, plus a conformance test suite. | The models profile is reviewed; the conformance cases for all three profiles can be run as checks, not only read; results are reported per profile under the five headings. |
| **v1.0** | Public release with reference adopters. | Vektra Agent, Phryktor and vektra-reflex each adopt the Laws, pass their profile's suite, and publish the result. |
| **Later** | An open review process, with Vektra as owner. | A written process for proposing, reviewing and accepting changes and new profiles, with Vektra keeping final say. |

## Rules for every version

- The five Laws and their order don't change without Pablo's seal.
- Clause ids, once published, are never reused for a different meaning. A removed clause is marked
  retired, not renumbered.
- The conformance suite is versioned with the Laws. A claim of conformance names both versions.
- Every real-world failure reported against a clause becomes a test case (5.7).
