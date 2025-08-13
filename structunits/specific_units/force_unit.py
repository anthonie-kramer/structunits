from __future__ import annotations

from enum import Enum
from typing import Final, List, TYPE_CHECKING

from structunits.constants import (
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
)
from structunits.unit import UnitBase

if TYPE_CHECKING:
    # Only for type checking; avoids runtime cycles
    from .length_unit import LengthUnit
    from .force_per_length_unit import ForcePerLengthUnit
    from .force import Force

class ForceUnit(UnitBase, Enum):
    """
    Force units. Internal standard: kip.
    Each member stores a multiplier to convert FROM this unit TO kip.
    """

    # Tell the type checker these instance attributes exist
    symbol: str
    label: str
    _to_kip: float

    POUND = ("lb", "pound", 1.0 / POUNDS_PER_KIP)
    KIP = ("kip", "kip", 1.0)
    NEWTON = ("N", "newton", KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON)
    KILONEWTON = ("kN", "kilonewton", KIPS_PER_KILONEWTON)

    # ---- Enum construction ----
    def __new__(cls, symbol: str, label: str, to_kip: float):
        obj = object.__new__(cls)
        obj._value_ = symbol          # enum's value
        obj.symbol = symbol           # UnitBase field
        obj.label = label             # UnitBase field (avoid Enum's reserved .name)
        obj._to_kip = float(to_kip)   # instance attribute declared above
        return obj

    # Stub __init__ only to satisfy static checkers for the 3-tuple signature
    def __init__(self, symbol: str, label: str, to_kip: float) -> None:
        pass

        # --- NEW: scalar constructors ---
    def __rmul__(self, other: float | int) -> "Force":
        # enables: 1 * ForceUnit.KIP
        if not isinstance(other, (int, float)):
            return NotImplemented
        from structunits.specific_units.force import Force  # lazy import avoids cycles
        return Force(float(other), self)

    def __mul__(self, other: float | int) -> "Force":
        # enables: ForceUnit.KIP * 1
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "Force":
        # enables: ForceUnit.KIP(1)
        from structunits.specific_units.force import Force
        return Force(float(value), self)
    
     # --- NEW: unit arithmetic: ForceUnit / LengthUnit -> ForcePerLengthUnit
    def __truediv__(self, other: "LengthUnit") -> "ForcePerLengthUnit":
        # Lazy import to avoid import cycles at runtime
        from .length_unit import LengthUnit as LU
        from .force_per_length_unit import ForcePerLengthUnit as FPLU

        if not isinstance(other, LU):
            raise TypeError(f"Expected LengthUnit on right-hand side, got {type(other).__name__}")

        # Common mappings (imperial and SI)
        if self is ForceUnit.POUND and other is LU.INCH:
            return FPLU.POUND_PER_INCH
        if self is ForceUnit.POUND and other is LU.FOOT:
            return FPLU.POUND_PER_FOOT

        if self is ForceUnit.KIP and other is LU.INCH:
            return FPLU.KIP_PER_INCH
        if self is ForceUnit.KIP and other is LU.FOOT:
            return FPLU.KIP_PER_FOOT

        if self is ForceUnit.NEWTON and other is LU.METER:
            return FPLU.NEWTON_PER_METER
        if self is ForceUnit.KILONEWTON and other is LU.METER:
            return FPLU.KILONEWTON_PER_METER

        if self is ForceUnit.NEWTON and other is LU.MILLIMETER:
            return FPLU.NEWTON_PER_MILLIMETER
        if self is ForceUnit.KILONEWTON and other is LU.MILLIMETER:
            return FPLU.KILONEWTON_PER_MILLIMETER

        if self is ForceUnit.NEWTON and other is LU.CENTIMETER:
            return FPLU.NEWTON_PER_CENTIMETER
        if self is ForceUnit.KILONEWTON and other is LU.CENTIMETER:
            return FPLU.KILONEWTON_PER_CENTIMETER

        raise TypeError(f"No force/length unit mapping for {self} / {other}")

    # ---- API ----
    @property
    def conversion_to_kip(self) -> float:
        """Multiply a value in this unit by this factor to get kips."""
        return self._to_kip

    def get_conversion_factor(self) -> float:
        """Compatibility with Unit-like API."""
        return self._to_kip

    @classmethod
    def list(cls) -> list[ForceUnit]:
        return list(cls)

    @classmethod
    def from_symbol(cls, s: str) -> ForceUnit:
        s = s.strip().lower()
        for u in cls:
            if u.symbol.lower() == s:
                return u
        raise ValueError(f"Unknown force unit symbol: {s!r}")


__all__ = ["ForceUnit"]
