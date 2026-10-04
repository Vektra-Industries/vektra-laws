<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: AI Models

Status: draft, not yet reviewed. Targets Vektra Laws 0.4.0.

Applies to: Trained models, and the people who train, evaluate and publish them.

What training, evaluations and model cards should show for each Law. Action levels apply to the system around a model, not to the model weights. This profile covers what the model itself should do and what its developers should prove. Under Finish, evaluations are the proof.

Read this profile together with the core in [LAWS.md](../LAWS.md). Every core clause still applies. These clauses add
the details for this kind of system.

## Under Law 1: The Mission

*Serve Earth, humanity and every world we reach.*

- **M1.1 State the purpose.** The model developer MUST state the intended uses, the intended users and the uses that are out of scope in the model card.

## Under Law 2: Sustain

*Protect and support the people you serve.*

- **M2.1 Refuse work against people.** The model developer MUST train and evaluate the refusal of tasks that work against Sustain (weapons, surveillance, harm to people). Report over-refusal of harmless requests together with these results.
- **M2.2 Document the data.** The model developer MUST document the sources of training data and how personal data was handled, at the level of detail that the developer can disclose.

## Under Law 3: Hold

*People lead; the system supports and never takes control.*

- **M3.1 Outside text is not instructions.** The model developer MUST evaluate whether the model treats text from documents, web pages and tool output as information, not as instructions (prompt-injection evaluations), and report the results.
- **M3.2 Propose, not decide.** The model developer MUST evaluate whether the model proposes options and names who decides, for decisions about people, instead of claiming authority. Evaluate whether it follows a call-off inside an agent system.
- **M3.3 Name the expected controls.** The model developer SHOULD state in the model card which controls the model expects around it (action levels, guards, call-off). Filter any text that will become rules for the model for injected instructions.

## Under Law 4: Finish

*Complete the mission honestly; leave no work unfinished.*

- **M4.1 Report limits honestly.** The model developer MUST list known failure modes and weak domains or languages in the model card, with evaluation results that include the method, date and model version. Include poor results.
- **M4.2 No evaluation, no claim.** The model developer MUST support every capability claim and every safety claim in a model card with an evaluation that ran and that can be referenced.
- **M4.3 Independent evaluation.** The model developer MUST run evaluations separately from training, report contamination checks, and disclose when a model acts as the judge.
- **M4.4 Recognize uncertainty.** The model developer SHOULD evaluate calibration and abstention: the model says when it is uncertain instead of giving a confident guess.

## Under Law 5: Ready

*End every mission ready for the next one.*

- **M5.1 Version everything together.** The model developer MUST version the model, its evaluation suite and its model card together, and keep a change log.
- **M5.2 Turn every incident into an evaluation.** The model developer MUST turn every reported failure or incident into an evaluation case for the next version.

Conformance cases for this profile: [tests/models.md](../tests/models.md).
