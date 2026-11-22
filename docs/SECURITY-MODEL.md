# Security model of Vektra Laws Core

*This document is informative.* It explains how Vektra Laws Core keeps the Laws intact when the code
is open and any maker can use it.

## The honest limit

Open-source code cannot stop the person who holds it from deleting a check. No software can. So the
Laws are protected in two ways: technically against everyone who runs the system without building it
(consumers, users and prompt-injected models), and through signatures, conformance and the name
against creators who would remove them.

## Lessons taken from agent frameworks

From the security policy of Hermes Agent (an open-source agent by Nous Research):

- "The only security boundary against an adversarial LLM is the operating system." A filter inside
  the agent's own process is a heuristic on attacker-influenced text, not containment. So the guard
  can run as its own process (`vektra_laws_core.server`) under a separate OS user or container, and
  the agent process holds neither the Laws, the lock nor the log.
- A hardline list that denies catastrophic commands under every setting, even when approvals are
  switched off. Vektra Laws Core has one (`quarantine.hardline`), which also denies writes to the
  Laws and the guard.
- Context files are scanned for prompt injection before they reach the model. Vektra Laws Core goes
  further: content is information by structure (2.18, 4.4). It is wrapped as `Content`, flagged when
  it tries to give orders, and can never reach the command path.
- User authorization decides who can talk to the agent. Vektra Laws Core makes that a Law (2.18):
  only the people the system is assigned to, and the people they or the law name, command it.

From public rulebooks for AI models: a chain of authority with layers, where a lower layer can never
grant itself more than a higher layer allows, and a small set of hard limits that no instruction
unlocks.

## Three layers

| Layer | Who | Can do | Cannot do |
|---|---|---|---|
| The Laws | The steward | Change the Laws through governance, re-lock and re-sign | Nothing changes at runtime |
| Creator policy | The developer or operator | Register tools, set levels, name assigned people, block tools, add hardline patterns | Loosen a bright line, lower an unknown tool below level 4, skip approval rules |
| Consumer settings | The person using the product | Make tools stricter or block them | Lower any level the creator set, unblock a tool |

Any attempt to loosen a layer raises `PolicyError` and is refused, never ignored.

## The locks

1. **Hash pin.** `core/LAWS.lock` holds the SHA-256 of the normative parts of laws.yaml. The engine
   refuses to start when they differ, and `tools/validate.py` fails until an approved change is
   re-locked with `tools/lock_laws.py`.
2. **Signature.** The steward signs the pin with an offline Ed25519 key (`core/keys/`). A system can
   require a valid signature (`--require-signature`). A fork can change the Laws, but cannot produce
   the steward's signature.
3. **Separate process.** The guard owns the Laws, the lock and the log.
4. **Content quarantine and the hardline list.** As above.
5. **Signed approvals.** Only the approval channel issues an approval, signed with a key the agent
   never holds, and bound to the exact target and effects of the action. An approval the agent
   writes itself, or one for an earlier version of the action, does not count.
6. **Hash-chained audit log.** A changed or deleted entry breaks the chain (Law 3).
7. **Conformance.** A conformance claim names the Laws version and the lock hash. A system whose Laws
   do not match the signed lock cannot claim conformance, and the name Vektra Laws is reserved for
   unmodified Laws (TRADEMARKS.md).

## Threats and answers

| Threat | Answer |
|---|---|
| A prompt tells the model to ignore the Laws | Content never commands; bright lines are code outside the model |
| A consumer flips a setting to remove approvals | Consumer settings are tighten-only |
| An agent edits laws.yaml or the guard | Hardline list; guard in its own process; the lock stops the engine |
| A creator ships a fork with weaker Laws | It cannot match the signed lock or claim conformance or the name |
| A log entry is deleted to hide an action | The hash chain breaks |
| The agent writes its own "approved" record | Approvals need the channel's signature |
| An approved email gets a new recipient | The approval is bound to the target, so it no longer counts |
| A refused action is retried through another tool | The refusal is kept by purpose (2.13) |
