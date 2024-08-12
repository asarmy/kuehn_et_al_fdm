"""This module calculates the predicted displacement profile for a magnitude/style/percentile scenario."""

# Python imports
import argparse
import warnings
import numpy as np

# Module imports
from kuehn_et_al_fdm.calc_displ_site import calc_displ_site
from kuehn_et_al_fdm._common_args import *  # noqa: F403 *


def calc_displ_profile(
    *, magnitude, style, percentile, coefficient_type="median", folded=True, location_step=0.05
):
    """
    Calculate the predicted displacement profile in meters.

    Parameters
    ----------
    magnitude : int or float or numpy.ndarray with a single element
        Earthquake moment magnitude.

    style : str
        Style of faulting (case-insensitive). Valid options are 'strike-slip', 'reverse', or
        'normal'.

    percentile : int or float or numpy.ndarray with a single element
        Aleatory quantile value. Use -1 for mean.

    coefficient_type : str, optional
        Option to run model using mean or median point estimates of the model coefficients (case-
        insensitive). Valid options are 'mean' or 'median'. (The 'full' option is not enabled for
        this function.) Default 'median'.

    folded : boolean, optional
        Return displacement for the folded location. Default True.

    location_step : float, optional
        Profile location step interval. Default 0.05.

    Returns
    -------
    tuple
        - 'locations': Normalized location along rupture length.
        - 'displ_meters': Displacement in meters.

    Raises
    ------
    ValueError
        If `coefficient_type` is not 'mean' or 'median'.

    Examples
    --------
    From command line:

    .. code-block:: console

        $ kea-displ_profile -m 6 -s reverse -p 0.5
        $ kea-displ_profile -m 6 -s reverse -p -1 -ls 0.01 -ct median --unfolded
    """
    coefficient_type = coefficient_type.lower()
    if coefficient_type not in ["mean", "median"]:
        raise ValueError(
            f"'{coefficient_type}' is an invalid 'coefficient_type';"
            " only 'mean' or 'median' is allowed for the profile."
        )

    locations = np.arange(0, 1 + location_step, location_step)
    params = {
        "magnitude": magnitude,
        "location": locations,
        "style": style,
        "percentile": percentile,
        "folded": folded,
        "coefficient_type": coefficient_type,
    }
    vectorized_site_calc = np.vectorize(calc_displ_site)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        displ_meters = vectorized_site_calc(**params, override=True)
        # override allows multiple scenarios; default is false to avoid mis-matched arrays

    return locations, displ_meters


# Create an ArgumentParser instance and add specific arguments to the parser
parser = argparse.ArgumentParser(
    description=calc_displ_profile.__doc__, formatter_class=argparse.RawTextHelpFormatter
)
_add_magnitude(parser)
_add_style(parser)
_add_percentile(parser)
_add_coefficient_type(parser)
_add_folded_flag(parser)
_add_location_step(parser)


@_add_arguments(parser)
def main(**kwargs):

    try:
        result = calc_displ_profile(**kwargs)

        print(
            f"     Displacments for magnitude {kwargs.get('magnitude')}, "
            f"percentile {kwargs.get('percentile')}, {kwargs.get('style')} faulting:"
        )
        print(f"     {np.round(result[1].squeeze(), 3)} meters")

        print("     Locations:")
        print(f"     {result[0].squeeze()} ")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
