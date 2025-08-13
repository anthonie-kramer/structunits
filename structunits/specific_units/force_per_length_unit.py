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


class ForcePerLengthUnit(UnitBase, Enum):
    """
    Distributed load units (force per length).

    Internal standard unit: kip per inch (k/in).
    Each member stores a multiplier to convert FROM this unit TO kips per inch.
    """

    # Instance attributes (declared for static checkers)
    symbol: str
    label: str
    _to_kip_per_in: float

    POUND_PER_INCH = ("lb/in", "pound per inch", 1.0 / POUNDS_PER_KIP)
    POUND_PER_FOOT = ("lb/ft", "pound per foot", 1.0 / POUNDS_PER_KIP / INCHES_PER_FOOT)
    KIP_PER_INCH = ("k/in", "kip per inch", 1.0)
    KIP_PER_FOOT = ("k/ft", "kip per foot", 1.0 / INCHES_PER_FOOT)

    NEWTON_PER_METER = (
        "N/m",
        "newton per meter",
        KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON / INCHES_PER_METER,
    )
    KILONEWTON_PER_METER = (
        "kN/m",
        "kilonewton per meter",
        KIPS_PER_KILONEWTON / INCHES_PER_METER,
    )

    NEWTON_PER_MILLIMETER = (
        "N/mm",
        "newton per millimeter",
        KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON / INCHES_PER_METER * MILLIMETERS_PER_METER,
    )
    KILONEWTON_PER_MILLIMETER = (
        "kN/mm",
        "kilonewton per millimeter",
        KIPS_PER_KILONEWTON / INCHES_PER_METER * MILLIMETERS_PER_METER,
    )

    NEWTON_PER_CENTIMETER = (
        "N/cm",
        "newton per centimeter",
        KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON / INCHES_PER_METER * CENTIMETERS_PER_METER,
    )
    KILONEWTON_PER_CENTIMETER = (
        "kN/cm",
        "kilonewton per centimeter",
        KIPS_PER_KILONEWTON / INCHES_PER_METER * CENTIMETERS_PER_METER,
    )

    # Enum construction: set attributes in __new__
    def __new__(cls, symbol: str, label: str, to_kip_per_in: float):
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label  # avoid Enum's reserved .name
        obj._to_kip_per_in = float(to_kip_per_in)
        return obj

    # Stub __init__ only to satisfy static checkers for 3-tuple values
    def __init__(self, symbol: str, label: str, to_kip_per_in: float) -> None:
        pass

    @property
    def conversion_to_kip_per_in(self) -> float:
        """Multiply a value in this unit by this factor to get kips/inch."""
        return self._to_kip_per_in

    # Compatibility with code that expects Unit-like API
    def get_conversion_factor(self) -> float:
        return self._to_kip_per_in

    @classmethod
    def list(cls) -> list[ForcePerLengthUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> ForcePerLengthUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown force-per-length unit symbol: {s!r}")


__all__ = ["ForcePerLengthUnit"]
