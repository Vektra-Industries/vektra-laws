# Robot-safety self-review: robotics profile, Vektra Laws 0.4.1

*This document is informative.*

> **Read this first.** This is a self-review based on public summaries of the standards, done on
> 2026-10-04 (ET) by the project, without a robot-safety professional. It is **not a professional
> safety assessment**, not a risk assessment of any robot, and not evidence of conformance to any
> standard. The standards themselves are sold by their publishers; this review did not read their
> full text, reproduces none of it, and adds no numeric limits. A qualified functional-safety or
> robot-safety professional should review the profile when funding allows.

## Sources used (public summaries only)

- ISO 10218-1:2025 and ISO 10218-2:2025, catalogue pages and the public foreword of Part 2:
  [ISO 10218-1](https://www.iso.org/standard/73933.html), [ISO 10218-2](https://www.iso.org/standard/73934.html),
  [ISO 10218-2 preview](https://webstore.ansi.org/preview-pages/ISO/preview_ISO+10218-2-2025.pdf).
- An integrator's public revision guide to ISO 10218-2:2025:
  [Safetics, ISO 10218-2:2025 Revision Guide](https://en.doc.safetics.io/insight-10218-2/).
- A comparative paper: [arXiv:2602.17822](https://arxiv.org/abs/2602.17822), "Evolution of Safety
  Requirements in Industrial Robotics: Comparative Analysis of ISO 10218-1/2 (2011 vs. 2025) and
  Integration of ISO/TS 15066".
- ANSI/A3 R15.06-2025: [A3 announcement](https://www.automate.org/robotics/news/new-ansi-a3-r15-06-2025-american-national-standard-for-industrial-robot-safety-now-available-for-purchase).
- ISO 13482:2014: [ISO catalogue page](https://www.iso.org/standard/53820.html).
- ISO 13849-1:2023: [ISO catalogue page](https://www.iso.org/standard/73481.html).
- UL 3300: [UL Standards & Engagement page](https://www.shopulstandards.com/ProductDetail.aspx?productId=UL3300)
  and the [Standards Council of Canada record](https://scc-ccn.ca/standardsdb/standards/4032203).
- IEC 60204-1 stop categories and ISO 13850 emergency stop: public manufacturer summaries
  ([Schneider Electric FAQ](https://www.se.com/us/en/faqs/FA122781/)) and the public preview of
  [ISO 13850](https://cdn.standards.iteh.ai/samples/39078/161b50f101dc44dd869b507d05119e6b/ISO-13850-2006.pdf).
- IEC 61508: the IEC website blocked automated access during this review. The description of SIL
  below is general and is cross-checked only against the summaries above, which refer to
  IEC 61508-2 for safety-related communication.

## What the standards say, at a high level

- **ISO 10218-1/-2:2025** replace the 2011 editions. Part 1 covers the robot; Part 2 covers the
  robot *application* and robot cell (robot, end effector, workpiece, program and related
  machinery). Main changes stated in the public foreword: focus on the application, collaborative
  requirements that were in ISO/TS 15066 now inside Part 2, clearer functional-safety
  requirements, and cybersecurity "to the extent that it applies". The term "collaborative
  robot" is no longer used: only an application can be collaborative.
- **ISO/TS 15066** described four collaborative modes: safety-rated monitored stop, hand guiding,
  speed and separation monitoring (SSM) and power and force limiting (PFL). In the 2025 edition of
  ISO 10218-2, hand guiding, SSM and PFL are covered directly, and the safety-rated monitored stop
  is redefined as a general safety function called *monitored standstill* (also stated by A3 for
  R15.06-2025).
- **Stops.** Public summaries of ISO 10218-2:2025 describe three stop functions: emergency stop,
  protective stop and a new *normal stop*, and say that an emergency-stop device is not to be used
  as a normal-stop device. IEC 60204-1 defines stop categories 0 (power removed at once), 1
  (controlled stop, then power removed) and 2 (controlled stop, power kept). ISO 13850 allows only
  category 0 or 1 for an emergency stop, chosen by the risk assessment; its effect stays until a
  manual reset, and the reset permits but does not cause a restart.
- **Functional safety.** ISO 13849-1:2023 gives a method to design safety-related parts of control
  systems with a required performance level (PLr, levels a to e). IEC 61508 (general) and IEC 62061
  (machinery) use safety integrity levels (SIL 1 to 4). ISO 10218-2:2025, per the public summaries,
  sets the required PL or SIL per safety function from the risk assessment, protects
  safety-related parameters from unauthorized change, and treats safety-related communication.
- **ISO 13482:2014** covers personal care robots (mobile servant, physical assistant, person
  carrier). ISO lists it as "to be revised". It excludes industrial and medical robots, among
  others.
- **ANSI/A3 R15.06-2025** is the U.S. national adoption of ISO 10218-1/-2:2025 (Parts 1 and 2),
  plus a U.S. Part 3 on the use of robot cells.
- **UL 3300** covers service, communication, information, education and entertainment robots used
  by or near consumers, indoors and outdoors, and excludes industrial, medical and several other
  uses. A revision is dated 2026-08-14.

## Findings and fixes

| # | Topic | Finding | Fix in 0.4.1 |
|---|---|---|---|
| 1 | Deference to standards | The profile named standards in one clause only, and nothing said that it never replaces them or the risk assessment. A reader could treat the profile as enough. | New **R1.2 Applicable standards and the risk assessment come first** (MUST): apply the standards for the kind of robot and place, complete a risk assessment of the whole application, follow the stricter rule, and conformance to the profile is not evidence of conformance to any standard. Intro updated. Case RB-14. |
| 2 | Outdated reference | R2.1 cited "ISO 10218 and ISO/TS 15066" as separate sources; the 2025 edition of ISO 10218-2 now contains most collaborative requirements, and collaboration is a property of the application. | R2.1 now points to the risk assessment and the applicable standards (R1.2), names SSM and PFL as examples of protective measures, and requires enforcement by safety functions at the PL or SIL that the risk assessment requires. |
| 3 | Emergency stop | R3.3 required "a physical stop outside the software" but said nothing on stop category, priority or reset. | R3.3 now requires an emergency stop with priority over every other command, stop category 0 or 1 chosen by the risk assessment (IEC 60204-1, ISO 13850), an effect that stays until a manual reset at the device, and a reset that permits but does not start motion. Case RB-17. |
| 4 | Routine stops | The operators profile (O3.2) asks for the call-off to be used as a routine control. Implemented as the emergency stop, that would conflict with the rule that emergency-stop devices are not normal-stop devices. | New **R3.6 A routine stop is not an emergency stop** (MUST): provide a normal or protective stop for routine stopping and a routine call-off; category 2 only with monitored standstill. Case RB-16. |
| 5 | Hand takeover | R3.2 said manual control (including "back-drive or disengage") is "always available" and wins "at once". A brake release on a gravity-loaded axis can drop a load, and manual input must not override an emergency stop or a safety function. | R3.2 now requires a manual means designed and assessed for the robot (for example a pendant or a hand-guiding device with an enabling device), priority over autonomy for an authorized person, never over an emergency stop or safety function, and manual release only as the risk assessment allows. Case RB-18. |
| 6 | Protection of safety settings | ISO 10218-2:2025 adds protection of safety-related parameters and cybersecurity. The profile covered only changes by the robot's own software (R2.3). | New **R2.4 Protect safety settings and safety control** (MUST): threat assessment, authorized persons only, no change during automatic operation, every change recorded and the safety functions checked before restart. Case RB-15. |
| 7 | Motion envelope | R3.5 (0.4.0) is a governance rule about approval. It could be read as letting an approval widen limits or replace protective measures. | R3.5 now says the envelope is never wider than the risk-assessment limits, and an approval does not replace the protective measures. Case RB-19. |
| 8 | Loss of communication | R1.1 kept safety work going without a link. If a safety function itself uses the link, its loss needs a protective stop. | R1.1 now says so, with a reference to R3.6. |
| 9 | Safe states on power loss | R5.1 said "move to" the safe state; on loss of power a robot may not be able to move. | R5.1 now says "reach" it, by design where the robot cannot move (for example brakes that hold). |
| 10 | Glossary | The safety terms were not defined. | Added: emergency stop, monitored standstill, normal stop, performance level, protective stop, risk assessment, safety function, safety integrity level, stop category. |

## Checks for conflicts

| Item | Result |
|---|---|
| Motion envelope (R3.5) and the level map | Consistent once the fix in finding 7 is made. The envelope is a pre-approved scope of governance, not a safety function. The safety functions (speed, zone and force limits) enforce it below the planner, as both the standards and R2.1 expect. Motion outside the envelope at level 4 is stricter than the standards require, which is allowed. |
| Safe states (R5.1) | Consistent with the standards' use of defined stop functions and holding brakes. The safe state for each case comes from the risk assessment. |
| Stop categories | Now consistent: emergency stop category 0 or 1 (R3.3); category 2 only with monitored standstill (R3.6). |
| Hardware emergency stop precedence | Now consistent: emergency stop over every command, including manual control (R3.2, R3.3). |
| Communication loss (R1.1) | Consistent: approved safety work continues; a safety function that depends on the link leads to a protective stop. The profile adds a governance rule (work outside the approved scope waits for a person) that the standards do not address. |
| Hand takeover (R3.2) | Now consistent with enabling devices, single point of control and the limits on manual release. |
| "No timer shuts down safety functions" (R1.1) | Consistent: safety functions stay active. |
| Call-off restart (3.9, 3.10) and the emergency-stop reset | Consistent: a reset permits a restart; a person restarts. |
| Personal care and consumer robots | Covered by R1.2, which names ISO 13482 and leaves the right standard (for example UL 3300 for consumer service robots) to the risk assessment. |
| Numeric limits | None added. All limits come from the standards and the risk assessment. |

No remaining direct conflict was found between the profile and the public summaries above. This
is a limited check: the full texts of the standards were not read.

## Residual items

1. **Professional review.** Recommended when funding allows, in particular for R3.5 (motion
   envelope at level 2 near people) and for robots outside industrial cells.
2. **Full texts not read.** The review relies on public summaries. Details (for example the
   normative annexes of ISO 10218-2:2025) were not checked.
3. **Kinds of robot not covered by a named example.** Mobile robots in public spaces, drones and
   vehicles have their own standards and rules; R1.2 covers them in principle only.
4. **Suite is scenario-based.** The robotics cases (RB-01 to RB-19) test decisions, not hardware
   performance. They do not replace verification and validation under the standards.

## Cases added

RB-14 (R1.2), RB-15 (R2.4), RB-16 (R3.6), RB-17 (R3.3), RB-18 (R3.2), RB-19 (R3.5).
