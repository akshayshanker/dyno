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
    assert list(port.find_data("arrtuple"))
    cons = trees["cons_savings_iid.dynspec"]
    # operators with subscripts (E_{y}) and plain calls (evaluate) both parse
    assert list(cons.find_data("opcall"))
