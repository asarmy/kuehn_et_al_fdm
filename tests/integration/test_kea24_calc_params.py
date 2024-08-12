""" """

import pytest
import numpy as np

from kuehn_et_al_fdm.calc_params import _calc_params


# Test setup
RTOL = 1e-2
FILE = "distribution_params_full_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test__calc_params_full_model(load_expected):

    # Inputs
    magnitude = 7
    location = 0.5
    style = "normal"

    # Expected
    expected_values = {
        "bc_param": load_expected["lambda"],
        "mean": load_expected["mu"],
        "stdv_total": load_expected["sigma_tot"],
        "stdv_within": load_expected["sigma_u"],
        "stdv_between": load_expected["sigma_m"],
    }

    # Computed
    computed = _calc_params(
        magnitude=magnitude, location=location, style=style, coefficient_type="full"
    )
    computed_values = {
        "bc_param": computed[1],
        "mean": computed[2],
        "stdv_total": computed[3],
        "stdv_within": computed[4],
        "stdv_between": computed[5],
    }

    # Checks
    for key, expected in expected_values.items():
        computed = computed_values[key]
        np.testing.assert_allclose(
            expected,
            computed,
            rtol=RTOL,
            err_msg=f"Mag {magnitude}, u-star {location}, {key}, Expected: {expected}, Computed: {computed}",
        )


# Test setup
FILE = "distribution_params_mean_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test__calc_params_mean_model(load_expected):
    for row in load_expected:
        # Inputs
        magnitude, location, style, *expected = row

        # Expected
        expected_keys = [
            "bc_param",
            "mean",
            "stdv_between",
            "stdv_within",
            "stdv_total",
        ]
        expected_values = dict(zip(expected_keys, expected))

        # Computed
        computed = _calc_params(
            magnitude=magnitude, location=location, style=style, coefficient_type="mean"
        )
        computed_values = {
            "bc_param": computed[1],
            "mean": computed[2],
            "stdv_total": computed[3],
            "stdv_within": computed[4],
            "stdv_between": computed[5],
        }

        # Checks
        for key, expected in expected_values.items():
            computed = computed_values[key]
            np.testing.assert_allclose(
                expected,
                computed,
                rtol=RTOL,
                err_msg=f"Mag {magnitude}, u-star {location}, {key}, Expected: {expected}, Computed: {computed}",
            )
