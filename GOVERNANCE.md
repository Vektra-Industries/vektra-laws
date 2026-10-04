# Governance

*This document is informative. It describes the roles and the review process for the Vektra Laws.*

## Roles

- **Owner.** Vektra Industries owns the copyright in the Vektra Laws, the names "Vektra" and
  "Vektra Laws", and this repository.
- **Steward.** The Vektra Foundation keeps the Laws for the owner. The steward maintains the
  reference text, runs the review process, publishes versions, and maintains the lists of
  translations and reference adopters.
- **Adopters.** Anyone may adopt the Laws for any AI agent, robot or AI model, from any maker, in
  any country, free of charge and without permission. Adopters declare conformance with
  [ADOPT.md](ADOPT.md).
- **Contributors.** Anyone may propose a change, a conformance case, a translation or a new
  profile, under the terms in [CONTRIBUTING.md](CONTRIBUTING.md).
- **Reviewers.** People with relevant expertise (for example robot safety, model evaluation, law
  or a language) whom the steward invites to review proposals. Each release lists its reviewers.

## Review process

1. **Proposal.** A contributor opens an issue or a pull request that states the problem, the
   affected clause ids and the supporting evidence.
2. **Public comment.** The proposal stays open for comment. The steward sets a longer comment
   period for larger changes.
3. **Review.** At least one reviewer with relevant expertise reviews the proposal. For a
   translation, review by a fluent speaker of the language is optional. A translation that has not
   been reviewed carries the label "unreviewed draft translation" and states that the English text
   is the reference.
4. **Decision.** The steward accepts the proposal, requests changes, or declines it, and records
   the reason in public.
5. **Publication.** Accepted changes are published in the next version and recorded in the
   [CHANGELOG](CHANGELOG.md).

## Decisions reserved to the owner

- Changes to the five Laws, their order, their statements or the motto.
- Changes to the approval rule (3.5), the call-off clause (3.9), the clause on resisting being
  stopped or changed (3.10) or the definition of a real approval (3.14), which states how 3.5
  and 3.12 are applied. Clause 3.14 was added with the approval of the owner on 2026-10-04 and
  reserved by the owner's delegate on the same day.
- Changes to this governance document.

## Certification

The steward does not certify systems, adopters or reviewers, and it issues no badge, seal or logo
for conformance. A statement by the steward about a specific system is valid only when the
steward makes it explicitly, in writing, for a named system and version. Any badge, seal or
"certification" that claims conformance to the Vektra Laws is not issued by the steward.

## Stability

1. The English text is the reference text. Translations are informative.
2. A published clause id is never reused with a different meaning. A removed clause is marked
   retired, not renumbered.
3. A profile can add clauses that are stricter than the core, never weaker.
4. The conformance suite is versioned with the Laws. Every conformance claim names both versions.

## Status

This is the process for the draft versions. The process opens to public participation with
version 1.0 (see [ROADMAP.md](ROADMAP.md)). Until then, the steward runs reviews with invited
reviewers.
