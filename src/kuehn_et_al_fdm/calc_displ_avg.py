"""This module calculates the median predicted average displacement for a magnitude/style."""

# Python imports
import argparse
import warnings
import numpy as np

# Module imports
from kuehn_et_al_fdm.calc_params import _calc_params
from kuehn_et_al_fdm.transformation_functions import _calc_analytic_mean
from kuehn_et_al_fdm._common_args import *  # noqa: F403 *


def calc_displ_avg(*, magnitude, style, coefficient_type="median"):
    """
    Calculate the median predicted average displacement in meters.

    Parameters
    ----------
    magnitude : int or float or numpy.ndarray with a single element
        Earthquake moment magnitude.

    style : str
        Style of faulting (case-insensitive). Valid options are 'strike-slip', 'reverse', or
        'normal'.

    coefficient_type : str, optional
        Option to run model using mean or median point estimates of the model coefficients (case-
        insensitive). Valid options are 'mean' or 'median'. (The 'full' option is not enabled for
        this function.) Default 'median'.

    Returns
    -------
    float
        Average displacement in meters.

    Raises
    ------
    ValueError
        If `coefficient_type` is not 'mean' or 'median'.

    Examples
    --------
    From command line:

    .. code-block:: console

        $ kea-displ_avg -m 7 -s normal
    """
    coefficient_type = coefficient_type.lower()
    if coefficient_type not in ["mean", "median"]:
        raise ValueError(
            f"'{coefficient_type}' is an invalid 'coefficient_type';"
            " only 'mean' or 'median' is allowed."
        )

    # Calculate statistical distribution parameter predictions
    # Dense location spacing is used to create well-descritized profile for intergration
    params = {"magnitude": magnitude, "style": style, "coefficient_type": coefficient_type}
    locations = np.arange(0, 1.01, 0.01)
    vectorized_param_calc = np.vectorize(_calc_params)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _, bc_param, mean, _, stdv_within, _ = vectorized_param_calc(
            **params, location=locations, override=True
        )
        # override allows multiple scenarios; default is false to avoid mis-matched arrays

    # Calculate predicted mean slip profile
    # Use within-event variability only for median AD; see manucript for discussion
    mean_displ_meters = _calc_analytic_mean(bc_param, mean, stdv_within)

    # Calculate area under the mean slip profile; this is the Average Displacement (AD)
    return np.trapz(mean_displ_meters, locations)


# Create an ArgumentParser instance and add specific arguments to the parser
parser = argparse.ArgumentParser(
    description=calc_displ_avg.__doc__, formatter_class=argparse.RawTextHelpFormatter
)
_add_magnitude(parser)
_add_style(parser)


@_add_arguments(parser)
def main(**kwargs):

    try:
        result = calc_displ_avg(**kwargs)

        print(
            "     Median prediction for average displacement for magnitude "
            f"{kwargs.get('magnitude')}, {kwargs.get('style')} faulting: "
        )
        print(f"     {np.round(result.squeeze(), 3)} meters")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
