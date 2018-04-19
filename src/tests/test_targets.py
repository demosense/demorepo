import pytest
import copy

import demorepo.config
from demorepo.commands.targets import get_targets
from . import raises

"""
    The Following tests cover the functions:
        - get_targets
        - _order_targets
        - _add_dependencies
"""


@pytest.mark.parametrize("projects, dependencies, targets, reverse_targets, expected, exception", [
    # No filter no deps
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=[], target_B=[], target_C=[]),
        "target_A target_B target_C",
        False,
        ["target_A", "target_B", "target_C"],
        None
    ),
    # Filter
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=[], target_B=[], target_C=[]),
        "target_A target_C",
        False,
        ["target_A", "target_C"],
        None
    ),
    # Filter empty
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=[], target_B=[], target_C=[]),
        "",
        False,
        [],
        None
    ),
    # Filter invalid target
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=[], target_B=[], target_C=[]),
        "target_A target_D",
        False,
        None,
        Exception
    ),
    # No filter with deps
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=["target_B"], target_B=[], target_C=["target_A"]),
        "target_A target_B target_C",
        False,
        ["target_B", "target_A", "target_C"],
        None
    ),
    # Filter and deps
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=["target_B"], target_B=[], target_C=["target_A"]),
        "target_A target_C",
        False,
        ["target_A", "target_C"],
        None
    ),
    # No filter, reverse deps
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=["target_B"], target_B=[], target_C=["target_A"]),
        "target_A target_B target_C",
        True,
        ["target_C", "target_A", "target_B"],
        None
    ),
    # Filter, reverse deps
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=["target_B"], target_B=[], target_C=["target_A"]),
        "target_B target_C",
        True,
        ["target_C", "target_B"],
        None
    ),
    # Cycle
    (
        ["target_A", "target_B", "target_C"],
        dict(target_A=["target_B"], target_B=[
             "target_A"], target_C=["target_A"]),
        "target_A target_B target_C",
        False,
        None,
        Exception
    ),
])
def test_get_targets_plain(projects, dependencies, targets, reverse_targets, expected, exception):
    with raises(exception):
        result = get_targets(projects, dependencies, targets, reverse_targets)
        assert result == expected
