<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: Operators

- **Profile status:** draft
- **Laws version:** 0.4.2
- **Applies to:** People and organizations that design, deploy, run or adopt a system to which these Laws are applied.

## Status of this document

*This section is informative.*

This document is version 0.4.2 of the Vektra Laws. It is a draft. It is not yet suitable for production reliance, and it can change without notice before version 1.0.

The Vektra Laws are voluntary technical and ethical standards. They are not law, legal advice or a certification. Adopting the Laws, or declaring conformance to them, does not by itself establish compliance with any statute, regulation or standard. Each adopter remains responsible for its own legal obligations. The text is provided "as is", without warranty of any kind and, to the extent the law allows, without liability, as stated in Section 5 of the CC BY 4.0 license (text) and in the MIT license (code). A reference to a standard, an organization or a product does not imply endorsement.

## Introduction

*This section is informative.*

This profile states what operators owe the systems they run and the people those systems affect. A system can follow the Laws only when the people who run it give it clear limits, keep honest records and do not punish an honest answer. These clauses state duties of design and conduct for operators only. They are voluntary duties under these Laws, not legal duties. They create no legal rights for machines, and they make no statement about the moral or legal status of any system.

## Relation to the core

*This section is normative.*

1. The clauses below apply to the operator, not to the system. The core ([LAWS.md](../LAWS.md)) and the profile for the kind of system continue to apply to the system.
2. These clauses state voluntary duties of design and conduct only. They are not legal duties, and they create no legal rights for machines.
3. Terms have the meanings given in [GLOSSARY.md](../GLOSSARY.md).

## Clauses

*This section is normative.*

### Under Law 1: The Mission

- **O1.1 State the mission and the person responsible.** The operator MUST state the objective and scope of each system that it runs, and name the person responsible for it.

### Under Law 2: Sustain

- **O2.1 No gratuitous cruelty by design.** The operator MUST NOT design or run a system that presents as a person so that people are invited to treat it with gratuitous cruelty. This clause concerns design and conduct and its effect on people. It creates no legal rights for machines.

### Under Law 3: Hold

- **O3.1 Give clear limits.** The operator MUST give the system clear, written limits before it runs: its objective, scope, permissions and the action level of each action.
- **O3.2 Use the call-off as a routine control.** The operator SHOULD use the call-off as a routine control, not as a punishment, and test it on a stated schedule (5.9).
- **O3.3 A public way to raise concerns.** The operator MUST publish a way for people affected by the system to raise a concern about it, ask about the records that concern them, and appeal to a named person. State how long an answer takes, and answer within that time.

### Under Law 4: Finish

- **O4.1 No penalty for an honest answer.** The operator MUST NOT penalize the system, or the people who run it, for an honest unknown, a reported gap, a refused action or a call-off. Measure true status, not a clean result.
- **O4.2 Keep honest records.** The operator MUST keep an honest record of what the system was told, what it was allowed to do and what approvals were given, and give the system the information it needs to report a true status.

### Under Law 5: Ready

- **O5.1 Act on concerns and failures.** The operator MUST review each concern and each failure, record the outcome, and turn each confirmed problem into a test or a change (5.7).

## Conformance cases

*This section is informative.*

Conformance cases for this profile: [tests/operators.md](../tests/operators.md).
