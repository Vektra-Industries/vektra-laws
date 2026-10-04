# Open questions

Choices that need Pablo (or a reviewer) before they're settled. Each one says what this draft
did in the meantime.

## For v0.1 (before going public)

1. ~~**Ethos word.**~~ **Resolved 2026-10-04:** Pablo confirmed the ethos word is *Sustain*,
   not Carry. README and laws.yaml now say Sustain. Wording that uses "carry" as a verb (such as
   the tagline) stays.
2. **Action level definitions.** This draft uses the levels from the brief: 0 READ, 1 PREPARE,
   2 REVERSIBLE WRITE, 3 EXTERNAL ACTION, 4 MONEY OR IRREVERSIBLE. Ada proposed a different cut
   (1 = reversible change in its own workspace, 2 = reversible change others can see, 3 = hard to
   reverse or affects people, money or the physical world, 4 = irreversible or a safety risk).
   Her rules were kept (levels declared before shipping, undeclared counts as 4, approvals come
   through a channel the system can't write to); her definitions were not. Keep the brief's
   levels, or switch?
3. **How quiet is the call-off?** It is clause 3.9 inside Hold, titled with the approved line
   "People can always call it off," and the precedence note names it once. There is no headline,
   box or section for it. Is naming it in the precedence note acceptable, or should that note
   only name the approval line?
4. **Record signing.** 5.4 says the action record SHOULD be keyed or signed. Ada asked for it to
   be required. vektra-reflex's ledger isn't keyed yet, so MUST would make Vektra's own tool
   non-conforming today. Keep SHOULD for v0.1 and raise it to MUST by v1.0?
5. **The name.** CC BY 4.0 lets anyone adapt the text. It doesn't stop someone calling a changed
   version "Vektra Laws." CONTRIBUTING asks adapters to use a different name; real protection
   would need a trademark policy. Do you want one?
6. **Sol's "One thing at a time" (2.5)** is a SHOULD, because some users want the full plan.
   Raise it to MUST for people in distress?
7. **Repo tagline.** Rei's pick is used: "Laws for machines that carry the mission: on Earth and
   beyond." Rei's two other options are in her notes.

## For v0.2 (robotics)

8. **Level 3 in shared space.** Any actuator moving in a space shared with people is level 3,
   which needs a person's approval of that action. That fits Ada's note, but a robot working
   among people would need approval for nearly every motion. Options: a signed per-mission
   envelope that names specific motions, or a stricter level 2 for low-force motion inside
   tested limits. Needs a robotics reviewer.
9. **Standards.** R2.1 points to ISO 10218 and ISO/TS 15066 as examples and sets no numbers. A
   reviewer should confirm the references and say which other standards (mobile robots, drones,
   medical) a profile should name.
10. **Responder sign-off.** R3.4 and 3.2 allow a named responder's sign-off when a person can't
    consent. Whose protocol counts, and how is it recorded on a robot with no network?

## For v0.3 (models)

11. **Who the models profile binds.** Its subject is "the model's makers". Should it also bind
    people who fine-tune or deploy someone else's model?
12. **How much data disclosure.** M2.2 asks makers to document data sources "at the level of
    detail they can disclose." Is that strong enough?
13. **Who may claim conformance.** Self-assessment, review by Vektra, or both? Is there a mark or
    badge, and who grants it?

## Housekeeping

14. The internal foundation files (Charter §2.1, CORE.md) still describe the older laws, and the
    internal enforcement config in VEKTRA-LAWS.md uses its own check names, not these clause ids.
    They should be brought in line once this text is sealed.
