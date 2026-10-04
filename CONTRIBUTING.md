# Contributing to Vektra Laws

Vektra Laws are owned by Vektra (Vektra Industries). Collaboration is welcome. Issues and pull
requests are open to everyone; Vektra makes the final call on what goes in.

## What helps most

- **A failing case.** Something a real system did that the Laws should have caught, or a clause
  that blocked something it shouldn't. Write it as a case in `tests/` (format in
  [tests/README.md](tests/README.md)).
- **Review of a profile**, especially robotics and models, from people who build those systems.
- **Clearer wording.** Plain words, short sentences.
- **A new profile** for another kind of system.

## Rules

1. **Edit `laws.yaml`, not the generated files.** Then run `python tools/build_docs.py` to rebuild
   LAWS.md and `profiles/`.
2. **Run `python tools/validate.py`** before opening a pull request. CI runs it too.
3. **The five Laws and their order** change only with the owner's sign-off.
4. **Profiles add, never loosen.** A profile clause sits under one of the five Laws and can be
   stricter than the core, never looser.
5. **Clause ids are stable.** Don't renumber published clauses or reuse an id for a new meaning.
6. **No made-up numbers.** Any figure, limit or claim needs a source.
7. **Voice.** Lead with the verb, keep it calm and plain, write it like a crew member's promise.
   No combat language, no sermon.

## Adapting the Laws

The text is CC BY 4.0, so you may adapt it with attribution. If you publish a changed version,
please give it a different name so people can tell it apart from Vektra Laws, and say what you
changed.

## License of contributions

By contributing, you agree your text contributions are licensed under CC BY 4.0 and your code
contributions under MIT, the same as the rest of the repository.
