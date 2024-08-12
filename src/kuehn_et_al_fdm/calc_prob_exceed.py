"""This module calculates the probability of exceedance for a magnitude/location/style scenario.
In other words, this module implements the conditional probability of exceedance term in the hazard
integral in a probabilistic fault displacement hazard analysis.
"""

# Python imports
import argparse
import types
import numpy as np
import pandas as pd
from scipy import stats

# Module imports
from kuehn_et_al_fdm.calc_params import _calc_params
from kuehn_et_al_fdm._common_args import *  # noqa: F403 * # noqa: F403


def _create_debug_dataframe(**kwargs):
    """A helper function to create the debugging dataframe."""
    # Create dynamic variables
    ns = types.SimpleNamespace(**kwargs)

    # Repeat scenario info
    arrays = [ns.magnitude, ns.location, ns.style]
    reshaped_arrays = [np.full(ns.reshaped_displ.shape[0], arr) for arr in arrays]
    magnitude, location, style = reshaped_arrays
    del arrays, reshaped_arrays

    # Create DataFrame
    keys = [
        "magnitude",
        "location",
        "style",
        "model_id",
        "bc_param",
        "mean_site",
        "stdv_site",
        "mean_complement",
        "stdv_complement",
    ]
    values = [
        magnitude,
        location,
        style,
        ns.model_id,
        ns.bc_param,
        ns.mean_site,
        ns.stdv_site,
        ns.mean_complement,
        ns.stdv_complement,
    ]
    values = [v.flatten() for v in values]
    result = {k: v for k, v in zip(keys, values)}
    datafame = pd.DataFrame.from_dict(result)
    del keys, values, result

    # Explode dataframe based on number of displacement exceedances
    arrays = [
        ns.reshaped_displ,
        ns.transformed_displ,
        ns.probex_site,
        ns.probex_complement,
        ns.probex_folded,
    ]
    names = [
        "displ_meters",
        "transformed_displ",
        "probex_site",
        "probex_complement",
        "probex_folded",
    ]
    for array, name in zip(arrays, names):
        datafame[name] = [list(row) for row in array]

    return datafame.apply(lambda col: col.explode() if col.name in names else col)


