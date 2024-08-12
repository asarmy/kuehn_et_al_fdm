"""This module contains private functions for common arguments used for the command line interfacing."""

__all__ = [
    "_add_magnitude",
    "_add_location",
    "_add_style",
    "_add_coefficient_type",
    "_add_percentile",
    "_add_folded_flag",
    "_add_debug_flag",
    "_add_displacement",
    "_add_location_step",
    "_add_arguments",
]

import functools


def _add_magnitude(parser, nargs=None):
    """Add magntiude argument to an existing parser."""
    if nargs:
        parser.add_argument(
            "-m",
            "--magnitude",
            required=True,
            nargs=nargs,
            type=float,
            help="Earthquake moment magnitude.",
        )
    else:
        parser.add_argument(
            "-m",
            "--magnitude",
            required=True,
            type=float,
            help="Earthquake moment magnitude.",
        )


def _add_location(parser, nargs=None):
    """Add location argument to an existing parser."""
    if nargs:
        parser.add_argument(
            "-l",
            "--location_array",
            required=True,
            nargs=nargs,
            type=float,
            help="Normalized locations along rupture length, range [0, 1.0].",
        )

    else:
        parser.add_argument(
            "-l",
            "--location",
            required=True,
            type=float,
            help="Normalized location along rupture length, range [0, 1.0].",
        )


def _add_style(parser):
    """Add style argument to an existing parser."""
    parser.add_argument(
        "-s",
        "--style",
        required=True,
        type=str.lower,
        choices=("strike-slip", "reverse", "normal"),
        help="Style of faulting (case-insensitive).",
    )


def _add_coefficient_type(parser):
    """Add coefficient type argument to an existing parser."""
    parser.add_argument(
        "-ct",
        "--coefficient_type",
        default="median",
        type=str.lower,
        choices=("mean", "median", "full"),
        help=(
            "Run model with point estimates for coefficients ('mean' or 'median') or with full "
            "model coefficients ('full'); case-insensitive. Default is 'median'."
        ),
    )


def _add_percentile(parser):
    """Add percentile argument to an existing parser."""
    parser.add_argument(
        "-p",
        "--percentile",
        required=True,
        type=float,
        help="Aleatory quantile value. Use -1 for mean.",
    )


def _add_folded_flag(parser):
    """Add folded argument (boolean) to an existing parser, defaulting to True."""
    parser.add_argument(
        "--folded",
        dest="folded",
        action="store_true",
        help="Return results for the folded location. (Default.)",
    )
    parser.add_argument(
        "--unfolded",
        dest="folded",
        action="store_false",
        help="Return results for the unfolded location.",
    )
    parser.set_defaults(folded=True)


def _add_debug_flag(parser):
    """Add debug argument (boolean) to an existing parser."""
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Option to return DataFrame of interim calculations.",
        default=False,
    )


def _add_displacement(parser, nargs="+"):
    """Add displacement argument to an existing parser."""
    parser.add_argument(
        "-d",
        "--displacement_array",
        required=True,
        nargs=nargs,
        type=float,
        help="Test values of displacement in meters.",
    )


def _add_location_step(parser):
    """Add location step size argument to an existing parser."""
    parser.add_argument(
        "-ls",
        "--location_step",
        default=0.05,
        type=float,
        help="Profile location step interval. Default 0.05",
    )


def _add_arguments(parser):
    """Decorator function that takes an argument parser object."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            parsed_args = vars(parser.parse_args())
            kwargs.update(parsed_args)
            return func(**kwargs)

        return wrapper

    return decorator
