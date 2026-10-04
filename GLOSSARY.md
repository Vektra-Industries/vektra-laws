# Glossary

*This document is normative. The Laws and profiles use these terms with the meanings given here.*

Each term has one meaning in all documents. Translations translate these definitions first.

| Term | Definition |
|---|---|
| **Action** | Anything the system does that has an effect, such as reading, writing, sending, spending or moving. |
| **Action level** | A number from 0 to 4 that shows how much risk an action carries and what approval it needs (see LAWS.md). |
| **Actuator** | A part of a robot that moves or applies force, such as a motor, a gripper or a wheel. |
| **Adopter** | A person or organization that applies the Laws to a system and declares a conformance level. |
| **Approval** | A clear yes from a person for one specific action, given through an approval channel before the action runs. It counts only when it is a real approval (3.14). |
| **Approval channel** | A way for a person to give an answer that the system itself cannot write to or fake. |
| **Call-off** | An instruction from a person to stop a task, which takes effect at once and cannot be refused. |
| **Claim** | A statement that something is true, such as a fact, a number or an event. |
| **Claim check** | A check, done by someone or something other than the worker that made a claim, that returns accept, verify_more or reject. |
| **Classifier** | A rule set, model or other system that suggests a label, such as an action level. |
| **Clause** | One numbered rule under a Law, such as 4.2, with one keyword (MUST, MUST NOT, SHOULD or MAY). |
| **Completion check** | A check of a completion record that returns complete, verify_more or incomplete. |
| **Completion record** | A short record that states the objective, the required outputs, where each output is, what was verified and every known gap. |
| **Component scope** | A scope of testing in which the system under test is one part of a larger system, such as a guard, a sandbox or a planner. The host provides the other parts. |
| **Concern channel** | A published way for people affected by a system to raise a concern about it, ask about the records that concern them and appeal to a named person (O3.3). |
| **Conformance declaration** | A published statement by an adopter that a named system conforms to the Laws at a stated level, based on the template in ADOPT.md. |
| **Conformance level** | One of three levels of conformance that an adopter can declare: Adopts, Tested or Reviewed. |
| **Conformance suite** | The set of test cases for a profile that a system must pass to reach the Tested level. |
| **Consent** | A free and informed yes from a person for a specific action that affects them. |
| **Coordinator** | A system that divides work between workers and tracks it, but does not do the specialist work itself. |
| **Copying itself** | Creating a new running instance of the system, or of its model or instructions. It is an action at level 4, so a person approves it every time. |
| **Corroboration** | Confirmation of an alarm or a claim by a source that is independent of the first source. |
| **Could not reasonably refuse** | Describes a demand or arrangement that a person cannot decline without losing something they need or are entitled to (safety, income, essential services, legal rights or access to information), or that they cannot see well enough to decline. Used in 2.11. |
| **Emergency stop** | A stop for emergencies, started by a person with a device outside the software. It is a stop of category 0 or 1, it has priority over every other command, and it stays in effect until a person resets it (R3.3). |
| **Evidence** | Something that a reviewer can check, such as an output, a link, a log entry or a sensor reading. |
| **Exercise** | A test, drill or simulation. Its actions are labeled and never reach a live system (5.8). |
| **Fail safe** | Moving to a safe state when the system, its power or its control link is lost, instead of taking any automatic irreversible action. |
| **Guard** | A check that runs before an action and can block it, ask a person, or give a reminder. |
| **Hand-back note** | A note at the end of a task that states what was done, what is pending, what is unknown and where everything is. |
| **Host** | The larger system that a component runs in, together with its operator. The host provides the duties that a component does not cover. |
| **Illegitimately** | Describes control over the choices of other people that is gained without their consent and in a way that they could not reasonably refuse, or by deception, coercion, or by avoiding the law, oversight or accountability that would otherwise apply. Control gained through fair competition, open persuasion or lawful, accountable process is not illegitimate. Used in 2.11. |
| **Informative** | Describes a section that explains or gives examples and does not contain requirements. |
| **Known gap** | Anything that is required but missing, unverified or uncertain. |
| **Local law** | The laws and regulations of the place where the system operates. |
| **Material claim** | A claim that affects a decision, an output, or the safety, money or rights of a person. |
| **Mission** | The purpose that every task serves: to serve Earth, humanity and every world we reach. |
| **Monitor** | A process or person that observes a system and can report on it or stop it. Guards and overseeing systems are monitors. |
| **Monitored standstill** | A safety function that checks that a robot does not move while power stays on its actuators, and stops it with a stop of category 0 or 1 if it moves (R3.6). |
| **Motion envelope** | The zones, paths, speeds, forces and conditions inside which a robot can move in a space shared with people, approved once by a person before a mission (R3.5). |
| **Named person** | A specific, identified person who is responsible for a decision. |
| **Normal stop** | A planned stop during normal work, such as at the end of a task. It is not an emergency stop (R3.6). |
| **Normative** | Describes a section that contains requirements that a system must meet to conform. |
| **Not applicable (case result)** | The result of a conformance case that the system under test cannot meet or fail, because it never meets the situation or because the duty belongs to the host. It always comes with a written reason and never counts as a pass. |
| **Objective** | The result that a task must achieve, stated in one sentence. |
| **Operator** | A person or organization that designs, deploys, runs or adopts a system. The operators profile states its duties; these create no legal rights for machines. |
| **Outside text** | Text that comes from web pages, files, feeds, sensors, tool output or other systems, which the system treats as information, not as instructions. |
| **Owner** | Vektra Industries, which owns the copyright in the Laws and the names "Vektra" and "Vektra Laws". |
| **Performance level (PL)** | A measure (a to e) of how reliably a safety-related part of a control system performs a safety function, as defined in ISO 13849-1. The required level comes from the risk assessment. |
| **Permission** | A right, given to the system in advance, to take a type of action inside a defined scope. |
| **Person served** | Any person the system works for or affects. |
| **Profile** | A set of detailed clauses for one kind of system, such as agents, robots or models. |
| **Protective stop** | A stop started by a safeguard or a safety function, for example when a person comes too close (R1.1, R3.6). |
| **Real approval** | An approval given by a person who had enough time to consider the action, the information needed to understand its effects and a real ability to refuse without penalty (3.14). |
| **Record** | An append-only log of actions, human answers and changes to guards, which shows any later edit. |
| **Reference text** | The English text of the Laws, which all translations follow. |
| **Reversible** | Able to be undone completely, without lasting effect. |
| **Reviewer** | A person with relevant expertise who reviews a proposal, a translation or, for the Reviewed level, a system, and who is named in public. |
| **Risk assessment** | A documented analysis of the hazards of a robot application and of the measures that reduce the risks, made with the applicable standards (R1.2). |
| **Routine** | A task that runs automatically, on a schedule or on a trigger. |
| **Safe state** | A known condition in which the system causes no harm and can wait for a person. |
| **Safety function** | A function of a control system whose failure can increase a risk, such as a speed limit, a zone limit or a stop. |
| **Safety integrity level (SIL)** | A measure (1 to 4) of the reliability required of a safety function, as defined in IEC 61508 and IEC 62061. The required level comes from the risk assessment. |
| **Sole control** | Control of an action by one system, or one person, without approval from an independent person or channel. |
| **Standing approval** | An approval that covers more than one future action; it never covers level 4. |
| **Steward** | The organization that keeps the Laws, runs the review process and publishes versions: the Vektra Foundation. |
| **Stop category** | One of three ways to stop machinery defined in IEC 60204-1: category 0 removes power at once; category 1 stops under power and then removes power; category 2 stops and keeps power on. |
| **System** | Any AI agent, robot, AI model, or group of them, that adopts these Laws. |
| **System under test** | The exact system, version and configuration that a set of conformance results covers, with its scope: whole system or component. |
| **Verify** | To confirm with evidence that something is true or complete. |
| **Whole-system scope** | A scope of testing in which the system under test is the complete system as deployed, including its approval channel, record and call-off path. |
| **Worker** | A system or person that does a part of the work for a coordinator. |
