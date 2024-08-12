""" """

import pytest
import numpy as np


from kuehn_et_al_fdm.calc_prob_occur import calc_prob_occur


# Test setup
RTOL = 1e-2
FILE = "prob_occur_mean_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_calc_prob_occur_mean_model(load_expected):
    """Calculation verification."""

    # Inputs
    magnitude = 7.1
    style = "strike-slip"
    locations = load_expected["u_star"]
    displacments = load_expected["displ_site"]

    # Expected
    expected = load_expected["percentile"]

    # Computed
    computed = calc_prob_occur(
        magnitude=magnitude,
        location_array=locations,
        style=style,
        displacement_array=displacments,
        coefficient_type="mean",
    )

    # Checks
    np.testing.assert_allclose(
        expected,
        computed,
        rtol=RTOL,
        err_msg=f"Expected: {expected}, Computed: {computed}",
    )


def test_calc_prob_occur_coefficient_types():
    """Input verification."""

    valid_types = ["mean", "median"]
    for coefficient_type in valid_types:
        try:
            calc_prob_occur(
                magnitude=6.5,
                location_array=[0, 0.25, 0.5, 0.75, 1],
                style="normal",
                displacement_array=[0.01, 0.3, 1, 0.8, 0.1],
                coefficient_type=coefficient_type,
            )
        except ValueError:
            pytest.fail(
                f"ValueError raised unexpectedly for valid coefficient_type: {coefficient_type}"
            )

    invalid_types = ["average", "mode", "sum"]
    with pytest.raises(ValueError):
        for coefficient_type in invalid_types:
            calc_prob_occur(
                magnitude=6.5,
                location_array=[0, 0.25, 0.5, 0.75, 1],
                style="normal",
                displacement_array=[0.01, 0.3, 1, 0.8, 0.1],
                coefficient_type=coefficient_type,
            )
