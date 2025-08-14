from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, Final

from structunits.constants import (
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
)
from structunits.unit import UnitBase

if TYPE_CHECKING:
    from .length_unit import LengthUnit
    from .force_per_length_unit import ForcePerLengthUnit
    from .moment_unit import MomentUnit
    from .force import Force


@unique
class ForceUnit(UnitBase, Enum):
    """
    Units for force quantities.
    
    The internal standard unit is kip.
    Each member stores a conversion factor to convert FROM this unit TO kip.
    
    This enum also supports:
    - Scalar arithmetic: `2 * ForceUnit.KIP` creates a Force of 2 kips
    - Unit arithmetic: `ForceUnit.KIP / LengthUnit.INCH` creates ForcePerLengthUnit
    - Unit arithmetic: `ForceUnit.KIP * LengthUnit.INCH` creates MomentUnit
    
    Examples
    --------
    >>> unit = ForceUnit.POUND
    >>> unit.symbol
    'lb'
    >>> unit.get_conversion_factor()
    0.001
    >>> force = 1000 * unit  # Creates Force(1000, ForceUnit.POUND)
    >>> force.kip
    1.0
    >>> moment_unit = unit * LengthUnit.FOOT  # Creates MomentUnit.POUND_FOOT
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
    POUND = ("lb", "pound", 1.0 / POUNDS_PER_KIP)
    KIP = ("kip", "kip", 1.0)
    NEWTON = ("N", "newton", KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON)
    KILONEWTON = ("kN", "kilonewton", KIPS_PER_KILONEWTON)
    
    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "ForceUnit":
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
        return f"ForceUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for Force creation ---
    def __rmul__(self, other: float | int) -> "Force":
        """Enable: scalar * ForceUnit -> Force."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        from structunits.specific_units.force import Force
        return Force(float(other), self)

    def __mul__(self, other: float | int | "LengthUnit") -> "Force | MomentUnit":
        """Enable: ForceUnit * scalar -> Force, ForceUnit * LengthUnit -> MomentUnit."""
        if isinstance(other, (int, float)):
            return self.__rmul__(other)
        
        # ForceUnit * LengthUnit -> MomentUnit
        from .length_unit import LengthUnit as LU
        if isinstance(other, LU):
            return self._multiply_by_length_unit(other)
            
        return NotImplemented

    def __call__(self, value: float | int) -> "Force":
        """Enable: ForceUnit(scalar) -> Force."""
        from structunits.specific_units.force import Force
        return Force(float(value), self)
        
    # --- Unit arithmetic: ForceUnit / LengthUnit -> ForcePerLengthUnit ---
    def __truediv__(self, other: "LengthUnit") -> "ForcePerLengthUnit":
        """Enable: ForceUnit / LengthUnit -> ForcePerLengthUnit."""
        from .length_unit import LengthUnit as LU
        from .force_per_length_unit import ForcePerLengthUnit as FPLU

        if not isinstance(other, LU):
            raise TypeError(f"Expected LengthUnit, got {type(other).__name__}")

        # Common unit combinations for division
        _DIVISION_COMBINATIONS: Final[dict[tuple[ForceUnit, LU], FPLU]] = {
            (ForceUnit.POUND, LU.INCH): FPLU.POUND_PER_INCH,
            (ForceUnit.POUND, LU.FOOT): FPLU.POUND_PER_FOOT,
            (ForceUnit.KIP, LU.INCH): FPLU.KIP_PER_INCH,
            (ForceUnit.KIP, LU.FOOT): FPLU.KIP_PER_FOOT,
            (ForceUnit.NEWTON, LU.METER): FPLU.NEWTON_PER_METER,
            (ForceUnit.KILONEWTON, LU.METER): FPLU.KILONEWTON_PER_METER,
            (ForceUnit.NEWTON, LU.MILLIMETER): FPLU.NEWTON_PER_MILLIMETER,
            (ForceUnit.KILONEWTON, LU.MILLIMETER): FPLU.KILONEWTON_PER_MILLIMETER,
            (ForceUnit.NEWTON, LU.CENTIMETER): FPLU.NEWTON_PER_CENTIMETER,
            (ForceUnit.KILONEWTON, LU.CENTIMETER): FPLU.KILONEWTON_PER_CENTIMETER,
        }

        combination = (self, other)
        if combination in _DIVISION_COMBINATIONS:
            return _DIVISION_COMBINATIONS[combination]

        available_combinations = [f"{f.symbol}/{l.symbol}" for f, l in _DIVISION_COMBINATIONS.keys()]
        raise TypeError(
            f"No force/length unit mapping for {self.symbol} / {other.symbol}. "
            f"Available combinations: {available_combinations}"
        )

    def _multiply_by_length_unit(self, length_unit: "LengthUnit") -> "MomentUnit":
        """Helper method for ForceUnit * LengthUnit -> MomentUnit."""
        from .length_unit import LengthUnit as LU
        from .moment_unit import MomentUnit as MU

        # Common unit combinations for multiplication
        _MULTIPLICATION_COMBINATIONS: Final[dict[tuple[ForceUnit, LU], MU]] = {
            (ForceUnit.POUND, LU.INCH): MU.POUND_INCH,
            (ForceUnit.POUND, LU.FOOT): MU.POUND_FOOT,
            (ForceUnit.KIP, LU.INCH): MU.KIP_INCH,
            (ForceUnit.KIP, LU.FOOT): MU.KIP_FOOT,
            (ForceUnit.NEWTON, LU.METER): MU.NEWTON_METER,
            (ForceUnit.KILONEWTON, LU.METER): MU.KILONEWTON_METER,
            (ForceUnit.NEWTON, LU.MILLIMETER): MU.NEWTON_MILLIMETER,
            (ForceUnit.KILONEWTON, LU.MILLIMETER): MU.KILONEWTON_MILLIMETER,
            (ForceUnit.NEWTON, LU.CENTIMETER): MU.NEWTON_CENTIMETER,
            (ForceUnit.KILONEWTON, LU.CENTIMETER): MU.KILONEWTON_CENTIMETER,
        }

        combination = (self, length_unit)
        if combination in _MULTIPLICATION_COMBINATIONS:
            return _MULTIPLICATION_COMBINATIONS[combination]

        available_combinations = [f"{f.symbol}*{l.symbol}" for f, l in _MULTIPLICATION_COMBINATIONS.keys()]
        raise TypeError(
            f"No force*length unit mapping for {self.symbol} * {length_unit.symbol}. "
            f"Available combinations: {available_combinations}"
        )

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (kip)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (kip)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "ForceUnit":
        """Get the standard unit for this unit type."""
        return cls.KIP

    @classmethod
    def list_all(cls) -> list["ForceUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "ForceUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching ForceUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown force unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["ForceUnit"]
