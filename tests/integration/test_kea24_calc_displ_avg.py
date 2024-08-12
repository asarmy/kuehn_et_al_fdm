""" """

import pytest
import numpy as np


from kuehn_et_al_fdm.calc_displ_avg import calc_displ_avg


# Test setup
RTOL = 1e-2
FILE = "avg_displacement.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_calc_displ_avg_mean_model(load_expected):
    """Calculation verification."""

    for row in load_expected:
        # Data
        magnitude, style, expected = row

        # Computed
        computed = calc_displ_avg(
            magnitude=magnitude,
            style=style,
            coefficient_type="mean",
        )
        np.testing.assert_allclose(
            expected,
            computed,
            rtol=RTOL,
            err_msg=f"Mag {magnitude}, style {style}, Expected: {expected}, Computed: {computed}",
        )


def test_calc_displ_avg_coefficient_types():
    """Input verification."""

    valid_types = ["mean", "median"]
    for coefficient_type in valid_types:
        try:
            calc_displ_avg(
                magnitude=6,
                style="reverse",
                coefficient_type=coefficient_type,
            )
        except ValueError:
            pytest.fail(
                f"ValueError raised unexpectedly for valid coefficient_type: {coefficient_type}"
            )

    invalid_types = ["average", "mode", "sum"]
    with pytest.raises(ValueError):
        for coefficient_type in invalid_types:
            calc_displ_avg(
                magnitude=6,
                style="reverse",
                coefficient_type=coefficient_type,
            )
