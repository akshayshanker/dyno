"""Parser for block-surface stage files (bellman-ddsl spec 0.3 demo).

Builds the Lark parser for ``grammars/stage_grammar.lark`` with a
post-lexer that drops newline tokens inside parentheses, so a
multi-line joint law parses as one declaration.
"""

from os import path
from lark import Lark

_GRAMMAR = path.join(path.dirname(__file__), "grammars", "stage_grammar.lark")


class _NewlineInParens:
    """Drop _NL tokens while inside ( ) so wrapped arguments parse."""

    always_accept = ("_NL",)

    def process(self, stream):
        depth = 0
        for tok in stream:
            if tok.value == "(":
                depth += 1
            elif tok.value == ")":
                depth = max(0, depth - 1)
            if tok.type == "_NL" and depth > 0:
                continue
            yield tok


parser = Lark(
    open(_GRAMMAR, encoding="utf-8").read(),
    parser="lalr",
    propagate_positions=True,
    postlex=_NewlineInParens(),
)


def parse_stage(text: str):
    """Parse block-surface source text; returns the Lark tree."""
    return parser.parse(text)


def parse_stage_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        return parse_stage(f.read())
