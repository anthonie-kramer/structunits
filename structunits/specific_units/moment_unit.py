from __future__ import annotations

from enum import Enum
from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
)


class MomentUnit(UnitBase, Enum):
    """
    Moment (force × distance) units.

    Internal standard unit: kip·inch (kip-in).
    Each member stores a multiplier to convert FROM this unit TO kip-in.
    """

    # Instance attributes (declared for static checkers)
    symbol: str
    label: str
    _to_kip_in: float

    POUND_INCH = ("lb-in", "pound-inch", 1.0 / POUNDS_PER_KIP)
    POUND_FOOT = ("lb-ft", "pound-foot", (1.0 / POUNDS_PER_KIP) * INCHES_PER_FOOT)
    KIP_INCH = ("k-in", "kip-inch", 1.0)
    KIP_FOOT = ("k-ft", "kip-foot", INCHES_PER_FOOT)

    NEWTON_METER = (
        "N-m",
        "newton-meter",
        KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON * INCHES_PER_METER,
    )
    KILONEWTON_METER = (
        "kN-m",
        "kilonewton-meter",
        KIPS_PER_KILONEWTON * INCHES_PER_METER,
    )
    KILONEWTON_MILLIMETER = (
        "kN-mm",
        "kilonewton-millimeter",
        KIPS_PER_KILONEWTON * INCHES_PER_METER / MILLIMETERS_PER_METER,
    )
    NEWTON_MILLIMETER = (
        "N-mm",
        "newton-millimeter",
        KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON * INCHES_PER_METER / MILLIMETERS_PER_METER,
    )
    KILONEWTON_CENTIMETER = (
        "kN-cm",
        "kilonewton-centimeter",
        KIPS_PER_KILONEWTON * INCHES_PER_METER / CENTIMETERS_PER_METER,
    )
    NEWTON_CENTIMETER = (
        "N-cm",
        "newton-centimeter",
        KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON * INCHES_PER_METER / CENTIMETERS_PER_METER,
    )

    # Enum construction: set attributes in __new__, not __init__
    def __new__(cls, symbol: str, label: str, to_kip_in: float):
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label  # avoid Enum's reserved .name
        obj._to_kip_in = float(to_kip_in)
        return obj

    # Stub __init__ to satisfy static checkers (matches 3-tuple signature)
    def __init__(self, symbol: str, label: str, to_kip_in: float) -> None:
        pass

    @property
    def conversion_to_kip_in(self) -> float:
        """Multiply a value in this unit by this factor to get kip-in."""
        return self._to_kip_in

    # Compatibility with code expecting a Unit-like API
    def get_conversion_factor(self) -> float:
        return self._to_kip_in

    @classmethod
    def list(cls) -> list[MomentUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> MomentUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown moment unit symbol: {s!r}")


__all__ = ["MomentUnit"]
