# Adopt the Vektra Laws

Any agent, robot or model, from any maker, in any country, can adopt the Vektra Laws, free of
charge and without permission. To declare adoption, copy the template below into your own
repository or website, fill it in, and publish it.

## Conformance levels

| Level | Requires | Evidence to publish |
|---|---|---|
| **Adopts** | You apply the Laws to your system and publish how. | This declaration, and the prompt or policy that applies the Laws. |
| **Tested** | Adopts, plus your system passes the conformance suite for its profile. | The above, plus the suite results, with the suite version. |
| **Verified** | Tested, plus a reviewer who is independent of you checked the system and the results. | The above, plus the published review and the reviewer's name. |

Rules:

- Declare only the level that your published evidence supports.
- Name the version of the Laws and of the conformance suite.
- Update or withdraw the declaration when your system changes.
- A conformance level is a statement about these Laws only. It is not a certification of
  compliance with any law or standard.

## Self-declaration template

```markdown
# Vektra Laws declaration

- **System:** <name and version>
- **Maker:** <organization or person>
- **Kind of system:** <AI agent | robot | AI model | other>
- **Profile:** <agents | robotics | models>
- **Vektra Laws version:** <for example 0.2.0>
- **Conformance level:** <Adopts | Tested | Verified>
- **Date:** <YYYY-MM-DD>
- **Contact:** <how to report a problem>

## How the Laws are applied
- **Prompt or policy:** <link to the published prompt, policy or configuration>
- **Action levels:** <how each tool or actuator gets a level (3.4); where the levels are declared>
- **Approval channel:** <how a person approves level 3 and level 4 actions (3.5)>
- **Call-off:** <how a person calls off a task, and what it stops (3.9)>
- **Record:** <where actions and human answers are recorded (5.4)>
- **Local law:** <the places where the system operates, and how stricter local rules are applied (1.4)>

## Conformance evidence (Tested and Verified only)
- **Suite and version:** <for example tests/agents.md at 0.2.0>
- **Results:** <link; list every case that did not pass>
- **Independent review (Verified only):** <reviewer, date, link>

## Known gaps
- <every clause the system does not yet meet, and the plan for it>
```

The "Known gaps" section is required at every level (clause 4.3). A declaration with honest gaps
is better than a declaration with none.

To be listed as a reference adopter, open a pull request that adds your system to
[docs/REFERENCE-ADOPTERS.md](docs/REFERENCE-ADOPTERS.md) with a link to your declaration.
