# Contributing

*This document is informative. It describes how to contribute to the Vektra Laws.*

Contributions are welcome from anyone. All proposals go through the review process in
[GOVERNANCE.md](GOVERNANCE.md). Participants follow the [code of conduct](CODE_OF_CONDUCT.md).

## Types of contribution

- **Conformance cases.** A situation that the Laws handle incorrectly, or do not handle, written in
  the case format in [tests/README.md](tests/README.md).
- **Profile review**, in particular for robotics and models, from practitioners in those fields.
- **Editorial changes** that make the text clearer or easier to read.
- **New profiles** for other kinds of systems.
- **Problem reports** (see [SECURITY.md](SECURITY.md)).

## Requirements for every contribution

1. **Developer Certificate of Origin.** Every commit MUST carry a `Signed-off-by` line, added with
   `git commit -s`. By signing off, the contributor certifies the
   [Developer Certificate of Origin, version 1.1](https://developercertificate.org/). The full
   text at that link is what the contributor certifies. In short: (a) the contributor created the
   contribution and has the right to submit it under the license indicated in the file; or (b) it
   is based on earlier work under an appropriate open license that allows this; or (c) it was
   given to the contributor by someone who certified (a), (b) or (c), unchanged; and (d) the
   contributor understands that the contribution and the sign-off, including the name and email
   given, are public and are kept permanently. The license for each file is stated in
   [LICENSE](LICENSE). Pull requests with commits that are not signed off are not merged.
2. **Licenses.** Text contributions are licensed under CC BY 4.0, and code contributions under the
   MIT License, the same as the rest of the repository.
3. **Edit the sources.** Edit `laws.yaml`, not the generated files.
   Then run `python tools/build_docs.py`.
4. **Validate.** Run `python tools/validate.py` before opening a pull request. Continuous
   integration runs it as well.
5. **Stable ids.** Do not renumber published clauses, and do not reuse an id with a new meaning.
6. **Sources.** Every figure, limit or factual claim needs a cited source. Do not add statistics
   without one.

## Writing rules

These rules apply to the normative text (the Laws, the profiles, the action levels and the
conformance levels). The validator checks several of them.

1. **Universal.** Name no maker, product, platform or internal tool. Use "the system" and "the
   people it serves".
2. **Controlled English.** Short sentences, one idea per sentence. No idioms, slang, contractions
   or culture-specific references. Use the terms in [GLOSSARY.md](GLOSSARY.md), and use each term
   in one meaning only.
3. **Key words.** Use MUST, MUST NOT, SHOULD and MAY only as defined in BCP 14 (RFC 2119 and RFC
   8174).
4. **No legal claims.** Do not use words that suggest legal authority or guarantees, such as
   "guarantee", "certified", "compliant" or "ensures safety". Use "conforms to" or "declares
   conformance".
5. **Profiles add, never weaken.** A profile clause sits under one of the five Laws and can be
   stricter than the core, never weaker.
6. **Owner approval.** Changes to the five Laws, their order, their statements or the motto need
   the owner's approval (see [GOVERNANCE.md](GOVERNANCE.md)).

## Adapted versions

The text is licensed under CC BY 4.0, so anyone can adapt it with attribution, and CC BY 4.0
requires an indication of what was changed. Under the policy on the names in
[TRADEMARKS.md](TRADEMARKS.md), which concerns trademark rights only, an adapted version uses a
different name and does not suggest endorsement.
