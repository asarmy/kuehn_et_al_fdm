""" """

import pytest
import numpy as np


from kuehn_et_al_fdm.load_data import DATA
from kuehn_et_al_fdm.prediction_functions import (
    _func_mu,
    _func_mode,
    _func_sd_u,
)

# Test setup
RTOL = 1e-2
STYLE = "reverse"
MODEL = "mean"
FILE = "reverse_mean-model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_misc_reverse(load_expected):

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
        "sd_mode": np.full(len(magnitudes), coeffs["s_m,r"]),
        "sd_u": _func_sd_u(coeffs, locations),
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
