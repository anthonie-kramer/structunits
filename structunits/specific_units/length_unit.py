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
    from .length import Length
    from .force import Force
    from .force_per_length import ForcePerLength
    from .moment import Moment
    from .area_unit import AreaUnit


class LengthUnit(UnitBase, Enum):
    """
    Units for length quantities.

    The internal standard unit is inch (in).
    Each member stores a conversion factor to convert FROM this unit TO inches.
    
    This enum also supports scalar arithmetic for creating Length objects:
    - `2 * LengthUnit.FOOT` creates a Length of 2 feet
    - `LengthUnit.METER(5)` creates a Length of 5 meters
    - `LengthUnit.FOOT * LengthUnit.FOOT` creates AreaUnit.SQUARE_FOOT
    - `ForceUnit.KIP * LengthUnit.INCH` creates MomentUnit.KIP_INCH
    
    Examples
    --------
    >>> unit = LengthUnit.FOOT
    >>> unit.symbol
    'ft'
    >>> unit.get_conversion_factor()
    12.0
    >>> length = 2 * unit  # Creates Length(2, LengthUnit.FOOT)
    >>> length.inch
    24.0
    >>> area_unit = unit * unit  # Creates AreaUnit.SQUARE_FOOT
    >>> area_unit.symbol
    'ft²'
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
    INCH = ("in", "inch", 1.0)
    FOOT = ("ft", "foot", INCHES_PER_FOOT)
    MILLIMETER = ("mm", "millimeter", INCHES_PER_METER / MILLIMETERS_PER_METER)
    CENTIMETER = ("cm", "centimeter", INCHES_PER_METER / CENTIMETERS_PER_METER)
    METER = ("m", "meter", INCHES_PER_METER)

    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "LengthUnit":
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
        return f"LengthUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for Length creation ---
    def __rmul__(self, other: float | int | "Force") -> "Length | Moment":
        """Enable: scalar * LengthUnit -> Length, Force * LengthUnit -> Moment."""
        if isinstance(other, (int, float)):
            from .length import Length
            return Length(float(other), self)
        
        # Force * LengthUnit -> Moment
        from .force import Force
        if isinstance(other, Force):
            from .moment import Moment
            from .force_unit import ForceUnit
            from .moment_unit import MomentUnit
            
            # Get the force unit from the Force object's display unit
            force_display_unit = other.display_unit
            force_unit = force_display_unit if isinstance(force_display_unit, ForceUnit) else ForceUnit.KIP
            
            # Create the moment unit from force unit * length unit
            # We need to explicitly call the helper method to get the right type
            moment_unit = force_unit._multiply_by_length_unit(self)
            
            # Get the force value in the appropriate unit and create moment
            force_value = other.to_value(force_unit)
            
            return Moment(force_value, moment_unit)
            
        return NotImplemented

    def __mul__(self, other: float | int | "LengthUnit") -> "Length | Moment | AreaUnit":
        """Enable: LengthUnit * scalar -> Length, LengthUnit * LengthUnit -> AreaUnit."""
        if isinstance(other, (int, float)):
            # This calls __rmul__ which can return Length, but we need to be explicit about the type
            from .length import Length
            return Length(float(other), self)
        
        # LengthUnit * LengthUnit -> AreaUnit
        if isinstance(other, LengthUnit):
            return self._multiply_by_length_unit(other)
            
        return NotImplemented

    def __call__(self, value: float | int) -> "Length":
        """Enable: LengthUnit(scalar) -> Length."""
        from .length import Length
        return Length(float(value), self)
    
    def __rtruediv__(self, other: "Force") -> "ForcePerLength":
        """Enable: Force / LengthUnit -> ForcePerLength."""
        from .force import Force
        if not isinstance(other, Force):
            return NotImplemented
        return other / self

    def _multiply_by_length_unit(self, other: "LengthUnit") -> "AreaUnit":
        """Helper method for LengthUnit * LengthUnit -> AreaUnit."""
        from .area_unit import AreaUnit
        
        # For now, only support same-unit multiplication (e.g., ft * ft = ft²)
        if self == other:
            # Map length units to their corresponding area units
            length_to_area_map: Final[dict[LengthUnit, AreaUnit]] = {
                LengthUnit.INCH: AreaUnit.SQUARE_INCH,
                LengthUnit.FOOT: AreaUnit.SQUARE_FOOT,
                LengthUnit.MILLIMETER: AreaUnit.SQUARE_MILLIMETER,
                LengthUnit.CENTIMETER: AreaUnit.SQUARE_CENTIMETER,
                LengthUnit.METER: AreaUnit.SQUARE_METER,
            }
            
            if self in length_to_area_map:
                return length_to_area_map[self]
        
        # For mixed units or unsupported combinations, raise an error
        supported_combinations = ["in*in", "ft*ft", "mm*mm", "cm*cm", "m*m"]
        raise TypeError(
            f"Unsupported length unit multiplication: {self.symbol} * {other.symbol}. "
            f"Supported combinations: {supported_combinations}"
        )

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (inches)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (inches)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "LengthUnit":
        """Get the standard unit for this unit type."""
        return cls.INCH

    @classmethod
    def list_all(cls) -> list["LengthUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "LengthUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching LengthUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown length unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["LengthUnit"]
