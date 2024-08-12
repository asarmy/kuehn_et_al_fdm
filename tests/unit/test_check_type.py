""" """

import pytest


from kuehn_et_al_fdm.utilities import _check_type


def test__check_type_passing():
    # Test cases that should not raise an error
    try:
        _check_type(5, "parameter", (int, float))
    except TypeError:
        pytest.fail("Unexpected ValueError for single value. (Test A)")

    try:
        _check_type("text", "parameter", str)
    except TypeError:
        pytest.fail("Unexpected ValueError for single value. (Test B)")


def test__check_type_failing():
    # Test cases that should raise an error

    with pytest.raises(TypeError):
        _check_type(5, "parameter", float)

    with pytest.raises(TypeError):
        _check_type([5], "parameter", (int, float))

    with pytest.raises(TypeError):
        _check_type([5, 6], "parameter", (int, float))
