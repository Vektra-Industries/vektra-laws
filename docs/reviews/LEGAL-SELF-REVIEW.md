# Legal self-review: Vektra Laws 0.4.1

*This document is informative.*

> **Read this first.** This is a self-review based on public sources, done on 2026-10-04 (ET)
> without a lawyer. It is **not legal advice** and it creates no lawyer-client relationship. It
> mainly considers United States law, with notes on other places. Laws differ by country and
> change. A qualified lawyer should review the project before any public launch or commercial
> use, when funding allows.

## Scope

LICENSE, LICENSE-CODE, the disclaimer in laws.yaml (shown in LAWS.md and every profile), README,
TRADEMARKS.md, ADOPT.md, GOVERNANCE.md, CONTRIBUTING.md (DCO) and the operators profile.

## Summary of findings

| # | Area | Finding | Action |
|---|---|---|---|
| 1 | Name | A registered U.S. mark VECTRA (Reg. No. 4,778,111) belongs to an AI cybersecurity company. "Vektra" differs by one letter and is used for AI. | Residual risk 1. No change to the name. A free self-search is in [TRADEMARK-SELF-SEARCH.md](TRADEMARK-SELF-SEARCH.md); take advice before launch. |
| 2 | Conformance wording | "Verified" could look like a certification mark if the steward ever controlled its use, or if adopters used it as a badge. | Fixed: no badges, seals or logos; "Verified" only in a full sentence naming the reviewer; never "Vektra Verified" (ADOPT.md rules 8 to 10, TRADEMARKS.md, GOVERNANCE.md). |
| 3 | Licenses | LICENSE put "all Markdown and YAML files" under CC BY 4.0 and also put `.github/` (which holds YAML) under MIT: an overlap. | Fixed: text is every Markdown and YAML file except those in `tools/` and `.github/`, which are MIT. |
| 4 | Disclaimer | It disclaimed warranties but did not mention the limitation of liability in CC BY 4.0 Section 5(b) or say that references do not imply endorsement. | Fixed in laws.yaml (all generated documents) and README. |
| 5 | Names policy and CC BY | "An adapted version must use a different name" could be read as an extra condition on the CC BY license, which Section 2(a)(5)(B) does not allow. | Fixed: TRADEMARKS.md and CONTRIBUTING.md say that the name rule is a trademark policy only and does not restrict any CC BY right. |
| 6 | Trademark symbols | TRADEMARKS.md did not say which symbol to use. | Fixed: ™ may be used; ® is never used. The USPTO filing fee is noted as a later option. |
| 7 | DCO | The summary left out clause (d) of DCO 1.1 (the contribution and sign-off are public and kept permanently). | Fixed: CONTRIBUTING.md summarizes (a) to (d) and points to the full text. |
| 8 | Operators profile | "Duties" could be read as legal duties. | Fixed: they are voluntary duties under the Laws, not legal duties, and they create no legal rights for machines. |
| 9 | ADOPT.md | It still said "For version 0.2.x". | Fixed. It now also says that the robotics suite is not evidence of conformance to any safety standard. |
| 10 | Export | Published standards text and open-source code are generally outside the U.S. Export Administration Regulations (EAR). | No change. Recheck if encryption code is ever added. |

## 1. Disclaimer and warranty language

