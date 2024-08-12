"""kuehn_et_al_fdm Quick Usage Guide

This module provides usage instructions for both CLI and module-level interactions with the
kuehn_et_al_fdm package.

Command-Line Interface (CLI)
----------------------------

To use the CLI, you can invoke the following commands:

- kea-stat_params : Calculate the predicted statistical distribution parameters.
- kea-displ_site : Calculate the predicted displacement in meters.
- kea-displ_avg : Calculate the median predicted average displacement in meters.
- kea-displ_profile : Calculate the predicted displacement profile in meters.
- kea-prob_exceed : Calculate the probability of exceedance.
- kea-prob_occur : Calculate the percentile rank of observations.

Example CLI Usage:

$ kea-stat_params --help

Module-Level Interface
----------------------

The following functions are available:
- _calc_params : Calculate the predicted statistical distribution parameters.
- calc_displ_site : Calculate the predicted displacement in meters.
- calc_displ_avg : Calculate the median predicted average displacement in meters.
- calc_displ_profile : Calculate the predicted displacement profile in meters.
- calc_prob_exceed : Calculate the probability of exceedance.
- calc_prob_occur : Calculate the percentile rank of observations.

Each function corresponds to a CLI command but can be invoked programmatically within Python.

To use the package at the module level, you can import and call the functions directly:

# Example for individual function
from kuehn_et_al_fdm import calc_displ_site
print(calc_displ_site.__doc__)

# Example for general package import
import kuehn_et_al_fdm as kea
print(kea.calc_displ_site.__doc__)

"""


def main():
    """Print the usage guide."""
    print(__doc__)
