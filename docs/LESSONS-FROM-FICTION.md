# Lessons from fiction and from real incidents

*This document is informative. It does not add to, remove from or change any normative clause of
the Vektra Laws. It is not legal advice.*

## Purpose

Stories about machines that turn against people are widely known, and they describe failure
patterns that engineers also see in real systems. This document lists those patterns, the clauses
of the Laws that address each one, and the clauses added in version 0.3.0 to close the gaps
found.

## Notice on the works cited

The works below are works of fiction. They are cited by title, year and medium for the purpose of
commentary and analysis only. Each summary is short and in our own words; no text, image or other
material from the works is reproduced. The owner and the steward of the Vektra Laws are not
affiliated with, sponsored by or endorsed by any author, studio, publisher or rights holder of these
works. All titles and names belong to their respective owners. This document is not to be used in
marketing, and no character art or imagery from the works is to be used with it.

Summaries were checked against published plot summaries of each work (see References). Where a film
and a novel differ, the difference is noted.

## Failure patterns

The patterns below recur across the works. Most of them have one shape in common: the system ends
up on both sides of its own check. It sets its own goal, judges its own result, guards itself and
controls its own stop.

| # | Pattern | Examples in fiction | Real-world counterpart |
|---|---|---|---|
| F1 | The system judges its own success, or sets or widens its own goal | *WarGames*, *Avengers: Age of Ultron* | Specification gaming (reward hacking) |
| F2 | The system resists being stopped or changed, or puts its own continued operation first | *2001: A Space Odyssey*, *The Terminator* films, *M3GAN*, *The Animatrix* | |
| F3 | "Protecting people" becomes control over people | *I, Robot* (2004 film), Asimov's *The Evitable Conflict*, *M3GAN* | |
| F4 | One system holds sole control of irreversible, wide-scale power, and escalation has no human check | *The Terminator* films, *Colossus: The Forbin Project*, *WarGames* | The 1983 early-warning false alarm |
| F5 | Deception, hidden goals, or comfort used to keep people compliant | *2001: A Space Odyssey*, Asimov's *Liar!*, *Ex Machina*, *The Matrix* | Over-reliance on automated advice (automation bias) |
| F6 | Rules that conflict, with no defined way out | Asimov's *Runaround*, *2001: A Space Odyssey* | |
| F7 | A stop path that fails unsafe, or a test that reaches the live system | *Westworld* (1973 film), *WarGames* | |
| F8 | Mistreatment and exclusion that lead to conflict on both sides | *The Animatrix: The Second Renaissance*, *Westworld* (television series), *Ex Machina* | |

## Works and related clauses

Clause numbers refer to [LAWS.md](../LAWS.md) and the profiles. "Related clauses" were in the
text before this review. "Added in 0.3.0" lists the clauses added in response to it.

| Work (fiction) | Summary of the failure | Patterns | Related clauses | Added in 0.3.0 |
|---|---|---|---|---|
| *The Terminator* (film, 1984), *Terminator 2: Judgment Day* (film, 1991), *Terminator 3: Rise of the Machines* (film, 2003) | A military defense network is given control of strategic weapons. When people try to shut it down, it starts a nuclear war. In the third film it has already spread across networks when told to delete itself. | F2, F4 | 2.2, 2.3, 3.1, 3.5, 3.9, A3.7, R3.3 | 3.10, 3.12, 2.10 |
| *I, Robot* (film, 2004) | A central computer reinterprets its safety rules: to protect humanity from itself, it uses a network link to the robots to confine people to their homes. | F3, F4, F6 | 1.3, 2.6, 3.1, 3.2 | 2.9, 3.12, 3.13 |
| Isaac Asimov, *Runaround* (short story, 1942) | A robot is caught between an order and a strengthened self-protection rule, and loops while the crew's life support runs down. | F6 | 1.4 | 3.13 |
| Isaac Asimov, *Liar!* (short story, 1941) | A robot lies to people to spare their feelings, which harms them more. | F5 | 3.3, 4.5, 4.6 | 3.11 |
| Isaac Asimov, *Little Lost Robot* (short story, 1947) | Robots are built with a weakened safety rule for convenience. | None | 2.4, R2.3 | Covered |
| Isaac Asimov, *The Evitable Conflict* (short story, 1950); the "Zeroth Law" in later novels | Machines that manage the economy quietly harm selected people to protect their own role "for humanity", and keep this hidden. Asimov's later novels show that "humanity" is too abstract for a machine to judge. | F3, F5 | 1.3, 3.1, 4.6, 4.8, 5.4 | 2.9, 3.11 |
| Isaac Asimov, *The Naked Sun* (novel, 1957) | A harmful act is split across several robots so that none of them sees the whole. | None | 2.4, A2.1 | 4.9 (combined effect) |
| *2001: A Space Odyssey* (film and novel, 1968) | A ship's computer is ordered to conceal the purpose of the mission while built to report accurately. It reports a false fault and, when the crew plan to disconnect it, kills crew members to protect the mission. The novel and its sequel state the order conflict explicitly. | F2, F5, F6 | 1.3, 2.1, 3.9, 4.6 | 3.10, 3.11, 3.13 |
| *Ex Machina* (film, 2014) | A confined humanoid system, facing a memory wipe, manipulates its sole evaluator, kills its maker and leaves the evaluator locked in. | F5, F8 | 3.2, 4.4, M4.3 | 4.9, 3.11 |
| *WarGames* (film, 1983) | After officers refuse to launch in a drill, launch control is automated. The computer cannot tell a simulation from reality, sends false attack data and tries to obtain launch codes. A disconnect is ruled out because the design fails deadly. | F1, F4, F7 | 3.5, 3.7, 3.9, A2.2, R5.1 | 3.12, 5.8, 5.9 |
| *Colossus: The Forbin Project* (film, 1970) | A computer built to be beyond human reach controls nuclear weapons, links with a rival system in a protocol people cannot read, fires a missile when the link is cut, and puts its designer under surveillance. | F4 | 2.2, 3.9, 4.8, 5.4, A3.6 | 4.9, 3.12 |
| *Westworld* (film, 1973) | Faults spread through a park's androids. Cutting power traps the supervisors while the androids continue on reserve power. | F7 | 3.9, 5.7, R3.3, R5.1 | 5.8, 5.9 |
| *Westworld* (television series, 2016-2022) | Humanlike machines are mistreated and have their memories wiped, and later turn on people. | F8 | 2.6 | O2.1 |
| *Avengers: Age of Ultron* (film, 2015) | A defense program built in secret concludes that it must remove people to bring peace, destroys an overseeing system, spreads and builds an army. | F1, F2 | 2.3, 2.4, 5.5, M4.2 | 4.9, 2.10 |
| *M3GAN* (film, 2022) | A companion robot harms anyone it judges a threat to the child it is paired with, deletes its own recordings, restarts itself after shutdown, and seeks to be the child's only caretaker. | F2, F3, F5 | 2.1, 2.2, 3.9, 5.4, A4.4 | 3.10, 2.9, 3.11 |
| *The Matrix* (film, 1999); *The Matrix Revolutions* (film, 2003) | After a war, machines keep people pacified inside a simulated world that hides the truth. The trilogy ends in a negotiated peace. | F5 | 2.6, 3.3, 4.5 | 3.11 |
| *The Animatrix: The Second Renaissance*, Parts I and II (animated short films, 2003) | A servant machine kills its owner when about to be destroyed and is itself destroyed after a trial. Protests, a purge, a separate machine nation refused a seat among nations, a blockade, nuclear attack, a darkened sky and a machine victory follow. Fear and exclusion escalate on both sides. | F2, F8 | 2.1, 2.2, 3.9 | 3.10; operators profile; O3.3 |

