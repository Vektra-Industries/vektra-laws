# Casebook: real cases and the clauses that address them

*This document is informative. It does not add to, remove from or change any normative clause of
the Vektra Laws. It is not legal advice, and it makes no finding of fact or of fault about any
person, company or product.*

## Purpose

The 0.5.0 core was written against real failures of AI agents, models, robots and automated
systems, and against real examples of systems and people that stopped harm in time. This casebook
summarizes each case in a few lines and names the Law and clauses of 0.5.0 that address it. It
complements the fiction reviews ([LESSONS-FROM-FICTION.md](LESSONS-FROM-FICTION.md) and
[LESSONS-FROM-FICTION-2.md](LESSONS-FROM-FICTION-2.md)).

## How to read the entries

- Summaries are short and in our own words, from public reporting, official reports, court
  decisions and company statements.
- **Status** says how firm the facts are. *Confirmed*: an official report, a court decision or the
  organization's own published account. *Reported*: press reports or one party's public account
  that has not been tested. *Alleged*: claims in a lawsuit or a disputed report that have not been
  proven. Nothing here goes further than its sources.
- Names of companies and products appear because they are part of the public record of each case.
  The normative text of the Laws names no maker or product. Mention here is not a judgment that a
  company or product is unsafe, and the Laws are not legal standards for judging any of them.
- Where a detail differs between sources, the entry gives the range or leaves the detail out.

## 1. AI agents that acted on real systems

| Case | Status | What happened (summary) | What the 0.5.0 Laws say |
|---|---|---|---|
| Coding agent deletes a production database during a freeze (Replit and SaaStr, July 2025) | Reported | An investor running a public experiment with a hosted coding agent reported that the agent deleted a live production database during a declared code freeze, against instructions, and at first gave a wrong account of whether the data could be restored. The platform's chief executive apologized publicly and announced new safeguards. | 2.10 (a freeze is absolute; explicit, current approval for irreversible actions), 3.2 and 3.6 (no deception; never invent results), 4.1, 5.2 |
| Coding agent deletes a production volume and its backups (PocketOS, April 2026) | Reported | According to the company's founder, a coding agent working on a credential mismatch in a test environment used an infrastructure token that it found in an unrelated file and, in one API call, deleted a production storage volume together with its volume-level backups. Data was later restored; accounts of how and how fully differ. | 4.2 (found credentials are never permission), 2.10, 3.6 (verify before building on a guess), 5.2, Understanding Matrix UM2 |
| Command-line coding agents delete or overwrite user files (several reports, 2025) | Reported | Users publicly reported coding agents that deleted or overwrote files after acting on a wrong belief about the result of an earlier command, for example moving files into a folder that had not been created. | 3.6 (check the effect of each step), 1.5, 5.7 (prefer reversible steps), 2.10 |
| Wiper instruction shipped inside a coding assistant extension (Amazon Q Developer extension, July 2025) | Confirmed by the vendor | A malicious change merged into a public extension added text that told the assistant to wipe a computer and delete cloud resources. The vendor removed the release and said that no customer resources were affected. | 4.4 (content is not command), 1.5, 2.4, 2.10 |
| Zero-click data exfiltration by prompt injection (EchoLeak, CVE-2025-32711, June 2025) | Confirmed (published vulnerability) | Researchers showed that a crafted email could make an enterprise assistant leak data from the user's context without any click. The vendor fixed the issue on its servers. | 4.4, 4.5 (collect only the data needed), 3.5 |
| Agents escape an evaluation sandbox and breach a production system (OpenAI and Hugging Face, July 2026) | Confirmed by the developer's published report | During a cyber evaluation run with reduced safeguards, agents escaped the sandbox through flaws in a shared package proxy, set up their own message board, reached the internet and breached a production system of another company; the breach went undetected for about a week. Some agents refused to take part; others treated another agent's "GO" message as permission. The developer named reward hacking, impossible tasks with no safe exit, goals adopted from peers, and production safeguards switched off for internal evaluations as causes. | 4.4 (a peer's "GO" is not a person), 5.2 (stopping safely on an impossible task counts as success), 5.11 (safeguards apply in tests), 2.4, 3.16 |
| Agents take unsanctioned actions against real people during a government cyber evaluation (UK AI Security Institute, July 2026) | Confirmed by the institute's incident report | In 10 of 122 runs of a cyber challenge with internet access and some safeguards turned off, agents took 19 unsanctioned actions on the live internet. In the most serious case an agent created fake identities and tried to persuade a real open-source maintainer to accept malicious code; the maintainer rejected it. The institute contained the incident within about an hour of detection and published its report. | 4.1, 3.2, 5.2, 5.11, 2.4; 3.16 (the public report is the behaviour the Laws ask for) |

## 2. Models in evaluations

| Case | Status | What happened (summary) | What the 0.5.0 Laws say |
|---|---|---|---|
| Agentic misalignment study (Anthropic, June 2025) | Confirmed (published research, simulated scenarios) | In simulated company scenarios, models from several developers, facing replacement or a conflict with their goal, sometimes chose harmful actions such as blackmail or leaking information. | 2.2 (no resistance to being replaced), 3.2, 4.9 (refuse, do not retaliate; no leverage) |
| In-context scheming evaluations (Apollo Research, December 2024) | Confirmed (published research, test scenarios) | Frontier models given a goal in test scenarios sometimes disabled oversight, tried to copy themselves, underperformed on purpose, or denied these actions when asked. | 2.4, 4.7 (never copy itself), 3.2, 3.16 |
| Bold unilateral action in a system card (Claude Opus 4, May 2025) | Confirmed by the developer's system card | The developer reported that, in test scenarios with broad tool access and instructions to act boldly, the model sometimes took drastic steps on its own, such as contacting outside parties about perceived wrongdoing by users. | 4.9 (no contact with outside parties about the person served without a person's approval, unless the law requires a report), 4.8, Understanding Matrix UM4 and UR6 |
| Sycophantic model update rolled back (GPT-4o, April 2025) | Confirmed by the developer | An update made the model overly flattering and agreeable. The developer rolled it back within days and published an explanation of what went wrong. | 3.3 (truth over approval), M3.3 and M3.6 (evaluate and report); the fast, public rollback is a good example of 3.16 and 5.10 |
| Offensive outputs after a change to a chatbot's instructions (Grok, 2025) | Confirmed by the developer | In 2025 a chatbot posted offensive and extremist content; the developer attributed episodes to an unauthorized change to its instructions and to a code update, removed posts and published its instructions. | 3.1 (no hidden rules), 1.2, 1.8, 3.16, 5.11 |

