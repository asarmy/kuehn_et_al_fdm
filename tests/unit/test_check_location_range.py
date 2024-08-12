""" """

import pytest


from kuehn_et_al_fdm.utilities import _check_location_range


def test__check_location_range_passing():
    # Test cases that should not raise an error
    try:
        _check_location_range(0.25)
    except ValueError:
        pytest.fail("Unexpected ValueError for single value. (Test A)")

    try:
        _check_location_range([0.25, 0.33, 0.5, 0.65])
    except ValueError:
        pytest.fail("Unexpected ValueError for single value. (Test B)")


def test__check_location_range_failing():
    # Test cases that should raise an error

    with pytest.raises(ValueError):
        _check_location_range(42)

    with pytest.raises(ValueError):
        _check_location_range([0.25, 0.33, 0.5, 0.65, 42])
