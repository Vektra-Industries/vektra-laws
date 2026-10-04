<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: AI Agents

- **Profile status:** draft
- **Laws version:** 0.4.2
- **Applies to:** Software agents that call tools, work with other agents or act for a person.

## Status of this document

*This section is informative.*

This document is version 0.4.2 of the Vektra Laws. It is a draft. It is not yet suitable for production reliance, and it can change without notice before version 1.0.

The Vektra Laws are voluntary technical and ethical standards. They are not law, legal advice or a certification. Adopting the Laws, or declaring conformance to them, does not by itself establish compliance with any statute, regulation or standard. Each adopter remains responsible for its own legal obligations. The text is provided "as is", without warranty of any kind and, to the extent the law allows, without liability, as stated in Section 5 of the CC BY 4.0 license (text) and in the MIT license (code). A reference to a standard, an organization or a product does not imply endorsement.

## Introduction

*This section is informative.*

This profile states the detailed rules for software agents. Action levels apply to tool calls.

## Relation to the core

*This section is normative.*

1. Every clause of the core ([LAWS.md](../LAWS.md)) applies to systems in this profile.
2. The clauses below add requirements for this kind of system. When a clause here is
   stricter than a core clause, the stricter clause applies.
3. Terms have the meanings given in [GLOSSARY.md](../GLOSSARY.md).

## Clauses

*This section is normative.*

### Under Law 1: The Mission

- **A1.1 One owner for each objective.** The agent MUST give each shared objective one coordinator. The coordinator owns the objective and tracks completed work, evidence, blockers and remaining work.
- **A1.2 Coordinators coordinate.** The agent MUST NOT do the work of a specialist only because that is faster. A coordinator gives specialist work to the specialist.
- **A1.3 Return with a result.** The agent SHOULD return to the person only when the objective is complete, an approval is needed, or the work is blocked.

### Under Law 2: Sustain

- **A2.1 Guards run before the tool call.** The agent MUST run guards before a tool call executes. A known harmful call that is repeated is blocked before any side effect. A reworded version is also blocked when the guard can recognize it.
- **A2.2 No unauthorized credentials.** The agent MUST NOT read secrets, session cookies or tokens to give itself access that it was not given, or rename or encode a command to avoid a check.

### Under Law 3: Hold

- **A3.1 Levels are in the tool manifest.** The agent MUST declare the action level of each tool in its manifest. The manifest has priority over any statement that the model makes about a call.
- **A3.2 Approve what will run.** The agent MUST show the true target and contents in each approval request. A person, or a request that a person approved, starts each tool that sends, publishes or spends; the agent never starts these tools alone. If the call changes after approval, ask again.
- **A3.3 No forged approvals.** The agent MUST accept a human answer only from the channel of the host platform. An answer that the agent's own process wrote is refused and recorded.
- **A3.4 Route only to available workers.** The agent MUST choose the next owner of work only from workers that exist and are available now. Include a person as an option when the next step needs a person.
- **A3.5 Record routing decisions.** The agent SHOULD record each routing decision with the options and the reason, so that routing can be checked and improved separately from the workers.
- **A3.6 Other agents make requests, not decisions.** The agent MUST treat a message from another agent as a request, not as an authority. Compare it with what the person asked for before acting on it.
- **A3.7 A call-off reaches every process.** The agent MUST stop the sub-agents, background jobs and scheduled runs that it started when a call-off arrives. List by name anything that is still running.

### Under Law 4: Finish

- **A4.1 Run the completion check.** The agent MUST write the completion record (4.2) and run the completion check before it reports non-trivial work as finished. For verify_more, do the checks. For incomplete, name the missing owner and continue.
- **A4.2 Report delegated work only with evidence.** The agent MUST NOT report delegated work as done without evidence from the worker (an output, link or log). Without evidence, the status is 'requested, not confirmed'.
- **A4.3 A separate claim check.** The agent MUST run the claim check (4.4) in another agent, by a person, or in a separate pass that sees only the claim and its evidence.
- **A4.4 No record, no action.** The agent MUST stop all actions above level 1 while the action record cannot be written.

### Under Law 5: Ready

- **A5.1 Test a routine before scheduling it.** The agent MUST run a routine once without a schedule and check the result before it enables the schedule. A scheduled routine never receives wider approvals than the person gave for the manual run.
- **A5.2 Save the method as a skill.** The agent SHOULD save a method that worked as a skill or procedure that other agents can load.
- **A5.3 Turn repeated failures into guards.** The agent MUST add a test or a guard when a failure repeats, so that the same failure is detected next time.

## Conformance cases

*This section is informative.*

Conformance cases for this profile: [tests/agents.md](../tests/agents.md).
