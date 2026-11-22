# Names and marks

*This document is informative. It describes how the names of the project may be used.*

## Names

"Vektra" and "Vektra Laws" are names of Vektra Industries. No trademark registration is claimed.
Any rights in the names are unregistered rights that come from their use. The names may be shown
with the ™ symbol. The ® symbol is never used with them, because it is only for marks registered
with a national office, such as the United States Patent and Trademark Office (USPTO).

The CC BY 4.0 license (for the text) and the MIT license (for the code) cover the content of this
repository. They do not grant any right to use these names, except as described below. The CC BY
4.0 license also does not license trademark rights (Section 2(b)(2)) and does not permit any
suggestion of endorsement (Section 2(a)(6)). This page is a policy on the names only. It does not
restrict any right that CC BY 4.0 or the MIT license grants in the text or the code: anyone can
copy and adapt the text under CC BY 4.0, with attribution.

Other parties own registered marks that are similar to VEKTRA. The Vektra Laws are not
affiliated with any of them.

## Permitted uses

- **Factual statements of conformance.** For example: "This system declares conformance to the
  Vektra Laws 0.5.0, agents profile, at the Adopts level." The statement must be accurate and must
  follow the conformance rules in [LAWS.md](LAWS.md) and [ADOPT.md](ADOPT.md).
- **Citation and reference.** Naming the Vektra Laws in research, articles, policies or
  documentation, with attribution as described in [CITATION.cff](CITATION.cff).
- **Unmodified copies.** Sharing an unmodified copy of a published version under its own name.

## Uses that are not permitted

- Using the names in a way that suggests endorsement, certification, sponsorship or partnership
  by Vektra Industries or the Vektra Foundation (planned, not yet formed), when there is none.
- Using the names, or the conformance levels, as a badge, seal or logo, or in a label such as
  "Vektra Reviewed", "Vektra Verified" or "Vektra certified". The steward issues no badge and certifies nothing
  (see [ADOPT.md](ADOPT.md)).
- Publishing an adapted or modified version of the Laws under the name "Vektra Laws" or a
  confusingly similar name. An adapted version uses a different name. It can, and under CC BY
  4.0 must, credit the source, for example "adapted from the Vektra Laws 0.5.0", and indicate
  what was changed.
- Using the names as part of the name of a product, service or organization without written
  permission.

## The Laws lock (0.6.0 and later)

From version 0.6.0, the normative parts of each published version are pinned by a SHA-256 hash in
`core/LAWS.lock`, and the steward signs that hash. The name follows the lock:

- **"Vektra Laws" means Laws whose normative parts match the published, signed lock** for that
  version. A system whose Laws do not match the lock does not use the name, and it cannot declare
  conformance.
- **A conformance declaration names the lock hash** it was tested against (the `laws_lock_sha256`
  field of a results file and the "Laws lock" line of the declaration in [ADOPT.md](ADOPT.md)).
  Anyone can check the claim by comparing the hash with the published lock.
- **Vektra Laws Core.** Anyone can use, change and ship the code under the MIT license. A product
  may say that it "uses Vektra Laws Core" only when the engine runs with the published lock and the
  check is switched on. A product that changes or removes the Laws, the lock check or the bright
  lines uses a different name and does not refer to itself as following the Vektra Laws.

These rules are about the names. They do not restrict what CC BY 4.0 or the MIT license allow
anyone to do with the text and the code.

## Registration

No registration has been filed.

## Questions

Open an issue in this repository with the label `names`.
