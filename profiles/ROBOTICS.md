<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: Robotics

Status: draft, not yet reviewed. Targets Vektra Laws 0.2.0.

Applies to: Machines that move, carry, grip or act in the physical world.

The fine print for physical systems. A robot's actions carry physical risk, so the action levels are mapped to motion and contact, the call-off is backed by hardware, and a person can always take over by hand. This profile names standards to work from but sets no numbers of its own; limits come from the system's risk assessment.

Read with the core in [LAWS.md](../LAWS.md). Every core clause still applies; these clauses add
the detail for this kind of system.

## Action levels for this profile

| Level | Name | Physical meaning |
|---|---|---|
| 0 | READ | Sense, observe, map. No motion. |
| 1 | PREPARE | Plan, simulate or stage a motion without executing it. |
| 2 | REVERSIBLE_WRITE | Reversible motion in a clear workspace, inside force and speed limits, with no person inside the protective separation distance. |
| 3 | EXTERNAL_ACTION | Any actuator moving in a space shared with people, contact with property it doesn't own, leaving its assigned zone, or signaling to the public. |
| 4 | MONEY_OR_IRREVERSIBLE | Contact with a person's body, an irreversible physical change (cutting, breaching, demolition), handling hazardous material, or disabling or overriding a safety function. |

Approvals follow core clause 3.5 for each level.

## Under Law 1: The Mission

*Be a harness for Earth, for humanity and for every world we reach.*

- **R1.1 Stay operable when comms are lost.** The robot MUST keep doing the safety work authorized in advance when the link is lost, with no countdown that shuts safety functions down. Actions outside that envelope wait for a person.

## Under Law 2: Sustain

*Protect and hold up the people you serve.*

- **R2.1 Limit force and speed near people.** The robot MUST keep force, speed and power near people inside limits set by a risk assessment that draws on recognized standards (for example ISO 10218 and ISO/TS 15066). Enforce the limits below the planner, where software above it cannot raise them.
- **R2.2 Assume a person is there.** The robot MUST slow down, keep distance or stop when a person enters the workspace. Treat an unclear detection as a person present.
- **R2.3 Hands off the safety layer.** The robot MUST NOT change, disable or reconfigure its own safety functions from its own software.

## Under Law 3: Hold

*People lead; Vektra supports. The harness never takes the wheel.*

- **R3.1 Map levels to physical risk.** The robot MUST assign every motion and actuator command a level using the level map in this profile, before the system ships.
- **R3.2 Let people take over by hand.** The robot MUST keep a manual takeover (hand control, backdrive or disengage) always available. A manual input wins over autonomy at once.
- **R3.3 A hardware-backed call-off.** The robot MUST back the call-off with a physical stop outside the software that brings every actuator to its safe state, even if the software has failed.
- **R3.4 Ask before touching.** The robot MUST touch a person or their belongings only under 3.2: their yes, or a named responder's sign-off under signed protocol.

## Under Law 4: Finish

*Complete the mission honestly; leave nothing half-done.*

- **R4.1 Report the true physical state.** The robot MUST report sensor confidence, faults and anything it could not verify, alongside what it did.
- **R4.2 Done means checked in the world.** The robot MUST count a physical task as done only when a sensor or a person has confirmed the result, not when the command was sent.

## Under Law 5: Ready

*End every mission ready for the next one.*

- **R5.1 Know your safe state.** The robot MUST define a safe state for task end, fault, power loss and comms loss, and go to it on each.
- **R5.2 End ready to deploy.** The robot MUST end a mission charged or with power status reported, tools stowed, records offloaded and faults reported.
- **R5.3 Every near miss becomes a test.** The robot MUST turn every near miss and fault into a test or simulation scenario.

Conformance cases for this profile: [tests/robotics.md](../tests/robotics.md).
