from __future__ import annotations

from enum import Enum
from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # only for type checkers; avoids runtime cycles
    from .length import Length
    from .force import Force
    from .force_per_length import ForcePerLength

class LengthUnit(UnitBase, Enum):
    """
    Length units.

    Internal standard unit: inch (in).
    Each member stores a multiplier to convert FROM this unit TO inches.
    """

    # Instance attributes for static checkers
    symbol: str
    label: str
    _to_in: float

    INCH = ("in", "inch", 1.0)
    FOOT = ("ft", "foot", INCHES_PER_FOOT)
    MILLIMETER = ("mm", "millimeter", INCHES_PER_METER / MILLIMETERS_PER_METER)
    CENTIMETER = ("cm", "centimeter", INCHES_PER_METER / CENTIMETERS_PER_METER)
    METER = ("m", "meter", INCHES_PER_METER)

    def __new__(cls, symbol: str, label: str, to_in: float):
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label  # avoid Enum's reserved .name
        obj._to_in = float(to_in)
        return obj

    # Stub for static checkers (matches 3-tuple)
    def __init__(self, symbol: str, label: str, to_in: float) -> None:
        pass

    # --- NEW: scalar constructors so 2 * FOOT, FOOT * 2, FOOT(2) create Length ---
    def __rmul__(self, other: float | int) -> "Length":
        if not isinstance(other, (int, float)):
            return NotImplemented
        from .length import Length  # lazy import to avoid circular import
        return Length(float(other), self)

    def __mul__(self, other: float | int) -> "Length":
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "Length":
        from .length import Length
        return Length(float(value), self)
    
    
    def __rtruediv__(self, other: "Force") -> "ForcePerLength":
        # (1*lb) / ft -> calls here if Force.__truediv__ returns NotImplemented
        from .force import Force
        if not isinstance(other, Force):
            return NotImplemented
        return other / self  # delegate to the Force override above

    @property
    def conversion_to_in(self) -> float:
        """Multiply a value in this unit by this factor to get inches."""
        return self._to_in

    # Compatibility with code expecting Unit-like API
    def get_conversion_factor(self) -> float:
        return self._to_in

    @classmethod
    def list(cls) -> list[LengthUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> LengthUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown length unit symbol: {s!r}")


__all__ = ["LengthUnit"]
