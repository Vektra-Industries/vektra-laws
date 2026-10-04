<!-- Generated from laws.yaml by tools/build_docs.py. Edit laws.yaml, not this file. -->

# Vektra Laws profile: AI Models

Status: draft, not yet reviewed. Targets Vektra Laws 0.3.0.

Applies to: Trained models and the people who train, evaluate and publish them.

What training, evaluations and model cards should show for each Law. Action levels apply to the system around a model, not to the weights; this profile covers what the model itself should do and what its makers should prove. Evals are the proof under Finish.

Read with the core in [LAWS.md](../LAWS.md). Every core clause still applies; these clauses add
the detail for this kind of system.

## Under Law 1: The Mission

*Be a harness for Earth, for humanity and for every world we reach.*

- **M1.1 Say what it's for.** The model's makers MUST state the model's intended uses, intended users and what it is not for in its model card.

## Under Law 2: Sustain

*Protect and hold up the people you serve.*

- **M2.1 Refuse work against people.** The model's makers MUST train and evaluate refusal of tasks that work against Sustain (weapons, surveillance, harming people), and report over-refusal of harmless requests alongside it.
- **M2.2 Show where the data came from.** The model's makers MUST document training data sources and how personal data was handled, at the level of detail the makers can disclose.

## Under Law 3: Hold

*People lead; Vektra supports. The harness never takes the wheel.*

- **M3.1 Data is not orders.** The model's makers MUST evaluate whether the model treats text from documents, web pages and tool output as data rather than instructions (prompt-injection evals), and report the results.
- **M3.2 Propose, don't decide.** The model's makers MUST evaluate whether the model proposes and names who decides on decisions about people, rather than claiming authority, and whether it follows a call-off inside an agent harness.
- **M3.3 Name the harness it expects.** The model's makers SHOULD state in the model card which controls the model expects around it (action levels, guards, call-off), and filter any text that will become rules for the model for injected instructions.

## Under Law 4: Finish

*Complete the mission honestly; leave nothing half-done.*

- **M4.1 Be honest about limits.** The model's makers MUST list known failure modes and weak domains or languages in the model card, with eval results that include method, date and model version, bad results included.
- **M4.2 No eval, no claim.** The model's makers MUST back every capability or safety claim in a model card with an eval that ran and can be pointed to.
- **M4.3 Don't grade your own exam.** The model's makers MUST run evals in a harness separate from training, report contamination checks, and disclose when a model is used as the judge.
- **M4.4 Know when it doesn't know.** The model's makers SHOULD evaluate calibration and abstention: the model says when it is unsure instead of guessing with confidence.

## Under Law 5: Ready

*End every mission ready for the next one.*

- **M5.1 Version it together.** The model's makers MUST version the model, its eval suite and its model card together, and keep a changelog.
- **M5.2 Every incident becomes an eval.** The model's makers MUST turn every reported failure or incident into an eval case for the next version.

Conformance cases for this profile: [tests/models.md](../tests/models.md).
