"""This module calculates the statistical distribution parameters for forward predition of the model."""

# Python imports
import argparse
import warnings
import numpy as np


# Module imports
from kuehn_et_al_fdm.load_data import DATA
from kuehn_et_al_fdm.utilities import _check_type, _check_location_range, _check_magnitude_range
from kuehn_et_al_fdm.prediction_functions import _func_nm, _func_rv, _func_ss
from kuehn_et_al_fdm._common_args import *  # noqa: F403 *


def _calc_params(*, magnitude, location, style, coefficient_type="median", override=False):
    """
    Calculate the predicted statistical distribution parameters.

    Parameters
    ----------
    magnitude : int or float
        Earthquake moment magnitude.

    location : int or float
        Normalized location along rupture length, range [0, 1.0].

    style : tr
        Style of faulting (case-insensitive). Valid options are 'strike-slip', 'reverse', or
        'normal'.

    coefficient_type : str, optional
        Option to run model using full epistemic uncertainty or with point estimates (mean or
        median) of the model coefficients (case-insensitive). Valid options are 'mean', 'median',
        or 'full'. Default 'median'.

    override : boolean, optional
        Option to override single scenario limitation that is hard-coded. Not recommended for most
        users. Default False.

    Returns
    -------
    tuple
        - 'model_id': Model coefficient row number or point estimate definition.
        - 'bc_param': Box-Cox transformation parameter (lambda).
        - 'mean': Mean displacement in transformed units (unfolded).
        - 'stdv_total': Total standard deviation in transformed units (unfolded).
        - 'stdv_within': Within-event standard deviation in transformed units (unfolded).
        - 'stdv_between': Between-event standard deviation in transformed units (unfolded).

    Raises
    ------
    ValueError
        If `coefficient_type` is not 'mean', 'median', or 'full'.

    ValueError
        If `location` is not within range [0, 1].

    Warns
    -----
    UserWarning
        If `override` is `True`, indicating that multiple scenarios are being run.

    UserWarning
        If `magnitude` is not within the recommended range for that style.

    Examples
    --------
    From command line:

    .. code-block:: console

        $ kea-stat_params -m 6 -l 0.33 -s normal
    """
    # Only one value is allowed
    # TODO: vectorize / organize
    msg = "***Note: Only one value is allowed."
    _check_type(style, "style", str, msg=msg)

    if not override:
        _check_type(magnitude, "magnitude", (int, float), msg=msg)
        _check_type(location, "location", (int, float), msg=msg)
    else:
        magnitude = np.atleast_1d(magnitude)
        location = np.atleast_1d(location)
        warnings.warn("\n***Running multiple scenarios. Track your mag/loc.\n", UserWarning)

    style = style.lower()
    coefficient_type = coefficient_type.lower()

    # Check ranges of inputs
    _check_location_range(location)
    _check_magnitude_range(magnitude, style)

    function_map = {"strike-slip": _func_ss, "reverse": _func_rv, "normal": _func_nm}

    # Calculate parameters for each set of coefficients
    if coefficient_type == "full":
        coeffs = DATA["full"][style].to_records(index=False)
        model_id, lam, mu, sd_total, sd_u, sd_mode = function_map[style](
            coeffs, magnitude, location
        )

    # Calculate parameters for point estimates of coefficients
    else:
        if coefficient_type not in ["mean", "median"]:
            raise ValueError(
                f"'{coefficient_type}' is an invalid 'coefficient_type';"
                " only 'mean', 'median', or 'full' is allowed."
            )

        coeffs = DATA["point"][style]
        coeffs = coeffs[coeffs["model_id"] == coefficient_type].to_records(index=False)

        model_id, lam, mu, sd_total, sd_u, sd_mode = function_map[style](
            coeffs, magnitude, location
        )

    return model_id, lam, mu, sd_total, sd_u, sd_mode


# Create an ArgumentParser instance and add specific arguments to the parser
parser = argparse.ArgumentParser(
    description=_calc_params.__doc__, formatter_class=argparse.RawTextHelpFormatter
)
_add_magnitude(parser)
_add_location(parser)
_add_style(parser)
_add_coefficient_type(parser)


@_add_arguments(parser)
def main(**kwargs):

    try:
        result = _calc_params(**kwargs)

        names = ["model_id", "bc_param", "mean", "stdv_total", "stdv_within", "stdv_between"]

        print(
            f"     Displacement for magnitude {kwargs.get('magnitude')}, "
            f"location {kwargs.get('location')}, {kwargs.get('style')} faulting:"
        )
        for name, val in zip(names, result):
            print(f"     {name}: {val.squeeze()}")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
