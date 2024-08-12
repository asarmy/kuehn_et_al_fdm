"""This module contains various private helper functions."""

import numpy as np
import warnings

# Define recommended magnitude ranges
MAG_RANGES = {"strike-slip": [6, 8], "reverse": [5, 8], "normal": [6, 8]}


def _check_type(param, param_name, *expected_types, msg=None):
    """Check that the variable is of the specified type."""
    if len(expected_types) == 1 and isinstance(expected_types[0], (tuple, list)):
        expected_types = tuple(expected_types[0])

    if not isinstance(param, expected_types):
        expected_types_names = ", ".join(t.__name__ for t in expected_types)
        error_message = (
            f"{param_name} should be of type ({expected_types_names}). "
            "Received type: {type(param).__name__}."
        )
        if msg:
            error_message += f"\n{msg}"
        raise TypeError(error_message)


def _check_location_range(location):
    """Check that the location is within the allowable range."""
    min_val, max_val = 0, 1
    location = np.atleast_1d(location)

    if not np.all((location >= min_val) & (location <= max_val)):
        raise ValueError(
            "One or more location values are not within the range " f"[{min_val}, {max_val}]."
        )


def _check_magnitude_range(magnitude, style, ranges_dict=MAG_RANGES):
    """Check that the magnitude is within the allowable range for the style."""
    style = style.lower()
    min_val, max_val = MAG_RANGES[style]
    magnitude = np.atleast_1d(magnitude)

    if not np.all((magnitude >= min_val) & (magnitude <= max_val)):
        warning_message = (
            "\n***One or more magnitudes are not within the recommended range for "
            f"{style} faulting, which is [{min_val}, {max_val}]."
        )
        warnings.warn(warning_message, UserWarning)
