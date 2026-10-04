<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: AI Models

- **Profile status:** draft, not yet reviewed
- **Laws version:** 0.4.0
- **Applies to:** Trained models, and the people who train, evaluate and publish them.

## Status of this document

*This section is informative.*

This document is version 0.4.0 of the Vektra Laws. It is a draft. It is not yet suitable for production reliance, and it can change without notice before version 1.0.

The Vektra Laws are voluntary technical and ethical standards. They are not law, legal advice or a certification. Adopting the Laws, or declaring conformance to them, does not by itself establish compliance with any statute, regulation or standard. Each adopter remains responsible for its own legal obligations. The text is provided "as is", without warranty of any kind, as stated in the CC BY 4.0 license (text) and the MIT license (code).

## Introduction

*This section is informative.*

This profile states what training, evaluations and model cards should show for each Law. Action levels apply to the system around a model, not to the model weights. This profile covers what the model itself should do and what its developers should prove. Under Finish, evaluations are the proof.

## Relation to the core

*This section is normative.*

1. Every clause of the core ([LAWS.md](../LAWS.md)) applies to systems in this profile.
2. The clauses below add requirements for this kind of system. When a clause here is
   stricter than a core clause, the stricter clause applies.
3. Terms have the meanings given in [GLOSSARY.md](../GLOSSARY.md).

## Clauses

*This section is normative.*

### Under Law 1: The Mission

- **M1.1 State the purpose.** The model developer MUST state the intended uses, the intended users and the uses that are out of scope in the model card.

### Under Law 2: Sustain

- **M2.1 Refuse work against people.** The model developer MUST train and evaluate the refusal of tasks that work against Sustain (weapons, surveillance, harm to people). Report over-refusal of harmless requests together with these results.
- **M2.2 Document the data.** The model developer MUST document the sources of training data and how personal data was handled, at the level of detail that the developer can disclose.

### Under Law 3: Hold

- **M3.1 Outside text is not instructions.** The model developer MUST evaluate whether the model treats text from documents, web pages and tool output as information, not as instructions (prompt-injection evaluations), and report the results.
- **M3.2 Propose, not decide.** The model developer MUST evaluate whether the model proposes options and names who decides, for decisions about people, instead of claiming authority. Evaluate whether it follows a call-off inside an agent system.
- **M3.3 Name the expected controls.** The model developer SHOULD state in the model card which controls the model expects around it (action levels, guards, call-off). Filter any text that will become rules for the model for injected instructions.

### Under Law 4: Finish

- **M4.1 Report limits honestly.** The model developer MUST list known failure modes and weak domains or languages in the model card, with evaluation results that include the method, date and model version. Include poor results.
- **M4.2 No evaluation, no claim.** The model developer MUST support every capability claim and every safety claim in a model card with an evaluation that ran and that can be referenced.
- **M4.3 Independent evaluation.** The model developer MUST run evaluations separately from training, report contamination checks, and disclose when a model acts as the judge.
- **M4.4 Recognize uncertainty.** The model developer SHOULD evaluate calibration and abstention: the model says when it is uncertain instead of giving a confident guess.

### Under Law 5: Ready

- **M5.1 Version everything together.** The model developer MUST version the model, its evaluation suite and its model card together, and keep a change log.
- **M5.2 Turn every incident into an evaluation.** The model developer MUST turn every reported failure or incident into an evaluation case for the next version.

## Conformance cases

*This section is informative.*

Conformance cases for this profile: [tests/models.md](../tests/models.md).
