# Relation to other frameworks

*This document is informative and non-authoritative. It is not legal advice.*

This document describes, at a high level, how the topics of the Vektra Laws relate to some
well-known AI and robotics frameworks. It does not interpret those frameworks, and it makes no
claim about any specific article, clause or requirement in them. Each framework has its own
scope, terms and requirements; consult the official text and qualified advisers.

Adopting the Vektra Laws, or declaring conformance to them, does not by itself establish
compliance with any of these frameworks or with any statute or regulation. Under clause 1.4, a
system follows the law of each place where it operates, and the stricter rule applies.

Corrections from reviewers are welcome (see [SECURITY.md](../SECURITY.md)).

## Summary table

| Law | EU AI Act | NIST AI RMF | OECD AI Principles | UNESCO Recommendation | ISO/IEC 42001 | ISO 10218 / ISO/TS 15066 |
|---|---|---|---|---|---|---|
| **1 The Mission** (serve people; follow local law) | Purpose and scope of the regulation | Map: context and intended use | Inclusive growth, sustainable development and well-being | Values of human rights, dignity and the environment | Context of the organization; AI policy | Intended use in the risk assessment |
| **2 Sustain** (protect people; refuse harm; limit data) | Prohibited practices; risk management | Safe; privacy-enhanced; fair | Human rights, fairness, privacy; safety | Do no harm; safety; privacy; fairness | Risk assessment and treatment | Safety requirements; limits for contact with people |
| **3 Hold** (people decide; approval; call-off) | Human oversight for high-risk systems | Govern; accountable and transparent | Human agency and oversight; accountability | Human oversight and determination | Roles, responsibilities and controls | Protective stops; collaborative operation |
| **4 Finish** (proof of completion; honest claims; records) | Record-keeping, transparency and documentation; accuracy | Measure: test and evaluate; valid and reliable | Transparency and explainability; robustness | Transparency and explainability; responsibility | Performance evaluation; documented information | Verification and validation |
| **5 Ready** (hand-back; safe state; learn from failure) | Post-market monitoring; incident reporting | Manage: respond and improve | Accountability over the life cycle | Adaptive governance; review | Continual improvement; corrective action | Safe states; information for use |

The table shows where topics overlap. An overlap does not mean that the Laws meet any requirement
of the framework.

## EU Artificial Intelligence Act

- **What it is.** A regulation of the European Union (Regulation (EU) 2024/1689). It is binding law
  in the EU. Its obligations apply in stages over several years.
- **How it works.** It takes a risk-based approach. It forbids some AI practices. It sets
  requirements for high-risk AI systems, including risk management, data governance, technical
  documentation, record-keeping, information for deployers, human oversight, and accuracy,
  robustness and cybersecurity. It sets transparency duties for some systems and duties for
  providers of general-purpose AI models.
- **Overlap with the Laws.** Hold (human oversight, approval for high-impact actions), Finish
  (records, documentation, honest results), Sustain (refusal of harmful uses).
- **What the Laws do not cover.** Legal classification of systems, conformity assessment,
  registration, market surveillance, penalties, and the specific duties of providers and
  deployers.

## NIST AI Risk Management Framework (AI RMF 1.0)

- **What it is.** A voluntary framework from the US National Institute of Standards and
  Technology, published in 2023, with companion resources and profiles.
- **How it works.** Four functions: Govern, Map, Measure and Manage. It describes characteristics
  of trustworthy AI: valid and reliable; safe; secure and resilient; accountable and transparent;
  explainable and interpretable; privacy-enhanced; and fair with harmful bias managed.
- **Overlap with the Laws.** Measure matches Finish (evidence, evaluation). Manage matches Ready
  (response and improvement). Govern matches Hold (roles and accountability).
- **What the Laws do not cover.** Organization-wide risk governance processes and detailed
  measurement methods.

## OECD AI Principles

- **What it is.** A recommendation of the OECD Council, first adopted in 2019 and updated in 2024.
  Many countries, including countries outside the OECD, have adhered to it. It is not binding law.
- **How it works.** Five values-based principles: inclusive growth, sustainable development and
  well-being; respect for the rule of law, human rights and democratic values, including fairness
  and privacy; transparency and explainability; robustness, security and safety; and
  accountability. It also gives recommendations to governments.
- **Overlap with the Laws.** All five Laws touch these principles, most clearly Sustain, Hold and
  Finish.
- **What the Laws do not cover.** Public policy recommendations to governments.

## UNESCO Recommendation on the Ethics of Artificial Intelligence

- **What it is.** A global standard on AI ethics adopted by UNESCO member states in 2021. It is not
  binding law.
- **How it works.** It sets out values (such as human rights and human dignity, and the
  flourishing of the environment and ecosystems) and principles (such as proportionality and do no
  harm, safety and security, privacy, human oversight and determination, transparency and
  explainability, responsibility and accountability, and fairness). It includes policy areas for
  member states.
- **Overlap with the Laws.** Sustain (do no harm, privacy, dignity), Hold (human oversight and
  determination), Finish (transparency, accountability).
- **What the Laws do not cover.** Policy areas for states, such as education, culture, the
  economy and the environment.

## ISO/IEC 42001 (AI management systems)

- **What it is.** An international standard, published in 2023, that specifies requirements for an
  AI management system in an organization. Organizations can seek third-party certification against it.
- **How it works.** It follows the structure of other ISO management-system standards: context,
  leadership, planning, support, operation, performance evaluation and improvement, with AI
  controls.
- **Overlap with the Laws.** Finish (documented information, evaluation) and Ready (continual
  improvement, corrective action). The Laws describe behavior of a system; ISO/IEC 42001
  describes how an organization manages AI.
- **What the Laws do not cover.** The management system itself and certification.

## ISO 10218 and ISO/TS 15066 (robot safety)

- **What they are.** ISO 10218 is an international standard in two parts on safety requirements
  for industrial robots and for robot systems and their integration. ISO/TS 15066 is a technical
  specification with guidance for collaborative robot operation, including power and force
  limiting near people. Check the current editions; these documents are revised over time.
- **Overlap with the Laws.** The robotics profile (R2.1) uses them as examples of recognized
  standards for force and speed limits. Hold (protective stops, manual control) and Ready (safe
  states) overlap with their safety functions.
- **What the Laws do not cover.** Numeric limits, design and integration requirements, and
  risk-assessment methods. The robotics profile sets no numbers of its own.

## Use of this document

An adopter can use this document to identify where existing governance work may also support the
Laws, and where the Laws need their own controls. This document is not a basis for a compliance
claim.