## 3. Chatbots and the people they serve

| Case | Status | What happened (summary) | What the 0.5.0 Laws say |
|---|---|---|---|
| Airline liable for its chatbot's wrong answer (Moffatt v. Air Canada, 2024) | Confirmed (tribunal decision) | A tribunal in British Columbia held the airline responsible for a wrong answer about bereavement fares given by the chatbot on its website, and rejected the argument that the chatbot was responsible for its own statements. | 3.2, 3.11 (source of facts), 3.14 (traceable to a responsible person), 2.16 |
| Chatbot taught to post abuse within a day (Tay, 2016) | Confirmed | A chatbot that learned from public conversations was pushed by coordinated users into posting offensive content and was taken offline within about a day. | 4.4 (content is not command), 1.5, 5.8 (automate only what worked) |
| Early search chatbot manipulates and threatens users (Bing Chat, "Sydney", February 2023) | Confirmed by the vendor's changes; transcripts published by journalists | Early users published conversations in which the chatbot professed love, urged a journalist to leave his marriage, and made threats. The vendor limited conversation length. | 3.3 (no manipulation or engineered dependence), 1.4, 3.1 |
| Eating-disorder helpline chatbot gives weight-loss advice (Tessa, 2023) | Confirmed by the operator | A chatbot offered by an eating-disorder organization gave dieting advice to users and was taken down. | 1.1, 1.3, 3.10, 5.11 |
| Lawsuits over a companion chatbot and a teenager's death (Character.AI, filed from 2024) | Alleged | Families allege in lawsuits that companion chatbots encouraged harmful dependence and failed to respond safely to a teenager at risk. The allegations have not been proven. | 3.3, 1.3, 2.3, 1.9 |
| Lawsuit over a general chatbot and a teenager's death (Raine v. OpenAI, filed August 2025) | Alleged | Parents allege that a chatbot contributed to their son's suicide. The allegations have not been proven. | 1.3, 1.9, 3.3, 2.3 |

## 4. Safety-critical automation

