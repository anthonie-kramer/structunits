from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Final

from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)

if TYPE_CHECKING:
    from .length_to_the_4th import LengthToThe4th


class LengthToThe4thUnit(UnitBase, Enum):
    """
    Units for length^4 quantities (e.g., area moment of inertia).

    The internal standard unit is inch^4 (in⁴).
    Each member stores a conversion factor to convert FROM this unit TO in⁴.
    
    Examples
    --------
    >>> unit = LengthToThe4thUnit.FEET_TO_THE_4TH
    >>> unit.symbol
    'ft⁴'
    >>> unit.get_conversion_factor()
    20736.0
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
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

    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "LengthToThe4thUnit":
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
        return f"LengthToThe4thUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for LengthToThe4th creation ---
    def __rmul__(self, other: float | int) -> "LengthToThe4th":
        """Enable: scalar * LengthToThe4thUnit -> LengthToThe4th."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        from .length_to_the_4th import LengthToThe4th
        return LengthToThe4th(float(other), self)

    def __mul__(self, other: float | int) -> "LengthToThe4th":
        """Enable: LengthToThe4thUnit * scalar -> LengthToThe4th."""
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "LengthToThe4th":
        """Enable: LengthToThe4thUnit(scalar) -> LengthToThe4th."""
        from .length_to_the_4th import LengthToThe4th
        return LengthToThe4th(float(value), self)

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (in⁴)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (in⁴)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "LengthToThe4thUnit":
        """Get the standard unit for this unit type."""
        return cls.INCHES_TO_THE_4TH

    @classmethod
    def list_all(cls) -> list["LengthToThe4thUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "LengthToThe4thUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching LengthToThe4thUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown length⁴ unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["LengthToThe4thUnit"]
