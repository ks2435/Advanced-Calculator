from __future__ import annotations

import math

from .exceptions import ValidationError


def parse_number(s: str) -> float:
    try:
        x = float(s)
    except ValueError as e:
        raise ValidationError(f"Invalid number: {s}") from e
    if math.isnan(x) or math.isinf(x):
        raise ValidationError("NaN/Infinity is not allowed.")
    return x


def validate_range(x: float, max_abs: float) -> float:
    if abs(x) > max_abs:
        raise ValidationError(f"Input out of range. Max allowed absolute value is {max_abs}.")
    return x