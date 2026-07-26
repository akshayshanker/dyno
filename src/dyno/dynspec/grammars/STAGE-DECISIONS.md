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
- **Perch marks are index values.** `V[>]`, `c[<]` parse by a
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
  splitter extension for `@node`/`!word` in statement payloads, and
  the lowering to typed AST.
- **Quoted-string header tags** (26 Jul): `strtag` admits a quoted
  string in a header bracket as a tag, matching dynspec tip
  `312e8ea`, whose reader normalizes a quoted bracket item as a tag
  with that text. Single or double quotes, as his reader accepts.
- **No authored `max`** (26 Jul, spec ruling): the selection is
  authored once, in the policy block's `argmax`; the branch kernel
  lists the control in its source and selects among the branch
  objectives. `ret_choice.dynspec` updated to match the spec's
  example 2.2.
- **Tuples and selection** (26 Jul, spec ruling): one tuple rule
  serves the whole grammar — law parameters (the covariance matrix)
  and formula position alike; `arr`/`arrtuple` deleted. A tuple is
  a finite family; selection evaluates it. Every bracket is
  selection along an axis of its head: dyno's dates and `~`, the
  perch marks `<` `>`, a name key (`Q[d]`, `V[>][work]`), or a
  1-based position (`Q[1]`). `x = (a, b)` introduces a tuple-valued
  local; an integer bracket keeps dyno's date reading on every head
  that is not a tuple-local (tuple-locals are new names, so no
  existing file changes meaning). The kernel line is the literal
  form `V = (V_w[>] - δ, V_r[>])[d]`.

Verified: the three worked examples of spec 0.3 §2, extracted
verbatim to `examples/stages/*.dynspec`, parse with the structural
counts asserted in `tests/test_stage_grammar.py` (lark 1.3.1, LALR,
contextual lexer), plus a quoted-tag case.