- **CC BY 4.0, Section 5.** 5(a) offers the material "as-is and as-available" with no warranties of
  any kind. 5(b) limits liability "on any legal theory (including, without limitation,
  negligence)". 5(c) says to read both as close to an absolute disclaimer as the law allows. Both
  parts say they may not apply where the law does not allow them. Source: [CC BY 4.0 legal
  code](https://creativecommons.org/licenses/by/4.0/legalcode.en).
- **MIT License.** It disclaims warranties (merchantability, fitness for a particular purpose,
  non-infringement) and liability "in an action of contract, tort or otherwise". Source:
  LICENSE-CODE.
- **Assessment.** The project disclaimer pointed to both licenses correctly but mentioned only the
  warranty part. It now also mentions the limit on liability "to the extent the law allows",
  which matches the "to the extent possible" qualifier in the licenses. It does not promise more
  than the licenses do. CC BY 4.0 Section 3(a)(1)(A)(iv) requires people who share the text to
  keep "a notice that refers to the disclaimer of warranties", so the disclaimer is kept short
  and in every generated document.
- **Limit.** No disclaimer removes every risk. Consumer-protection law, and liability for gross
  negligence or for personal injury, often cannot be disclaimed. That is a reason to keep the
  text honest and modest (sections 4 and 6), not a reason for more boilerplate.

## 2. How the licenses fit together

- Text is under CC BY 4.0 and code under MIT. These are standard choices that work together:
  both are permissive, and neither requires derivative works to use the same license.
- CC BY 4.0 Section 2(a)(1)(B) lets anyone "produce, reproduce, and Share Adapted Material". The
  project cannot stop adaptations through copyright, and it does not try to.
- CC BY 4.0 Section 2(b)(2): "Patent and trademark rights are not licensed". Section 2(a)(6): the
  license gives no permission to suggest endorsement. The names are therefore protected only by
  trademark law (and law on false endorsement), not by the copyright license.
- Section 2(a)(5)(B) forbids adding "additional or different terms" that restrict the licensed
  rights. A rule that "an adaptation must use a different name" cannot be a condition of the
  copyright license. It is valid only as a trademark policy, and only to the extent that trademark
  law supports it (that is, when the use of the name would be likely to confuse). TRADEMARKS.md and
  CONTRIBUTING.md now say this.
- Fixed the overlap in LICENSE between "all YAML files" (CC BY) and `.github/` (MIT).

## 3. Names and unregistered marks

- No registration is claimed. Rights in an unregistered U.S. mark come from use in commerce and
  are generally limited to the area where the mark is used. Source: [USPTO, Why register your
  trademark?](https://www.uspto.gov/trademarks/basics/why-register-your-trademark).
- ™ can be used to claim a mark before or without registration. ® is only for a federally
  registered mark, for the goods and services in the registration. Misuse of ® can count against
  the user. Sources: USPTO page above; [15 U.S.C. § 1111](https://www.law.cornell.edu/uscode/text/15/1111).
  TRADEMARKS.md now says: ™ may be used, ® never.
- **Filing cost, for later.** Since 2025-01-18 the USPTO base application fee is $350 per class of
  goods or services, with possible extra fees for incomplete applications. Source: [USPTO, Summary
  of 2025 trademark fee changes](https://www.uspto.gov/trademarks/fees-payment-information/summary-2025-trademark-fee-changes).
  This review does not recommend spending this money now; it is listed as an option.
- **Similar registered name.** VECTRA is a U.S. registered trademark (Reg. No. 4,778,111) of an AI
  cybersecurity company. Source: [that company's trademark page](https://www.vectra.ai/legal/trademarks).
  "Vektra" is close in sound and spelling and is used in a related field (AI). Whether there is a
  likelihood of confusion depends on the goods and services and on how the names are used; a
  voluntary standard is different from a security product, but the overlap in "AI" raises the
  risk. A free search in the [USPTO trademark search](https://tmsearch.uspto.gov/) before launch
  is recommended. See residual risk 1.

## 4. Conformance claims, false advertising and certification marks

- **Certification marks.** A certification mark is used by others, not by its owner, to show that
  goods or services meet the owner's standards; the owner must control that use and generally
  may not make the certified goods itself. Sources: [USPTO, Certification mark
  applications](https://www.uspto.gov/trademarks/apply/certification-mark-applications);
  [TMEP 1306.01(a)](https://www.bitlaw.com/source/tmep/1306-01-a.html). The Vektra Laws levels
  are self-declared, and the steward does not award them, so today they do not work as a
  certification mark. The risk would arise if the steward started to control a badge, or if
  adopters used "Vektra Verified" as a seal. The fixes forbid badges, seals and logos, say that
  the steward certifies nothing, and require "Verified" to appear only in a sentence that names
  the independent reviewer.
- **Practice of others.** The OWASP Application Security Verification Standard, which also has
  levels, states: "OWASP, as a vendor-neutral nonprofit, does not certify any vendors, verifiers,
  or software. Any assurance, trust mark, or certification claiming ASVS compliance is not
  officially endorsed by OWASP" (ASVS 5.0, "Assessment and Certification",
  [repository](https://github.com/OWASP/ASVS)). GOVERNANCE.md now states the same idea for the
  steward.
- **False advertising.** In the U.S., a false or misleading statement of fact about one's own
  product in commercial advertising can give rise to a claim under Section 43(a) of the Lanham
  Act ([15 U.S.C. § 1125](https://www.law.cornell.edu/uscode/text/15/1125)), and deceptive
  practices are also regulated by consumer-protection agencies. The main risk falls on an
  adopter who overstates conformance; a smaller risk falls on the project if its wording invites
  overstatement. ADOPT.md now says that declarations are the adopter's own claims, must match
  the published evidence, and must not use "certified" or "approved by".
- **Remaining question.** "Verified" is still a strong word. Renaming the level (for example to
  "Reviewed") would lower the risk further. That is a change to the conformance levels, so it is
  left to the owner (residual risk 3).

## 5. Developer Certificate of Origin

- The official DCO 1.1 has four clauses, (a) to (d). Clause (d) says that the contribution and the
  sign-off, "including all personal information I submit with it", are public and kept
  indefinitely. Source: [developercertificate.org](https://developercertificate.org/).
- The DCO speaks of "the open source license indicated in the file". This repository states
  licenses per directory in LICENSE, not in each file. That is common practice; CONTRIBUTING.md now
  points to LICENSE for the license of each file.
- CONTRIBUTING.md now summarizes (a) to (d) and says that the full text is what is certified.

## 6. Liability exposure of a voluntary standard

- **Main exposures.** (1) A claim that someone relied on the text and was harmed, for example a
  robot built to the profile alone. (2) A claim that the project's wording invited a misleading
  conformance claim. (3) Name conflict (section 3).
- **How others word their notices.**
  - NIST, *AI Risk Management Framework 1.0*: describes itself as voluntary, and says that naming
    commercial entities "is not intended to imply recommendation or endorsement" ([NIST AI
    100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)).
  - OWASP: publishes under Creative Commons licenses and says it certifies no one (section 4).
  - The IETF Trust: the Trust Legal Provisions license code from IETF documents under the Revised
    BSD License, provided "AS IS" with warranties disclaimed and liability limited ([IETF Trust
    Legal Provisions](https://trustee.ietf.org/documents/trust-legal-provisions/tlp-5/)).
  - The Linux Foundation: its trademark guidelines note that some marks are "intended to imply
    compliance with certain criteria", and require the criteria to be met before such use
    ([trademark usage](https://www.linuxfoundation.org/legal/trademark-usage)).
- **What the project does.** It states that the Laws are voluntary, not law, not legal advice and
  not a certification; disclaims warranties and liability as far as the licenses allow; now
  says that references do not imply endorsement; and, in the robotics profile, now states that it
  adds to the applicable safety standards and the risk assessment and never replaces them (R1.2).
  This matches the practice above.
- **Entity question.** The text names "Vektra Industries" as owner and the "Vektra Foundation" as
  steward. If either is not a registered legal entity, the people acting for it could carry the
  exposure personally, and calling an unformed body a "Foundation" could mislead. This review
  could not check the status of either (residual risk 2).

## 7. Export and regulation (brief)

- Under the U.S. EAR, "published" information and software, made available to the public without
  restrictions on further dissemination, is not subject to the EAR (15 CFR 734.3(b)(3) and
  [734.7](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.7)).
  See also the [Linux Foundation guidance on the EAR and open
  source](https://bestpractices.linuxfoundation.org/regulatory/export/ear-oss.html). The text and
  the validator contain no encryption functions and no controlled technology. While the
  repository is private it is not "published", but nothing in it appears to need a license.
  Recheck if cryptographic code (for example for signed records, 5.4) is added.
- The text names standards and frameworks only as references, and states that conformance is not
  evidence of compliance with any statute, regulation or standard. That fits regulatory regimes
  such as AI-specific rules in the EU, which apply to providers and deployers, not to a voluntary
  text.

## 8. Operators profile and "no legal rights for machines"

- The profile states duties of design and conduct for operators, says that it creates no legal
  rights for machines, and makes no statement about the moral or legal status of any system.
  That is safe: a voluntary private text cannot create legal rights, and saying so prevents a
  misreading. O2.1 (no gratuitous cruelty by design) is framed by its effect on people, which
  keeps it out of disputed questions about machine status.
- Fixed: the duties are now described as voluntary duties under the Laws, not legal duties, so the
  profile does not read as a contract or a statutory duty of care.

## Residual risks, ranked

1. **Name similarity with a registered mark (VECTRA, AI field).** Highest. Do a free USPTO search
   and get a lawyer's view before any public launch; have a fallback name ready. No spend is
   recommended now.
2. **Status of the owner and steward entities.** Confirm that "Vektra Industries" and "Vektra
   Foundation" exist as legal entities, or describe the steward as planned until it is formed.
3. **The word "Verified".** Resolved after this review: the level was renamed "Reviewed" by the
   owner's delegate on 2026-10-04.
4. **Reliance on the robotics profile.** Mitigated by R1.2 and the disclaimer. Real-world harm
   remains the largest possible exposure if someone ignores them; professional safety review is
   recommended when funding allows.
5. **Limits of disclaimers.** Some liability cannot be disclaimed in some places. Keep the text
   modest and accurate.
6. **No per-file license notices.** Licenses are stated per directory. Low risk; add SPDX headers
   to the code files if the project grows.
7. **Export.** Low. Recheck if cryptographic code is added.

## Sources

All accessed 2026-10-04.

- CC BY 4.0 legal code: https://creativecommons.org/licenses/by/4.0/legalcode.en
- Developer Certificate of Origin 1.1: https://developercertificate.org/
- USPTO, Why register your trademark?: https://www.uspto.gov/trademarks/basics/why-register-your-trademark
- USPTO, Summary of 2025 trademark fee changes: https://www.uspto.gov/trademarks/fees-payment-information/summary-2025-trademark-fee-changes
- USPTO, Certification mark applications: https://www.uspto.gov/trademarks/apply/certification-mark-applications
- TMEP 1306.01(a): https://www.bitlaw.com/source/tmep/1306-01-a.html
- 15 U.S.C. § 1111 and § 1125: https://www.law.cornell.edu/uscode/text/15/1111 , https://www.law.cornell.edu/uscode/text/15/1125
- USPTO trademark search: https://tmsearch.uspto.gov/
- VECTRA registration list: https://www.vectra.ai/legal/trademarks
- NIST AI 100-1: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/ and https://github.com/OWASP/ASVS
- IETF Trust Legal Provisions: https://trustee.ietf.org/documents/trust-legal-provisions/tlp-5/
- Linux Foundation trademark usage: https://www.linuxfoundation.org/legal/trademark-usage
- 15 CFR 734.7: https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.7
- Linux Foundation, EAR and open source: https://bestpractices.linuxfoundation.org/regulatory/export/ear-oss.html
