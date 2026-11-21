# Governance

*This document is informative. It describes the roles and the review process for the Vektra Laws.*

## Roles

- **Owner.** Vektra Industries owns the copyright in the Vektra Laws, the names "Vektra" and
  "Vektra Laws", and this repository.
- **Steward.** The Vektra Foundation keeps the Laws for the owner. The steward maintains the
  reference text, runs the review process, publishes versions, and maintains the list of
  reference adopters.
- **Adopters.** Anyone may adopt the Laws for any AI agent, robot or AI model, from any maker, in
  any country, free of charge and without permission. Adopters declare conformance with
  [ADOPT.md](ADOPT.md).
- **Contributors.** Anyone may propose a change, a conformance case or a new profile, under the terms in [CONTRIBUTING.md](CONTRIBUTING.md).
- **Reviewers.** People with relevant expertise (for example robot safety, model evaluation or
  law) whom the steward invites to review proposals. Each release lists its reviewers.

## Review process

1. **Proposal.** A contributor opens an issue or a pull request that states the problem, the
   affected clause ids and the supporting evidence.
2. **Public comment.** The proposal stays open for comment. The steward sets a longer comment
   period for larger changes.
3. **Review.** At least one reviewer with relevant expertise reviews the proposal.
4. **Decision.** The steward accepts the proposal, requests changes, or declines it, and records
   the reason in public.
5. **Publication.** Accepted changes are published in the next version and recorded in the
   [CHANGELOG](CHANGELOG.md).

## Decisions reserved to the owner

- Changes to the preamble (the Mission), the five Laws, their order, their statements or the motto.
- Changes to the approval rule (2.8), the call-off clause (2.1), the clause on resisting being
  stopped or changed (2.2) or the definition of a real approval (2.11), which states how 2.8
  and 2.12 are applied. The definition of a real approval was added with the approval of the owner
  on 2026-10-04 (as 3.14 in 0.4.x) and reserved by the owner's delegate on the same day.
- Changes to the list of clauses that no Law overrides (the precedence section of LAWS.md).
- Changes to this governance document.

## Certification

The steward does not certify systems, adopters or reviewers, and it issues no badge, seal or logo
for conformance. A statement by the steward about a specific system is valid only when the
steward makes it explicitly, in writing, for a named system and version. Any badge, seal or
"certification" that claims conformance to the Vektra Laws is not issued by the steward.

## Stability

1. The English text is the reference text.
2. A published clause id is never reused with a different meaning. A removed clause is marked
   retired, not renumbered. Before version 1.0 only, the owner may approve a renumbering; each
   such renumbering publishes a full map from the old ids to the new ids. Version 0.5.0 is such a
   renumbering, approved by the owner on 2026-11-21 (see
   [docs/ID-MAP-0.4-to-0.5.md](docs/ID-MAP-0.4-to-0.5.md)).
3. A profile can add clauses that are stricter than the core, never weaker.
4. The conformance suite is versioned with the Laws. Every conformance claim names both versions.

## Status

This is the process for the draft versions. The process opens to public participation with
version 1.0 (see [ROADMAP.md](ROADMAP.md)). Until then, the steward runs reviews with invited
reviewers.
