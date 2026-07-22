# Stage grammar — decision record (demo)

A demonstration Lark grammar for the block surface of bellman-ddsl
spec 0.3 (`AI/dev-specs/dolang+/spec_0.3/spec_0.3-dynsym.md`), built
as a sibling of `grammar.lark` — no dynspec file is modified. The
schema underdetermines the concrete layer; every choice the schema
left open is recorded here.

- **Self-contained file.** The expression ladder is duplicated from
  `grammar.lark` rather than imported, following the
  `modfile_grammar.lark` precedent. The eventual merged grammar
  reconciles the two; this branch demonstrates the stage side.
- **Designation.** `@stage: <name>` is dyno's own metadata rule,
  copied verbatim. There is no stage head and no mode switch.
- **Top level.** Only metadata, declarations, and blocks — equations
  live inside blocks (the stage discipline), which also removes the
  one LALR ambiguity between a joint declaration and a parenthesised
  equation at line start.
- **Statement carriers stay raw (S2).** A statement's `:: […]`
  annotation is one raw token (`STMT_META`), exactly as dyno lexes
  his three carriers; the payload is read after parse.
- **Headers are parsed.** `[…]` before `{…}` parses as entries: bare
  tags, `!word` tags, `key=value` pairs, and the signature
  `(…) -> (…)` with typed sides. Interiors may contain `]` (`V[>]`),
  which is what forces the parsed header.
- **Perch marks ride the index.** `V[>]`, `c[<]` parse by a
  variable-shaped rule (`cname "[" ("<"|">") "]"`); dyno's `t`/`~`
  forms are not used by stage files and are omitted here.
- **Payload sub-grammar (S1).** `@in`/`@def`/`@dist` payloads own the
  exotic lexemes: `R+`/`R++` are single names there (`RPLUS`),
  intervals are spelled as four plain-paren alternatives (a closer
  terminal shared with `)` mis-lexes under LALR contextual states),
  finite sets `{…}` never meet block braces, and a law's arguments
  admit nested tuples (the covariance matrix).
- **Operators.** Subscripted heads (`E_{y}`, `argmax_{ς}`) parse as
  `opcall`; bare heads (`evaluate`) parse as calls and are promoted
  by the operator table at term-building (not part of this demo).
- **Newlines in parentheses** are dropped by a post-lexer so the
  multi-line joint law parses as one declaration.
- **`tests/conftest.py`** stubs the compiled `dynare_preprocessor`
  only when it is absent, so the grammar demo runs in pure-Python
  environments; with the real extension installed the stub is inert.
- **Not in this demo:** the discipline checker (spec §5), the
  splitter extension for `@node`/`!word` in statement payloads, the
  lowering to typed AST, and quoted-string tags in headers
  (dynspec tip `312e8ea` newly accepts them in his raw carriers —
  pending finding 6 of the spec's project record).

Verified: the three worked examples of spec 0.3 §2, extracted
verbatim to `examples/stages/*.dynspec`, parse with the structural
counts asserted in `tests/test_stage_grammar.py` (lark 1.3.1, LALR,
contextual lexer).
