from __future__ import annotations

from enum import Enum
from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
    KILONEWTON_PER_MEGANEWTON,
)


class StressUnit(UnitBase, Enum):
    """
    Stress units (force per area).

    Internal standard unit: ksi (kip/in²).
    Each member stores a multiplier to convert FROM this unit TO ksi.
    """

    # Instance attributes (for static checkers)
    symbol: str
    label: str
    _to_ksi: float

    PSI = ("psi", "pounds per square inch", 1.0 / POUNDS_PER_KIP)
    KSI = ("ksi", "kips per square inch", 1.0)
    PSF = ("psf", "pounds per square foot", 1.0 / POUNDS_PER_KIP / (INCHES_PER_FOOT * INCHES_PER_FOOT))
    KSF = ("ksf", "kips per square foot", 1.0 / (INCHES_PER_FOOT * INCHES_PER_FOOT))
    KPA = ("kPa", "kilopascals", 1.0 / (INCHES_PER_METER * INCHES_PER_METER) * KIPS_PER_KILONEWTON)
    MPA = ("MPa", "megapascals",
           1.0 / (INCHES_PER_METER * INCHES_PER_METER) * KIPS_PER_KILONEWTON * KILONEWTON_PER_MEGANEWTON)
    PA = ("Pa", "pascals",
          1.0 / (INCHES_PER_METER * INCHES_PER_METER) * KIPS_PER_KILONEWTON * NEWTONS_PER_KILONEWTON)

    def __new__(cls, symbol: str, label: str, to_ksi: float):
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label           # avoid Enum's reserved .name
        obj._to_ksi = float(to_ksi) # factor → ksi
        return obj

    # Stub for static checkers (matches 3-tuple signature)
    def __init__(self, symbol: str, label: str, to_ksi: float) -> None:
        pass

    @property
    def conversion_to_ksi(self) -> float:
        """Multiply a value in this unit by this factor to get ksi."""
        return self._to_ksi

    # Compatibility with code expecting a Unit-like API
    def get_conversion_factor(self) -> float:
        return self._to_ksi

    @classmethod
    def list(cls) -> list[StressUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> StressUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown stress unit symbol: {s!r}")


__all__ = ["StressUnit"]