def calc_prob_exceed(
    *,
    magnitude,
    location,
    style,
    displacement_array,
    coefficient_type="median",
    folded=True,
    debug=False,
):
    """
    Calculate the probability of exceedance.

    Parameters
    ----------
    magnitude : int or float or numpy.ndarray with a single element
        Earthquake moment magnitude.

    location : int or float or numpy.ndarray with a single element
        Normalized location along rupture length, range [0, 1.0].

    style : str
        Style of faulting (case-insensitive). Valid options are 'strike-slip', 'reverse', or
        'normal'.

    displacement_array : ArrayLike
        Test values of displacement in meters.

    coefficient_type : str, optional
        Option to run model using full epistemic uncertainty or with point estimates (mean or
        median) of the model coefficients (case-insensitive). Valid options are 'mean', 'median',
        or 'full'. Default 'median'.

    folded : boolean, optional
        Return probability of exceedance for the folded location. Default True.

    debug : boolean, optional
        Option to return DataFrame of internal calculations. Default False.

    Returns
    -------
    If debug is False:
        If `coefficient_type` is not 'full':
            probex_folded : numpy.ndarray, optional
                Probability of exceedance for the folded location (if folded is True).
            probex_site : numpy.ndarray, optional
                Probability of exceedance for the site location (if folded is False).

        If `coefficient_type` is 'full':
            pandas.DataFrame
                A DataFrame with the following columns:

                - **model_id**: Model coefficient row number or point estimate definition.
                - **displ_meters**: Test value of displacement in meters.
                - **transformed_displ**: Test value of displacement in transformed units.
                - **probex_folded**: Probability of exceedance for the folded location (if folded is True).
                - **probex_site**: Probability of exceedance for the site location (if folded is False).

    If debug is True:
        pandas.DataFrame
            A DataFrame with the following columns:

            - **magnitude**: Earthquake moment magnitude.
            - **location**: Normalized location along rupture length.
            - **style**: Style of faulting.
            - **model_id**: Model coefficient row number or point estimate definition.
            - **bc_param**: Box-Cox transformation parameter (lambda).
            - **mean_site**: Mean displacement in transformed units for the site location.
            - **stdv_site**: Total standard deviation in transformed units for the site location.
            - **mean_complement**: Mean displacement in transformed units for the complementary location.
            - **stdv_complement**: Total standard deviation in transformed units for the complementary location.
            - **displ_meters**: Test value of displacement in meters.
            - **transformed_displ**: Test value of displacement in transformed units.
            - **probex_site**: Probability of exceedance for the site location.
            - **probex_complement**: Probability of exceedance for the complementary location.
            - **probex_folded**: Probability of exceedance for the folded location.


    Raises
    ------
    ValueError
        If `coefficient_type` is not 'mean', 'median', or 'full'.

    Examples
    --------
    From command line:

    .. code-block:: console

        $ kea-prob_exceed -m 6 -l 0.2 -s reverse -d .01 0.03 0.1 0.3 1 3 10 30
        $ kea-prob_exceed -m 6 -l 0.2 -s reverse -d .01 0.03 0.1 0.3 1 3 10 30 --debug
    """
    # Calculate statistical distribution parameter predictions
    coefficient_type = coefficient_type.lower()
    params = {"magnitude": magnitude, "style": style, "coefficient_type": coefficient_type}
    model_id, bc_param, mean_site, stdv_site, _, _ = _calc_params(**params, location=location)
    _, _, mean_complement, stdv_complement, _, _ = _calc_params(**params, location=1 - location)

    # Reshape arrays for broadcasting
    arrays = [model_id, bc_param, mean_site, stdv_site, mean_complement, stdv_complement]
    reshaped_arrays = [arr[:, np.newaxis] for arr in arrays]
    model_id, bc_param, mean_site, stdv_site, mean_complement, stdv_complement = reshaped_arrays
    del arrays, reshaped_arrays

    # Calculate transformed displacements
    reshaped_displ = np.tile(np.atleast_1d(displacement_array), (bc_param.shape[0], 1))
    transformed_displ = (reshaped_displ**bc_param - 1) / bc_param

    # Calculate probability of exceedances
    probex_site = 1 - stats.norm.cdf(x=transformed_displ, loc=mean_site, scale=stdv_site)
    probex_complement = 1 - stats.norm.cdf(
        x=transformed_displ, loc=mean_complement, scale=stdv_complement
    )
    probex_folded = np.mean((probex_site, probex_complement), axis=0)

    # Collect variables in a dictionary to pass into datafame creator function if needed
    results = {
        k: v
        for k, v in locals().items()
        if k not in ["displacement_array", "coefficient_type", "folded", "debug", "params", "_"]
    }

    # Use Pandas DataFrame to manage results for debugging
    if debug:
        return _create_debug_dataframe(**results)

    # Also use Pandas DataFrame to manage results for full set of coefficients
    if coefficient_type == "full":
        dataframe = _create_debug_dataframe(**results)
        columns = ["model_id", "displ_meters"]

        if folded:
            columns.append("probex_folded")
            return dataframe[columns].copy()

        else:
            columns.append("probex_site")
            return dataframe[columns].copy()

    # Return array if point estimates of coefficients are used
    else:
        if coefficient_type not in ["mean", "median"]:
            raise ValueError(
                f"'{coefficient_type}' is an invalid 'coefficient_type';"
                " only 'mean', 'median', or 'full' is allowed."
            )

        return probex_folded.squeeze() if folded else probex_site.squeeze()


# Create an ArgumentParser instance and add specific arguments to the parser
parser = argparse.ArgumentParser(
    description=calc_prob_exceed.__doc__, formatter_class=argparse.RawTextHelpFormatter
)
_add_magnitude(parser)
_add_location(parser)
_add_style(parser)
_add_displacement(parser)
_add_coefficient_type(parser)
_add_folded_flag(parser)
_add_debug_flag(parser)


@_add_arguments(parser)
def main(**kwargs):

    try:
        result = calc_prob_exceed(**kwargs)

        if kwargs.get("debug", True):
            print(result)
        else:
            print(
                f"     Probability of exceedance for magnitude {kwargs.get('magnitude')}, "
                f"location {kwargs.get('location')}, percentile {kwargs.get('percentile')}, "
                f"{kwargs.get('style')} faulting:"
            )
            print("    ", np.array2string(result, formatter={"float_kind": lambda x: f"{x:.4e}"}))

            print("     Displacement (meters):")
            print(f"     {kwargs.get('displacement_array')} ")

    except ValueError as e:
        print(e)
