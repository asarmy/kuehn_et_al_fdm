"""This module calculates the probability of occurance for a magnitude/location/style scenario.
For example, one can compute the percentile rank of an observation(s) with respect to the model
predictions.
"""

# Python imports
import argparse
import warnings
import numpy as np
from scipy import stats

# Module imports
from kuehn_et_al_fdm.utilities import _check_type
from kuehn_et_al_fdm.calc_params import _calc_params
from kuehn_et_al_fdm._common_args import *  # noqa: F403 *


def calc_prob_occur(
    *, magnitude, location_array, style, displacement_array, coefficient_type="median"
):
    """
    Calculate the percentile rank of observations.
    Note that the ocation-displacement array pairs should be oriented with the profile peak at
    location <= 0.5.

    Parameters
    ----------
    magnitude : int or float or numpy.ndarray with a single element
        Earthquake moment magnitude.

    location_array : ArrayLike
        Normalized locations along rupture length, range [0, 1.0].

    style : str
        Style of faulting (case-insensitive). Valid options are 'strike-slip', 'reverse', or
        'normal'.

    displacement_array : ArrayLike
        Test values of displacement in meters.

    coefficient_type : str, optional
        Option to run model using mean or median point estimates of the model coefficients (case-
        insensitive). Valid options are 'mean' or 'median'. (The 'full' option is not enabled for
        this function.) Default 'median'.

    Returns
    -------
    percentile : numpy.ndarray
        Percentile rank for the location-displacement pair using the unfolded model (right-skewed).

    Raises
    ------
    ValueError
        If `location_array` and `displacement_array` do not have the same shape.

        If `coefficient_type` is not 'mean' or 'median'.

    Examples
    --------
    From command line:

    .. code-block:: console

        $ kea-prob_occur -m 6.2 -l 0 0.4 0.5 0.7 0.9 1 -s reverse -d 0.12 0.34 0.6 0.55 0.4 0.1
    """
    # Only one value is allowed
    msg = "***Note: Only one value is allowed."
    _check_type(magnitude, "magnitude", (int, float), msg=msg)

    # Displacement and location arrays should be the same shape
    location_array = np.atleast_1d(location_array)
    displacement_array = np.atleast_1d(displacement_array)
    if location_array.shape != displacement_array.shape:
        raise ValueError(
            f"The location and displacement arrays are not the same length.\n"
            f"Location array is {location_array.shape} and displacement array is {displacement_array.shape}."
        )

    coefficient_type = coefficient_type.lower()

    if coefficient_type not in ["mean", "median"]:
        raise ValueError(
            f"'{coefficient_type}' is an invalid 'coefficient_type';"
            " only 'mean' or 'median' is allowed."
        )

    # Calculate statistical distribution parameter predictions
    params = {
        "magnitude": magnitude,
        "location": location_array,
        "style": style,
        "coefficient_type": coefficient_type,
    }
    vectorized_params_calc = np.vectorize(_calc_params)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model_id, bc_param, mean_site, stdv_site, _, _ = vectorized_params_calc(
            **params, override=True
        )
        # override allows multiple locations

    # Calculate transformed displacements
    transformed_displ = (displacement_array**bc_param - 1) / bc_param

    # Calculate percentile rank of the observations
    return stats.norm.cdf(x=transformed_displ, loc=mean_site, scale=stdv_site)


# Create an ArgumentParser instance and add specific arguments to the parser
parser = argparse.ArgumentParser(
    description=calc_prob_occur.__doc__, formatter_class=argparse.RawTextHelpFormatter
)
_add_magnitude(parser)
_add_location(parser, nargs="+")
_add_style(parser)
_add_displacement(parser)
_add_coefficient_type(parser)


@_add_arguments(parser)
def main(**kwargs):

    try:
        result = calc_prob_occur(**kwargs)

        print("     Percentiles for observed displacements:")
        print(f"     {np.round(result.squeeze(), 3)}")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
