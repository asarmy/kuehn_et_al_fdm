""" """

import pytest
import numpy as np


from kuehn_et_al_fdm.calc_prob_exceed import calc_prob_exceed


# Test setup
RTOL = 1e-2
FILE = "prob_exceed_mean_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_calc_prob_exceed_mean_model(load_expected):

    # Inputs
    magnitude = 6.5
    location = 0.25
    style = "normal"
    displ = load_expected["displ_m"]

    # Expected
    expected_folded = load_expected["probex_folded"]
    expected_site = load_expected["probex_site"]

    # Computed
    computed_folded = calc_prob_exceed(
        magnitude=magnitude,
        location=location,
        style=style,
        displacement_array=displ,
        coefficient_type="mean",
        folded=True,
        debug=False,
    )

    computed_site = calc_prob_exceed(
        magnitude=magnitude,
        location=location,
        style=style,
        displacement_array=displ,
        coefficient_type="mean",
        folded=False,
        debug=False,
    )

    # Checks
    np.testing.assert_allclose(
        expected_folded,
        computed_folded,
        rtol=RTOL,
        err_msg=f"For the folded case, Expected: {expected_folded}, Computed: {computed_folded}",
    )

    np.testing.assert_allclose(
        expected_site,
        computed_site,
        rtol=RTOL,
        err_msg=f"For the unfolded case, Expected: {expected_site}, Computed: {computed_site}",
    )
