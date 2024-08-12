import pytest
import numpy as np


from kuehn_et_al_fdm.calc_displ_profile import calc_displ_profile


# Test setup
RTOL = 1e-2
FILE = "profile_displacement_mean_model.csv"


@pytest.mark.parametrize("filename", [FILE])
def test_calc_displ_profile_mean_model(load_expected):
    """Calculation verification."""

    # Inputs
    magnitude = 6.5
    style = "normal"
    percentile = 0.84
    step_size = 0.1

    # Expected
    expected_folded = load_expected["displ_folded"]
    expected_unfolded = load_expected["displ_site"]

    # Computed
    _, computed_folded = calc_displ_profile(
        magnitude=magnitude,
        style=style,
        percentile=percentile,
        coefficient_type="mean",
        folded=True,
        location_step=step_size,
    )
    _, computed_unfolded = calc_displ_profile(
        magnitude=magnitude,
        style=style,
        percentile=percentile,
        coefficient_type="mean",
        folded=False,
        location_step=step_size,
    )

    # Checks
    np.testing.assert_allclose(
        expected_folded,
        computed_folded,
        rtol=RTOL,
        err_msg=f"For folded profile, Expected: {expected_folded}, Computed: {computed_folded}",
    )
    np.testing.assert_allclose(
        expected_unfolded,
        computed_unfolded,
        rtol=RTOL,
        err_msg=f"For unfolded profile, Expected: {expected_unfolded}, Computed: {computed_unfolded}",
    )


def test_calc_displ_profile_coefficient_types():
    """Input verification."""

    valid_types = ["mean", "median"]
    for coefficient_type in valid_types:
        try:
            locs, displs = calc_displ_profile(
                magnitude=7,
                style="strike-slip",
                percentile=0.5,
                coefficient_type=coefficient_type,
                folded=False,
                location_step=0.1,
            )
        except ValueError:
            pytest.fail(
                f"ValueError raised unexpectedly for valid coefficient_type: {coefficient_type}"
            )

    invalid_types = ["average", "mode", "sum"]
    with pytest.raises(ValueError):
        for coefficient_type in invalid_types:
            locs, displs = calc_displ_profile(
                magnitude=7,
                style="strike-slip",
                percentile=0.5,
                coefficient_type=coefficient_type,
                folded=False,
                location_step=0.1,
            )
