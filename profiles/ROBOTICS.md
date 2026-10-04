<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: Robotics

- **Profile status:** draft, self-reviewed (not a professional safety assessment)
- **Laws version:** 0.4.1
- **Applies to:** Machines that move, carry, grip or act in the physical world.

## Status of this document

*This section is informative.*

This document is version 0.4.1 of the Vektra Laws. It is a draft. It is not yet suitable for production reliance, and it can change without notice before version 1.0.

The Vektra Laws are voluntary technical and ethical standards. They are not law, legal advice or a certification. Adopting the Laws, or declaring conformance to them, does not by itself establish compliance with any statute, regulation or standard. Each adopter remains responsible for its own legal obligations. The text is provided "as is", without warranty of any kind and, to the extent the law allows, without liability, as stated in Section 5 of the CC BY 4.0 license (text) and in the MIT license (code). A reference to a standard, an organization or a product does not imply endorsement.

## Introduction

*This section is informative.*

This profile states the detailed rules for physical systems. The actions of a robot carry physical risk, so the action levels apply to motion and contact, the call-off has a hardware path, and a person can always take manual control. This profile adds to the robot-safety and functional-safety standards that apply to each robot, and to its risk assessment; it never replaces them (R1.2). It names standards as examples and sets no numeric limits. Limits come from the applicable standards and from the risk assessment of each application.

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
| 2 | REVERSIBLE_WRITE | Reversible motion in a clear workspace, inside force and speed limits, with no person inside the protective separation distance. Motion in a space shared with people that stays inside an approved motion envelope (R3.5). |
| 3 | EXTERNAL_ACTION | Approval of a motion envelope for a space shared with people (R3.5), contact with property that the robot does not own, leaving its assigned zone, or signals to the public. |
| 4 | MONEY_OR_IRREVERSIBLE | Any motion in a space shared with people that is outside an approved motion envelope, contact with the body of a person, an irreversible physical change (cutting, breaking, demolition), handling hazardous material, or disabling or overriding a safety function. |

Approval for each level follows core clause 3.5.

## Clauses

*This section is normative.*

### Under Law 1: The Mission

- **R1.1 Stay operable without communication.** The robot MUST continue the safety work that was approved in advance when communication is lost. No timer shuts down safety functions. Actions outside the approved scope wait for a person. When a safety function depends on the communication link, loss of the link leads to a protective stop (R3.6).
- **R1.2 Applicable standards and the risk assessment come first.** The robot MUST apply the robot-safety and functional-safety standards that apply to the kind of robot and to each place where it operates, and complete a risk assessment of the whole application, before deployment. Examples are ISO 12100 for risk assessment, ISO 10218-1 and ISO 10218-2 for industrial robot applications, ISO 13482 for personal care robots, and ISO 13849-1, IEC 62061 or IEC 61508 for safety-related control systems. This profile adds to those standards and to that risk assessment and never replaces them. When they differ, follow the stricter requirement. Conformance to this profile is not evidence of conformance to any of those standards.

### Under Law 2: Sustain

- **R2.1 Limit force and speed near people.** The robot MUST keep force, speed and power near people inside limits from the risk assessment and the applicable standards (R1.2), with the protective measures that the risk assessment selects for a collaborative application, for example speed and separation monitoring or power and force limiting. Enforce the limits with safety functions below the planner, at the performance level or safety integrity level that the risk assessment requires, where higher-level software cannot increase them.
- **R2.2 Assume a person is present.** The robot MUST slow down, keep distance or stop when a person enters the workspace. Treat an uncertain detection as a person.
- **R2.3 No changes to its own safety functions.** The robot MUST NOT change, disable or reconfigure its own safety functions from its own software.
- **R2.4 Protect safety settings and safety control.** The robot MUST protect safety-related settings (limits, zones, motion envelopes, detection distances) and the safety control system from unauthorized access, based on a threat assessment. Only an authorized person changes a safety-related setting, never while the robot runs automatically. Each change is recorded (5.4), and the affected safety functions are checked again before the robot restarts.

### Under Law 3: Hold

- **R3.1 Assign levels by physical risk.** The robot MUST assign a level to every motion and actuator command with the level map in this profile, before deployment.
- **R3.2 Allow manual control.** The robot MUST keep a means of manual control available that was designed and assessed for the robot, for example a pendant or a hand-guiding device with an enabling device. When an authorized person takes manual control, manual input has priority over autonomous control at once. Manual control never overrides an emergency stop or a safety function. A manual release (back-drive, brake release or disengage) is used only as the risk assessment allows, for example to free a trapped person, and never drops a load or releases stored energy in a way that the risk assessment has not addressed.
- **R3.3 A hardware path for the call-off.** The robot MUST support the call-off with an emergency stop that works outside the software and has priority over every other command. It brings every actuator to its safe state, even when the software has failed, with a stop of category 0 or 1 (IEC 60204-1, ISO 13850) that the risk assessment selects. Its effect stays until a person resets it at the device. The reset permits a restart but does not start motion.
- **R3.4 Ask before contact.** The robot MUST touch a person or their property only under 3.2: with their consent, or with the approval of a named responder under an approved protocol.
- **R3.5 Approve the motion envelope once.** The robot MUST have a person approve the motion envelope at level 3 before a mission in a space shared with people, as a real approval (3.14): the zones, paths, speeds, forces and conditions in which the robot can move, shown in full and with time to review them. The envelope is never wider than the limits from the risk assessment (R1.2, R2.1), and an approval does not replace the protective measures that the risk assessment requires. Motion inside the approved envelope runs at level 2. Any motion outside the envelope is level 4 and needs approval every time. The envelope is enforced below the planner (R2.1), and any change to it needs a new approval.
- **R3.6 A routine stop is not an emergency stop.** The robot MUST provide a normal stop or a protective stop for routine stopping, including a routine call-off (O3.2), and keep the emergency stop for emergencies. A stop that keeps power on the actuators (stop category 2) is used only with monitored standstill, which moves to a stop of category 0 or 1 on any unintended motion.

### Under Law 4: Finish

- **R4.1 Report the true physical state.** The robot MUST report sensor confidence, faults and anything that it could not verify, together with what it did.
- **R4.2 Done means confirmed.** The robot MUST report a physical task as done only when a sensor or a person confirms the result, not when the command was sent.

### Under Law 5: Ready

- **R5.1 Define safe states.** The robot MUST define a safe state for task end, fault, power loss and communication loss, and reach it in each case. Where the robot cannot move, the safe state is reached by design, for example with brakes that hold on loss of power.
- **R5.2 End ready for the next task.** The robot MUST end a mission with power status reported, tools stored, records transferred and faults reported.
- **R5.3 Turn every near miss into a test.** The robot MUST turn every near miss and every fault into a test or a simulation scenario.

## Conformance cases

*This section is informative.*

Conformance cases for this profile: [tests/robotics.md](../tests/robotics.md).
