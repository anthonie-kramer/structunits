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
    from .area import Area


class AreaUnit(UnitBase, Enum):
    """
    Units for area (length^2) quantities.

    The internal standard unit is square inch (in²).
    Each member stores a conversion factor to convert FROM this unit TO in².
    
    This enum supports:
    - Scalar arithmetic: `100 * AreaUnit.SQUARE_FOOT` creates an Area
    - Unit decomposition: Can be used with stress calculations
    
    Examples
    --------
    >>> unit = AreaUnit.SQUARE_FOOT
    >>> unit.symbol
    'ft²'
    >>> unit.get_conversion_factor()
    144.0
    >>> area = 2 * unit  # Creates Area(2, AreaUnit.SQUARE_FOOT)
    >>> area.in2
    288.0
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
    SQUARE_INCH = ("in²", "square inch", 1.0)
    SQUARE_FOOT = ("ft²", "square foot", INCHES_PER_FOOT ** 2)
    SQUARE_MILLIMETER = (
        "mm²",
        "square millimeter",
        (INCHES_PER_METER / MILLIMETERS_PER_METER) ** 2,
    )
    SQUARE_CENTIMETER = (
        "cm²",
        "square centimeter",
        (INCHES_PER_METER / CENTIMETERS_PER_METER) ** 2,
    )
    SQUARE_METER = ("m²", "square meter", INCHES_PER_METER ** 2)

    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "AreaUnit":
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
        return f"AreaUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for Area creation ---
    def __rmul__(self, other: float | int) -> "Area":
        """Enable: scalar * AreaUnit -> Area."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        from .area import Area
        return Area(float(other), self)

    def __mul__(self, other: float | int) -> "Area":
        """Enable: AreaUnit * scalar -> Area."""
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "Area":
        """Enable: AreaUnit(scalar) -> Area."""
        from .area import Area
        return Area(float(value), self)

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (in²)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (in²)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "AreaUnit":
        """Get the standard unit for this unit type."""
        return cls.SQUARE_INCH

    @classmethod
    def list_all(cls) -> list["AreaUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "AreaUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching AreaUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown area unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    @classmethod
    def from_length_units(cls, length1_symbol: str, length2_symbol: str) -> "AreaUnit":
        """
        Create an AreaUnit from two length unit symbols.
        
        Args:
            length1_symbol: First length unit symbol (e.g., "ft")
            length2_symbol: Second length unit symbol (e.g., "ft")
            
        Returns:
            The corresponding AreaUnit
            
        Examples:
        --------
        >>> AreaUnit.from_length_units("ft", "ft")
        AreaUnit.SQUARE_FOOT
        >>> AreaUnit.from_length_units("m", "m")
        AreaUnit.SQUARE_METER
        """
        # Normalize symbols
        sym1 = length1_symbol.strip().lower()
        sym2 = length2_symbol.strip().lower()
        
        # Only support same-unit squares for now
        if sym1 != sym2:
            raise ValueError(f"Mixed area units not supported: {length1_symbol} × {length2_symbol}")
        
        # Map length symbols to area units
        length_to_area_map = {
            "in": cls.SQUARE_INCH,
            "ft": cls.SQUARE_FOOT,
            "mm": cls.SQUARE_MILLIMETER,
            "cm": cls.SQUARE_CENTIMETER,
            "m": cls.SQUARE_METER,
        }
        
        if sym1 in length_to_area_map:
            return length_to_area_map[sym1]
        
        available_symbols = list(length_to_area_map.keys())
        raise ValueError(
            f"Unknown length unit for area: {length1_symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["AreaUnit"]