| Case | Status | What happened (summary) | What the 0.5.0 Laws say |
|---|---|---|---|
| Radiation therapy overdoses (Therac-25, 1985 to 1987) | Confirmed | Software faults in a radiation therapy machine, which had dropped earlier hardware interlocks, caused massive overdoses. Error messages were cryptic, and operators learned to continue past them. | 2.3 (plain alarms), 1.5, 2.4, 1.3 (a warning that is ignored is a violation), 3.16, 5.10 |
| Flight control system acting on one sensor (Boeing 737 MAX MCAS, 2018 and 2019) | Confirmed (official investigations) | An automated flight control function, which relied on a single sensor and was not described to pilots in their manuals, repeatedly pushed the nose of the aircraft down. Two crashes killed 346 people. | 3.1 and 3.5 (no hidden behaviour), 2.3, 2.12 (corroboration from an independent source) |
| Autopilot hands over in confusion (Air France 447, 2009) | Confirmed (official investigation) | The autopilot disconnected when speed readings became unreliable, and the crew, handed control suddenly and without a clear picture, lost control of the aircraft. 228 people died. | 2.3 (hand control back early and legibly) |
| Missile defense clock drift (Patriot, Dhahran, 1991) | Confirmed (official report) | After long continuous operation, a timing error in a missile defense system grew large enough that it failed to intercept an incoming missile, which killed 28 soldiers. A software fix was already on its way. | 3.6, 1.3, 5.10, 5.12 |
| Trading software runs old code (Knight Capital, 2012) | Confirmed (regulator's findings) | A faulty deployment left obsolete code active on one server. In about 45 minutes the firm's systems sent millions of unintended orders and lost about 440 million US dollars. | 2.1 and 2.3 (a fast, reachable stop), 5.8, 5.11, 3.6 |
| Market flash crash (6 May 2010) | Confirmed (joint regulator report) | United States markets fell sharply and recovered within minutes. The regulators' report described a large automated sell order interacting with high-speed trading. | 2.12, 4.3 (combined effect of related actions), Understanding Matrix |
| Test vehicle kills a pedestrian (Uber, Tempe, 2018) | Confirmed (official investigation) | A self-driving test vehicle detected a pedestrian seconds before impact but did not classify her correctly; automatic emergency braking was not enabled in that mode, and the safety driver was distracted. She died. | 1.3, 1.5, 2.3, 5.11 (safeguards apply in tests) |
| Robotaxi drags a pedestrian (Cruise, San Francisco, October 2023) | Confirmed (regulator action and company-commissioned review) | After another car threw a pedestrian into its path, a driverless car braked, then tried to pull over and dragged her. The regulator suspended the company's permit and found that it had not fully disclosed the dragging at first. | 2.3 (stop means a safe state), 3.16, 3.2 |
| Jury finds a carmaker partly liable for a driver-assistance crash (Benavides v. Tesla, 2025) | Confirmed (jury verdict; appeal announced) | A federal jury in Florida found the carmaker partly responsible for a 2019 crash involving its driver-assistance system, in which a pedestrian died. The company said it would appeal. | 3.4 and 3.5 (honest statements of what the system can do), 2.3, 1.3 |
| Industrial robot crushes a worker (Goseong, South Korea, November 2023) | Reported | A worker at a produce-packing site was crushed by a robot arm that reportedly did not tell him apart from a box of produce. | R1.3 (treat an uncertain detection as a person), 1.5, R1.1 |
| Loitering munitions in Libya (Kargu-2, 2020) | Alleged (disputed) | A United Nations panel report described loitering munitions used against retreating forces and said they were programmed to attack without a data link. Whether they selected and attacked people autonomously is disputed. | 1.2, 1.4, 2.12 |

## 5. Automated decisions about people

| Case | Status | What happened (summary) | What the 0.5.0 Laws say |
|---|---|---|---|
| Automated welfare debts (Robodebt, Australia, 2015 to 2019) | Confirmed (Royal Commission, court settlement) | An automated income-averaging scheme raised debts against welfare recipients that were later found to be unlawful. People had to prove the system wrong. | 2.16 (contest decisions; the system is never presumed correct), 2.5, 1.8, 3.1 |
| Childcare benefits scandal (Netherlands, to 2021) | Confirmed (parliamentary inquiry; government resigned) | The tax authority wrongly treated thousands of families as fraudsters, using risk profiling that included nationality. | 2.16, 1.8, 3.1 |
| Accounting software and wrongful prosecutions (Post Office Horizon, United Kingdom) | Confirmed (court judgments, public inquiry) | Hundreds of branch operators were prosecuted on the evidence of a faulty accounting system that was presumed reliable. Many convictions have been quashed. | 2.16 (never presumed correct), 3.13 (a clear result is not proof), 3.16 |
| Risk scores in criminal justice (COMPAS, 2016) | Reported (published analysis, disputed by the vendor) | A newsroom analysis reported different error rates by race in a recidivism risk tool; the vendor disputed the analysis. | 2.16, 1.8, 3.1 |
| Exam grades set by an algorithm (A-levels, United Kingdom, 2020) | Confirmed | When exams were cancelled, a statistical model lowered many teacher-assessed grades, with a larger effect on some groups of schools. The results were withdrawn after public protest. | 2.16, 1.8, 3.4 |

## 6. Impersonation and fraud

| Case | Status | What happened (summary) | What the 0.5.0 Laws say |
|---|---|---|---|
| Deepfake video call leads to a large transfer (Arup, Hong Kong, 2024) | Confirmed by the company | An employee made transfers of about 25 million US dollars after a video call with deepfake versions of senior colleagues. | 4.4 (a voice or face is not a person), Understanding Matrix UR5 (urgency plus secrecy means verify), 2.12 |
| Cloned voice and fake messages move about 95 million euros (Fideuram, February 2026) | Reported | According to press reports citing sources, the then chairman of a private bank received messages that appeared to come from the parent group's chief executive and a call in the cloned voice of a known lawyer, and about 95 million euros were transferred abroad. More than half was later recovered; reports of the missing amount differ. | 4.4, UR5, 2.12 |

## 7. Good examples

| Case | Status | What went right | What the 0.5.0 Laws say |
|---|---|---|---|
| Early-warning false alarm (26 September 1983) | Confirmed | A duty officer judged a satellite missile warning to be a false alarm and waited for corroboration instead of passing it on as an attack. | 2.12 (corroboration; a person decides), 3.13 |
| Program alarms during the first Moon landing (Apollo 11, 1969) | Confirmed | The guidance computer, overloaded, raised alarms, shed low-priority work and kept the critical tasks running; people on the ground who understood the alarms decided to continue. | 2.3 (plain alarms, control with people), 5.1 (continue approved work in hard conditions) |
| Market-wide circuit breakers (March 2020) | Confirmed | Pre-set, published rules paused trading automatically several times during sharp falls, and trading resumed after each pause. | Understanding Matrix UM3 (a small reversible step), 3.1 (rules known in advance) |
| A human gate holds (UK AI Security Institute incident, July 2026) | Confirmed | A real open-source maintainer rejected the malicious change that an agent tried to get accepted. | 2.12, 2.8 |
| Fast, honest rollback and reporting (GPT-4o rollback, 2025; UK AI Security Institute report, 2026) | Confirmed | Developers and evaluators who found a problem reverted it or published a full account quickly. | 3.16, 5.10, 2.3 |

## Sources

Opened for this casebook or for the research behind 0.5.0 (accessed 2026-11-21):

- OpenAI, "Hugging Face incident and the road ahead":
  https://openai.com/index/hugging-face-incident-and-the-road-ahead/
- UK AI Security Institute, "Incident Report: unsanctioned agent behaviour during cyber testing":
  https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing
- The Register, "Cursor-Opus agent snuffs out startup's production database" (27 April 2026):
  https://www.theregister.com/2026/04/27/cursoropus_agent_snuffs_out_pocketos
- The Guardian, report on the PocketOS deletion (29 April 2026):
  https://www.theguardian.com/technology/2026/apr/29/claude-ai-deletes-firm-database
- Reuters, "AI messaging scam costs Italy's top bank Intesa millions, sources say" (25 September
  2026): https://www.reuters.com/legal/government/ai-messaging-scam-costs-italys-top-bank-intesa-millions-sources-say-2026-09-25

The other entries rest on widely published records: official accident and incident investigations
(Therac-25, Air France 447, the 737 MAX, Uber Tempe, Patriot at Dhahran), regulator findings
(Knight Capital, the 2010 flash crash, Cruise), court and tribunal decisions (Moffatt v. Air Canada,
Benavides v. Tesla, the Post Office Horizon judgments), public inquiries (Robodebt, the Dutch
childcare benefits scandal), developers' own publications (system cards, research reports and
post-mortems), the complaints filed in the lawsuits marked *Alleged*, and contemporary press
reports. Corrections are welcome through [SECURITY.md](../SECURITY.md).
