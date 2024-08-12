""" """

import pytest
import numpy as np


from kuehn_et_al_fdm.load_data import DATA
from kuehn_et_al_fdm.prediction_functions import (
    _func_mu,
    _func_mode,
    _func_sd_mode_sigmoid,
)

# Test setup
RTOL = 1e-2
STYLE = "normal"
MODEL = "mean"
FILE = "normal_mean-model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_misc_normal(load_expected):

    # Coefficients
    coeffs = DATA["point"][STYLE]
    coeffs = coeffs[coeffs["model_id"] == MODEL].to_records(index=False)

    # Inputs
    magnitudes = load_expected["mag"]
    locations = load_expected["u_star"]

    # Expected
    expected_values = {
        "mode": load_expected["mode"],
        "mu": load_expected["mu"],
        "sd_mode": load_expected["sd_mode"],
        "sd_u": load_expected["sd_u"],
    }

    # Computed
    computed_values = {
        "mode": _func_mode(coeffs, magnitudes),
        "mu": _func_mu(coeffs, magnitudes, locations),
        "sd_mode": _func_sd_mode_sigmoid(coeffs, magnitudes),
        "sd_u": np.full(len(magnitudes), coeffs["sigma"]),
    }

    # Checks
    for key, expected in expected_values.items():
        computed = computed_values[key]
        np.testing.assert_allclose(
            expected,
            computed,
            rtol=RTOL,
            err_msg=f"Mag {magnitudes}, u-star {locations}, {key}, Expected: {expected}, Computed: {computed}",
        )
