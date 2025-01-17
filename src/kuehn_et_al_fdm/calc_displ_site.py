"""This module calculates the predicted displacement for a magnitude/location/style/percentile scenario.
In other words, this module implements the model in a deterministic fault displacement hazard analysis.
"""

# Python imports
import argparse
import numpy as np
import pandas as pd

# Module imports
from kuehn_et_al_fdm.calc_params import _calc_params
from kuehn_et_al_fdm.transformation_functions import _calc_transformed_displ, _convert_bc_to_meters
from kuehn_et_al_fdm._common_args import *  # noqa: F403 *


def calc_displ_site(
    *,
    magnitude,
    location,
    style,
    percentile,
    coefficient_type="median",
    folded=True,
    debug=False,
    override=False,
):
    """
    Calculate the predicted displacement in meters. If displacement is less than 1 mm (0.001 m),
    returns zero.

    Parameters
    ----------
    magnitude : int or float or numpy.ndarray with a single element
        Earthquake moment magnitude.

    location : int or float or numpy.ndarray with a single element
        Normalized location along rupture length, range [0, 1.0].

    style : str
        Style of faulting (case-insensitive). Valid options are 'strike-slip', 'reverse', or
        'normal'.

    percentile : int or float or numpy.ndarray with a single element
        Aleatory quantile value. Use -1 for mean.

    coefficient_type : str, optional
        Option to run model using full epistemic uncertainty or with point estimates (mean or
        median) of the model coefficients (case-insensitive). Valid options are 'mean', 'median',
        or 'full'. Default 'median'.

    folded : boolean, optional
        Return displacement for the folded location. Default True.

    debug : boolean, optional
        Option to return DataFrame of internal calculations. Default False.

    override : boolean, optional
        Option to override single scenario limitation that is hard-coded. Not recommended for most
        users. Default False.

    Returns
    -------
    If debug is False:
        displ_folded_meters : numpy.ndarray
            Displacement in meters for the folded location. The array contains a single element.

    If debug is True:
        pd.DataFrame
            A DataFrame with the following columns:

            - **magnitude**: Earthquake moment magnitude.
            - **location**: Normalized location along rupture length.
            - **style**: Style of faulting.
            - **percentile**: The percentile for which the displacement is calculated.
            - **model_id**: Model coefficient row number or point estimate definition.
            - **bc_param**: Box-Cox transformation parameter (lambda).
            - **mean_site**: Mean displacement in transformed units for the site location.
            - **stdv_site**: Total standard deviation in transformed units for the site location.
            - **mean_complement**: Mean displacement in transformed units for the complementary location.
            - **stdv_complement**: Total standard deviation in transformed units for the complementary location.
            - **Y_site**: Transformed displacement for the site location.
            - **Y_complement**: Transformed displacement for the complementary location.
            - **Y_folded**: Transformed displacement for the folded location.
            - **displ_site_meters**: Displacement in meters for the site location.
            - **displ_complement_meters**: Displacement in meters for the complementary location.
            - **displ_folded_meters**: Displacement in meters for the folded location.


    Raises
    ------
    RuntimeError
        If `debug` is `True` and `override` is also `True`. Debug mode is not available when
        running multiple scenarios because the dataframe arrays are mismatched.

    Examples
    --------
    From command line:

    .. code-block:: console

        $ kea-displ_site -m 7 -l 0.25 -s strike-slip -p 0.5 -ct full --debug
        $ kea-displ_site -m 7 -l 0.25 -s strike-slip -p 0.5 --unfolded
    """
    # Calculate statistical distribution parameter predictions
    coefficient_type = coefficient_type.lower()
    params = {
        "magnitude": magnitude,
        "style": style,
        "coefficient_type": coefficient_type,
        "override": override,
    }
    model_id, bc_param, mean_site, stdv_site, _, _ = _calc_params(**params, location=location)
    _, _, mean_complement, stdv_complement, _, _ = _calc_params(**params, location=1 - location)

    # Calculate transformed displacement
    Y_site = _calc_transformed_displ(bc_param, mean_site, stdv_site, percentile)
    Y_complement = _calc_transformed_displ(bc_param, mean_complement, stdv_complement, percentile)
    Y_folded = np.mean([Y_site, Y_complement], axis=0)

    # Back-transform displacement to meters
    displ_site_meters = _convert_bc_to_meters(Y_site, bc_param)
    displ_complement_meters = _convert_bc_to_meters(Y_complement, bc_param)  # noqa: F841
    displ_folded_meters = _convert_bc_to_meters(Y_folded, bc_param)

    if debug:
        if override:
            raise RuntimeError(
                "***Debug is not available when `override=True`. \n"
                "   This is because the dataframe arrays are mismatched. \n"
                "   Try again with only one scenario. \n"
            )
            # TODO: vectorize / organize
        else:
            result = {
                k: v
                for k, v in locals().items()
                if k not in ["coefficient_type", "folded", "debug", "override", "params", "_"]
            }
            return pd.DataFrame.from_dict(result)
    else:
        return displ_folded_meters if folded else displ_site_meters


# Create an ArgumentParser instance and add specific arguments to the parser
parser = argparse.ArgumentParser(
    description=calc_displ_site.__doc__, formatter_class=argparse.RawTextHelpFormatter
)
_add_magnitude(parser)
_add_location(parser)
_add_style(parser)
_add_percentile(parser)
_add_coefficient_type(parser)
_add_folded_flag(parser)
_add_debug_flag(parser)


@_add_arguments(parser)
def main(**kwargs):

    try:
        result = calc_displ_site(**kwargs)

        if kwargs.get("debug", True):
            print(result)
        else:
            print(
                f"     Displacement for magnitude {kwargs.get('magnitude')}, "
                f"location {kwargs.get('location')}, percentile {kwargs.get('percentile')}, "
                f"{kwargs.get('style')} faulting:"
            )
            print(f"     {np.round(result.squeeze(), 3)} meters")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
