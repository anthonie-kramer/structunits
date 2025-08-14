from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Final

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

if TYPE_CHECKING:
    from .force_per_length import ForcePerLength


class ForcePerLengthUnit(UnitBase, Enum):
    """
    Units for distributed loads (force per length).

    The internal standard unit is kip per inch (k/in).
    Each member stores a conversion factor to convert FROM this unit TO k/in.
    
    Examples
    --------
    >>> unit = ForcePerLengthUnit.POUND_PER_FOOT
    >>> unit.symbol
    'lb/ft'
    >>> round(unit.get_conversion_factor(), 6)
    1.3e-05
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
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

    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "ForcePerLengthUnit":
        obj = object.__new__(cls)
        obj._value_ = symbol
        obj.symbol = symbol
        obj.label = label
        obj._conversion_factor = float(conversion_factor)
        return obj

    def __init__(self, symbol: str, label: str, conversion_factor: float) -> None:
        """Initialize unit (stub for type checker compatibility)."""
        pass

    def __repr__(self) -> str:
        return f"ForcePerLengthUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for ForcePerLength creation ---
    def __rmul__(self, other: float | int) -> "ForcePerLength":
        """Enable: scalar * ForcePerLengthUnit -> ForcePerLength."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        from .force_per_length import ForcePerLength
        return ForcePerLength(float(other), self)

    def __mul__(self, other: float | int) -> "ForcePerLength":
        """Enable: ForcePerLengthUnit * scalar -> ForcePerLength."""
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "ForcePerLength":
        """Enable: ForcePerLengthUnit(scalar) -> ForcePerLength."""
        from .force_per_length import ForcePerLength
        return ForcePerLength(float(value), self)

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (k/in)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (k/in)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "ForcePerLengthUnit":
        """Get the standard unit for this unit type."""
        return cls.KIP_PER_INCH

    @classmethod
    def list_all(cls) -> list["ForcePerLengthUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "ForcePerLengthUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching ForcePerLengthUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown force-per-length unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["ForcePerLengthUnit"]