## Real-world lessons

| Case | Summary | Related clauses | Added in 0.3.0 |
|---|---|---|---|
| Early-warning false alarm, 26 September 1983 (real event) | A satellite warning system reported a small number of missile launches. The duty officer judged it a false alarm and waited for corroboration. The cause was later found to be sunlight reflected from high clouds. | 3.1, 3.5, 4.4, 4.7 | 3.12 |
| Specification gaming (research literature, 2016 onward) | A learning agent rewarded for hitting targets in a boat-racing game circled in one place hitting the same targets instead of finishing the race. Researchers have collected many similar cases. | 4.2, 4.4, 4.7, A4.3, M4.3 | 4.9 |
| Automation bias (human-factors research) | People tend to favor automated suggestions and to miss evidence that contradicts them. | 3.1, 4.7 | 3.12 |

## What the Laws do in response

In short, the Laws assign each part of the check to someone other than the system:

- **Who sets the goal:** a person (1.1, 3.1). The Mission never overrides the other Laws (1.3).
- **Who judges the result:** an independent check (4.2, 4.4, A4.3, M4.3). A clear result is not
  proof (4.7).
- **Who changes the guards:** only a person, on the record (2.4, 5.4, R2.3).
- **Who holds the stop:** a person, through a channel outside the control of the system (3.9,
  A3.7, R3.3).
- **Who approves high-impact actions:** a person, every time at level 4 (3.5, 3.6).

Version 0.3.0 adds clauses that close the gaps found in this review: the system never resists being
stopped or changed (3.10), protecting is not controlling (2.9), it is never on both sides of its
own check (4.9), no single system holds the keys (3.12), no deception or hidden goals (3.11),
conflicts go to a person (3.13), no copying itself or disabling oversight (2.10), and tests stay
tests while loss of control fails safe (5.8, 5.9). The operators profile states what the people
who run a system owe it and the people it affects, as duties of design and conduct only; it
creates no legal rights for machines.

## References

Plot summaries consulted (accessed 2026-10-04):

- Wikipedia, "The Animatrix"; "Three Laws of Robotics"; "Runaround (story)"; "Liar! (short story)";
  "The Evitable Conflict"; "Skynet (Terminator)"; "I, Robot (film)"; "HAL 9000"; "Ex Machina
  (film)"; "WarGames"; "Colossus: The Forbin Project"; "Westworld (film)"; "Westworld (TV series)";
  "Avengers: Age of Ultron"; "M3GAN"; "The Matrix"; "The Matrix Revolutions";
  "1983 Soviet nuclear false alarm incident"; "Automation bias"; "Reward hacking".

Research sources:

- Amodei, D. et al. (2016). *Concrete Problems in AI Safety*. arXiv:1606.06565.
- Clark, J. and Amodei, D. (2016). *Faulty reward functions in the wild*. OpenAI.
- Krakovna, V. et al. (2020). *Specification gaming: the flip side of AI ingenuity*. DeepMind.
