""" """

import pytest
import warnings


from kuehn_et_al_fdm.utilities import _check_magnitude_range


def test__check_magnitude_range_passing():
    # Test cases that should not raise an error
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        _check_magnitude_range(7, "normal")
        assert not any(
            issubclass(warning.category, UserWarning) for warning in w
        ), "Unexpected UserWarning for single value. (Test A)"

        w.clear()
        _check_magnitude_range([5, 6, 7, 8], "reverse")
        assert not any(
            issubclass(warning.category, UserWarning) for warning in w
        ), "Unexpected UserWarning for list of values. (Test B)"


def test__check_magnitude_range_failing():
    # Test cases that should raise an error

    with pytest.warns(UserWarning):
        _check_magnitude_range(5, "normal")

    with pytest.warns(UserWarning):
        _check_magnitude_range([1, 2, 3], "strike-slip")
