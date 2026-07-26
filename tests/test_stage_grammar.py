"""The three worked examples of bellman-ddsl spec 0.3 parse as
block-surface stage files (demo grammar; see STAGE-DECISIONS.md)."""

import glob
import os

import pytest

from dyno.dynspec.stage import parse_stage_file

STAGES = sorted(
    glob.glob(os.path.join(os.path.dirname(__file__), "..", "examples", "stages", "*.dynspec"))
)


@pytest.mark.parametrize("path", STAGES, ids=[os.path.basename(p) for p in STAGES])
def test_stage_parses(path):
    tree = parse_stage_file(path)
    blocks = list(tree.find_data("block"))
    sigs = list(tree.find_data("signature"))
    assert blocks, "no operator blocks parsed"
    assert sigs, "no signatures parsed"


def test_structure_counts():
    trees = {os.path.basename(p): parse_stage_file(p) for p in STAGES}
    ret = trees["ret_choice.dynspec"]
    # branching parent holds two nested arm blocks
    assert len(list(ret.find_data("block"))) == 7  # 5 top + 2 arms
    port = trees["port.dynspec"]
    # the joint law's covariance matrix parses as nested tuples
    assert list(port.find_data("tuple"))
    ret = trees["ret_choice.dynspec"]
    # the kernel selects from a literal tuple of branch objectives
    assert list(ret.find_data("tupidx"))
    cons = trees["cons_savings_iid.dynspec"]
    # operators with subscripts (E_{y}) and plain calls (evaluate) both parse
    assert list(cons.find_data("opcall"))


def test_tuple_locals_and_selection(tmp_path):
    # x = (a, b) introduces a tuple-valued local; every bracket is
    # selection: Q[1] a position, Q[d] a key, V[>][work] iterated
    src = (
        "@stage: t\n"
        "delta @in R+\n"
        "[!G_dc, (V_w[>] @in R, V_r[>] @in R, d) @cntn -> (V @in R) @dcsn] {\n"
        "    Q = (V_w[>] - delta, V_r[>])\n"
        "    y = Q[1]\n"
        "    z = Q[d]\n"
        "    V = (V_w[>] - delta, V_r[>])[d]\n"
        "    w = V[>][work]\n"
        "}\n"
    )
    p = tmp_path / "tuples.dynspec"
    p.write_text(src, encoding="utf-8")
    tree = parse_stage_file(str(p))
    assert len(list(tree.find_data("tuple"))) == 2
    assert len(list(tree.find_data("tupidx"))) == 1


def test_quoted_string_header_tag(tmp_path):
    # a quoted string in a header bracket is a tag (dyno tip 312e8ea)
    src = (
        "@stage: demo\n"
        "beta @in (0,1)\n"
        '[!g_ad, "identity edge", (a @in R+) @arvl -> (b @in R+) @dcsn] {\n'
        "    b = a\n"
        "}\n"
    )
    p = tmp_path / "quoted_tag.dynspec"
    p.write_text(src, encoding="utf-8")
    tree = parse_stage_file(str(p))
    tags = list(tree.find_data("strtag"))
    assert len(tags) == 1
