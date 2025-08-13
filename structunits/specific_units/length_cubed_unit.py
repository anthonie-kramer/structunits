from __future__ import annotations

from enum import Enum
from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)


class LengthCubedUnit(UnitBase, Enum):
    """
    Volume units (length^3).

    Internal standard unit: cubic inch (in³).
    Each member stores a multiplier to convert FROM this unit TO in³.
    """

    # Instance attributes (declared for static checkers)
    symbol: str
    label: str
    _to_in3: float

    INCHES_CUBED = ("in³", "cubic inch", 1.0)
    FEET_CUBED = ("ft³", "cubic foot", INCHES_PER_FOOT ** 3)
    MILLIMETERS_CUBED = (
        "mm³",
        "cubic millimeter",
        (INCHES_PER_METER / MILLIMETERS_PER_METER) ** 3,
    )
    METERS_CUBED = ("m³", "cubic meter", INCHES_PER_METER ** 3)
    CENTIMETERS_CUBED = (
        "cm³",
        "cubic centimeter",
        (INCHES_PER_METER / CENTIMETERS_PER_METER) ** 3,
    )

    def __new__(cls, symbol: str, label: str, to_in3: float):
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label  # avoid Enum's reserved .name
        obj._to_in3 = float(to_in3)  # factor → in³
        return obj

    # Stub __init__ for static checkers (matches 3-tuple values)
    def __init__(self, symbol: str, label: str, to_in3: float) -> None:
        pass

    @property
    def conversion_to_in3(self) -> float:
        """Multiply a value in this unit by this factor to get in³."""
        return self._to_in3

    # Compatibility method for code that expects Unit-like API
    def get_conversion_factor(self) -> float:
        return self._to_in3

    @classmethod
    def list(cls) -> list[LengthCubedUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> LengthCubedUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown length^3 unit symbol: {s!r}")


__all__ = ["LengthCubedUnit"]
