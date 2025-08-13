from __future__ import annotations

from enum import Enum
from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)


class LengthToThe4thUnit(UnitBase, Enum):
    """
    Units for length^4 (e.g., area moment of inertia).

    Internal standard unit: in⁴.
    Each member stores a multiplier to convert FROM this unit TO in⁴.
    """

    # Instance attributes for static checkers
    symbol: str
    label: str
    _to_in4: float

    INCHES_TO_THE_4TH = ("in⁴", "inch to the 4th", 1.0)
    FEET_TO_THE_4TH = ("ft⁴", "foot to the 4th", INCHES_PER_FOOT ** 4)
    MILLIMETERS_TO_THE_4TH = (
        "mm⁴",
        "millimeter to the 4th",
        (INCHES_PER_METER / MILLIMETERS_PER_METER) ** 4,
    )
    METERS_TO_THE_4TH = ("m⁴", "meter to the 4th", INCHES_PER_METER ** 4)
    CENTIMETERS_TO_THE_4TH = (
        "cm⁴",
        "centimeter to the 4th",
        (INCHES_PER_METER / CENTIMETERS_PER_METER) ** 4,
    )

    def __new__(cls, symbol: str, label: str, to_in4: float):
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label  # avoid Enum's reserved .name
        obj._to_in4 = float(to_in4)
        return obj

    # Stub for static checkers (matches 3-tuple)
    def __init__(self, symbol: str, label: str, to_in4: float) -> None:
        pass

    @property
    def conversion_to_in4(self) -> float:
        """Multiply a value in this unit by this factor to get in⁴."""
        return self._to_in4

    # Compatibility with code expecting a Unit-like API
    def get_conversion_factor(self) -> float:
        return self._to_in4

    @classmethod
    def list(cls) -> list[LengthToThe4thUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> LengthToThe4thUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown length⁴ unit symbol: {s!r}")


__all__ = ["LengthToThe4thUnit"]
