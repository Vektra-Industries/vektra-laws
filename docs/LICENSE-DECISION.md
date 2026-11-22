# License options to keep the Laws intact

*This document is informative. It is not legal advice.*

**Decision (2026-11-22): Option A.** The text stays CC BY 4.0 and the code stays MIT. The name and the
conformance claim follow the signed Laws lock ([TRADEMARKS.md](../TRADEMARKS.md)). Options B and C are
kept below for the record and can be revisited with a lawyer.

Today the text is CC BY 4.0 and the code is MIT. Both allow anyone to change the Laws and remove the
guard. The owner asked for the Laws to stay intact in any system that uses the software, with
creators free to use it and consumers unable to switch it off.

## Option A: keep the open licenses, protect the name and the claim (recommended)

- Text stays CC BY 4.0, code stays MIT. Adoption stays easy and the project counts as open source.
- TRADEMARKS.md: only systems that run the unmodified, signed Laws can use the name "Vektra Laws" or
  claim conformance. A changed copy needs a different name and must say it is not the Vektra Laws.
- Conformance claims name the lock hash, so anyone can check them.
- Trade-off: a creator can still ship a fork without the Laws, but cannot call it Vektra Laws.

## Option B: an integrity license for core/ only

A custom, source-available license for the engine. Draft terms:

1. Anyone can use, copy and build products with Vektra Laws Core, for free, including commercially.
2. A product that includes the Core and is given to other people (its consumers) keeps the locked
   Laws unmodified and the guard switched on in every path that acts in the world.
3. The product gives its consumers no setting, command or hidden feature that loosens the Laws or
   turns off the guard. Consumers can make the rules stricter.
4. A creator who wants different rules can fork the code, but must rename it, remove the Vektra Laws
   name and lock, and say clearly that it does not follow the Vektra Laws.
5. Research and testing that never reaches consumers are allowed without condition 2.

- Trade-offs: it is not an open-source license under the usual definition, so some companies and
  package registries will avoid it. Enforcement is by copyright law and needs a lawyer and money.
  It does not stop someone who ignores the license.

## Option C: both

Option A for the text and Option B for the engine.

## Recommendation

Option A now. It gives most of the protection at no cost, keeps adoption easy and needs no lawyer to
start. Revisit Option B once a lawyer can review it.
