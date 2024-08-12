"""This module contains various private helper functions used to calculate the model predictions in transformed units."""

# Python imports
import numpy as np
from scipy import stats


def _calc_analytic_mean(bc_parameter, mean, stdv):
    """
    Helper function to calculate the back-transformed predicted mean displacement in meters
    using the model parameters.

    This analytical solution is from https://robjhyndman.com/hyndsight/backtransforming/

    Parameters
    ----------
    bc_parameter : ArrayLike
        Box-Cox transformation parameter "lambda".

    mean : ArrayLike
        Mean displacement in transformed units.

    stdv : ArrayLike
        Standard deviation of displacement in transformed units.

    Returns
    -------
    float
        Predicted mean displacement in meters.
    """
    return (np.power(bc_parameter * mean + 1, 1 / bc_parameter)) * (
        1 + (np.power(stdv, 2) * (1 - bc_parameter)) / (2 * np.power(bc_parameter * mean + 1, 2))
    )


def _calc_transformed_displ(bc_parameter, mean, stdv, quantile):
    """
    Helper function to calculate predicted displacement in transformed units
    using the model parameters.

    Parameters
    ----------
    bc_parameter : int or float or numpy.ndarray with a single element
        Box-Cox transformation parameter "lambda".

    mean : int or float or numpy.ndarray with a single element
        Mean displacement in transformed units.

    stdv : int or float or numpy.ndarray with a single element
        Standard deviation of displacement in transformed units.

    quantile : int or float or numpy.ndarray with a single element
        Aleatory quantile value. Use -1 for mean.

    Returns
    -------
    displ_bc : int or float or numpy.ndarray with a single element
        Predicted displacement in transformed units.
    """
    if quantile == -1:
        # Compute the back-transformed mean
        displ_meters = _calc_analytic_mean(bc_parameter, mean, stdv)
        displ_bc = (np.power(displ_meters, bc_parameter) - 1) / bc_parameter

    else:
        displ_bc = stats.norm.ppf(quantile, loc=mean, scale=stdv)

    return displ_bc
