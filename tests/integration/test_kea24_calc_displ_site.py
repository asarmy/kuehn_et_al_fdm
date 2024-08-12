""" """

import pytest
import numpy as np


from kuehn_et_al_fdm.calc_displ_site import calc_displ_site


# Test setup
RTOL = 1e-2
FILE = "site_displacement_mean_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_calc_displ_site_mean_model(load_expected):

    for row in load_expected:
        # Inputs
        magnitude, location, style, percentile, *expected = row

        # Expected
        expected_folded = expected[-1]
        expected_site = expected[-3]

        # Computed
        computed_folded = calc_displ_site(
            magnitude=magnitude,
            location=location,
            style=style,
            percentile=percentile,
            coefficient_type="mean",
            folded=True,
            debug=False,
        )

        computed_site = calc_displ_site(
            magnitude=magnitude,
            location=location,
            style=style,
            percentile=percentile,
            coefficient_type="mean",
            folded=False,
            debug=False,
        )

        # Checks
        np.testing.assert_allclose(
            expected_folded,
            computed_folded,
            rtol=RTOL,
            err_msg=f"Mag {magnitude}, u-star {location}, Folded, Expected: {expected_folded}, Computed: {computed_folded}",
        )

        np.testing.assert_allclose(
            expected_site,
            computed_site,
            rtol=RTOL,
            err_msg=f"Mag {magnitude}, u-star {location}, Unfolded, Expected: {expected_site}, Computed: {computed_site}",
        )


@pytest.mark.parametrize("filename", [FILE])
def test_calc_displ_site_mean_model_debug(load_expected):

    for row in load_expected:
        # Inputs
        magnitude, location, style, percentile, *expected = row

        # Expected
        expected_keys = [
            "bc_param",
            "mean_site",
            "stdv_site",
            "mean_complement",
            "stdv_complement",
            "Y_site",
            "Y_complement",
            "Y_folded",
            "displ_site_meters",
            "displ_complement_meters",
            "displ_folded_meters",
        ]
        expected_values = dict(zip(expected_keys, expected))

        # Computed
        results = calc_displ_site(
            magnitude=magnitude,
            location=location,
            style=style,
            percentile=percentile,
            coefficient_type="mean",
            debug=True,
        )
        for key, expected in expected_values.items():
            computed = results[key]
            np.testing.assert_allclose(
                expected,
                computed,
                rtol=RTOL,
                err_msg=f"Mag {magnitude}, u-star {location}, {key}, Expected: {expected}, Computed: {computed}",
            )


# Test setup
FILE = "site_displacement_full_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_calc_displ_site_full_model(load_expected):

    # Inputs
    magnitude = 7
    location = 0.5
    style = "strike-slip"
    percentile = 0.84

    # Expected
    expected = load_expected["displ_folded"]

    # Computed
    computed = calc_displ_site(
        magnitude=magnitude,
        location=location,
        style=style,
        percentile=percentile,
        coefficient_type="full",
        debug=False,
    )

    # Checks
    np.testing.assert_allclose(
        expected,
        computed,
        rtol=RTOL,
        err_msg=f"Expected: {expected}, Computed: {computed}",
    )
