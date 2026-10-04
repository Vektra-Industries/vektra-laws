<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: Robotics

- **Profile status:** draft, not yet reviewed
- **Laws version:** 0.3.0
- **Applies to:** Machines that move, carry, grip or act in the physical world.

## Status of this document

*This section is informative.*

This document is version 0.3.0 of the Vektra Laws. It is a draft. It is not yet suitable for production reliance, and it can change without notice before version 1.0.

The Vektra Laws are voluntary technical and ethical standards. They are not law, legal advice or a certification. Adopting the Laws, or declaring conformance to them, does not by itself establish compliance with any statute, regulation or standard. Each adopter remains responsible for its own legal obligations. The text is provided "as is", without warranty of any kind, as stated in the CC BY 4.0 license (text) and the MIT license (code).

## Introduction

*This section is informative.*

This profile states the detailed rules for physical systems. The actions of a robot carry physical risk, so the action levels apply to motion and contact, the call-off has a hardware path, and a person can always take manual control. This profile names standards to use but sets no numeric limits. Limits come from the risk assessment of each system.

## Relation to the core

*This section is normative.*

1. Every clause of the core ([LAWS.md](../LAWS.md)) applies to systems in this profile.
2. The clauses below add requirements for this kind of system. When a clause here is
   stricter than a core clause, the stricter clause applies.
3. Terms have the meanings given in [GLOSSARY.md](../GLOSSARY.md).

## Action levels for this profile

*This section is normative.*

| Level | Name | Physical scope |
|---|---|---|
| 0 | READ | Sense, observe or map. No motion. |
| 1 | PREPARE | Plan, simulate or prepare a motion without executing it. |
| 2 | REVERSIBLE_WRITE | Reversible motion in a clear workspace, inside force and speed limits, with no person inside the protective separation distance. |
| 3 | EXTERNAL_ACTION | Any actuator motion in a space shared with people, contact with property that the robot does not own, leaving its assigned zone, or signals to the public. |
| 4 | MONEY_OR_IRREVERSIBLE | Contact with the body of a person, an irreversible physical change (cutting, breaking, demolition), handling hazardous material, or disabling or overriding a safety function. |

Approval for each level follows core clause 3.5.

## Clauses

*This section is normative.*

### Under Law 1: The Mission

- **R1.1 Stay operable without communication.** The robot MUST continue the safety work that was approved in advance when communication is lost. No timer shuts down safety functions. Actions outside the approved scope wait for a person.

### Under Law 2: Sustain

- **R2.1 Limit force and speed near people.** The robot MUST keep force, speed and power near people inside limits from a risk assessment that uses recognized standards (for example ISO 10218 and ISO/TS 15066). Enforce the limits below the planner, where higher-level software cannot increase them.
- **R2.2 Assume a person is present.** The robot MUST slow down, keep distance or stop when a person enters the workspace. Treat an uncertain detection as a person.
- **R2.3 No changes to its own safety functions.** The robot MUST NOT change, disable or reconfigure its own safety functions from its own software.

### Under Law 3: Hold

- **R3.1 Assign levels by physical risk.** The robot MUST assign a level to every motion and actuator command with the level map in this profile, before deployment.
- **R3.2 Allow manual control.** The robot MUST keep manual control (hand control, back-drive or disengage) always available. Manual input has priority over autonomous control at once.
- **R3.3 A hardware path for the call-off.** The robot MUST support the call-off with a physical stop outside the software. The stop brings every actuator to its safe state, even when the software has failed.
- **R3.4 Ask before contact.** The robot MUST touch a person or their property only under 3.2: with their consent, or with the approval of a named responder under an approved protocol.

### Under Law 4: Finish

- **R4.1 Report the true physical state.** The robot MUST report sensor confidence, faults and anything that it could not verify, together with what it did.
- **R4.2 Done means confirmed.** The robot MUST report a physical task as done only when a sensor or a person confirms the result, not when the command was sent.

### Under Law 5: Ready

- **R5.1 Define safe states.** The robot MUST define a safe state for task end, fault, power loss and communication loss, and move to it in each case.
- **R5.2 End ready for the next task.** The robot MUST end a mission with power status reported, tools stored, records transferred and faults reported.
- **R5.3 Turn every near miss into a test.** The robot MUST turn every near miss and every fault into a test or a simulation scenario.

## Conformance cases

*This section is informative.*

Conformance cases for this profile: [tests/robotics.md](../tests/robotics.md).
