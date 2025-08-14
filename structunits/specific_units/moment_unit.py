from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Final, overload

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
    from .moment import Moment
    from .force_unit import ForceUnit
    from .length_unit import LengthUnit


class MomentUnit(UnitBase, Enum):
    """
    Units for moment (force × distance) quantities.

    The internal standard unit is kip-inch (k-in).
    Each member stores a conversion factor to convert FROM this unit TO k-in.
    
    This enum supports:
    - Scalar arithmetic: `100 * MomentUnit.POUND_FOOT` creates a Moment
    - Unit division: `MomentUnit.KIP_FOOT / LengthUnit.FOOT` creates ForceUnit.KIP
    - Unit division: `MomentUnit.KIP_FOOT / ForceUnit.KIP` creates LengthUnit.FOOT
    
    Examples
    --------
    >>> unit = MomentUnit.POUND_FOOT
    >>> unit.symbol
    'lb-ft'
    >>> unit.get_conversion_factor()
    0.001
    >>> moment = 100 * unit  # Creates Moment(100, MomentUnit.POUND_FOOT)
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
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

    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "MomentUnit":
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
        return f"MomentUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for Moment creation ---
    def __rmul__(self, other: float | int) -> "Moment":
        """Enable: scalar * MomentUnit -> Moment."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        from .moment import Moment
        return Moment(float(other), self)

    def __mul__(self, other: float | int) -> "Moment":
        """Enable: MomentUnit * scalar -> Moment."""
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "Moment":
        """Enable: MomentUnit(scalar) -> Moment."""
        from .moment import Moment
        return Moment(float(value), self)

    # --- Unit arithmetic for decomposition ---
    @overload
    def __truediv__(self, other: "ForceUnit") -> "LengthUnit": ...
    @overload  
    def __truediv__(self, other: "LengthUnit") -> "ForceUnit": ...

    def __truediv__(self, other: "ForceUnit | LengthUnit") -> "LengthUnit | ForceUnit":
        """Enable: MomentUnit / ForceUnit -> LengthUnit, MomentUnit / LengthUnit -> ForceUnit."""
        from .force_unit import ForceUnit as FU
        from .length_unit import LengthUnit as LU

        if isinstance(other, FU):
            return self._divide_by_force_unit(other)
        elif isinstance(other, LU):
            return self._divide_by_length_unit(other)
        else:
            raise TypeError(f"Expected ForceUnit or LengthUnit, got {type(other).__name__}")

    def _divide_by_force_unit(self, force_unit: "ForceUnit") -> "LengthUnit":
        """Helper method for MomentUnit / ForceUnit -> LengthUnit."""
        from .force_unit import ForceUnit as FU
        from .length_unit import LengthUnit as LU

        # Common combinations for moment/force -> length
        _MOMENT_FORCE_COMBINATIONS: Final[dict[tuple[MomentUnit, FU], LU]] = {
            (MomentUnit.POUND_INCH, FU.POUND): LU.INCH,
            (MomentUnit.POUND_FOOT, FU.POUND): LU.FOOT,
            (MomentUnit.KIP_INCH, FU.KIP): LU.INCH,
            (MomentUnit.KIP_FOOT, FU.KIP): LU.FOOT,
            (MomentUnit.NEWTON_METER, FU.NEWTON): LU.METER,
            (MomentUnit.KILONEWTON_METER, FU.KILONEWTON): LU.METER,
            (MomentUnit.NEWTON_MILLIMETER, FU.NEWTON): LU.MILLIMETER,
            (MomentUnit.KILONEWTON_MILLIMETER, FU.KILONEWTON): LU.MILLIMETER,
            (MomentUnit.NEWTON_CENTIMETER, FU.NEWTON): LU.CENTIMETER,
            (MomentUnit.KILONEWTON_CENTIMETER, FU.KILONEWTON): LU.CENTIMETER,
        }

        combination = (self, force_unit)
        if combination in _MOMENT_FORCE_COMBINATIONS:
            return _MOMENT_FORCE_COMBINATIONS[combination]

        available_combinations = [f"{m.symbol}/{f.symbol}" for m, f in _MOMENT_FORCE_COMBINATIONS.keys()]
        raise TypeError(
            f"No moment/force unit mapping for {self.symbol} / {force_unit.symbol}. "
            f"Available combinations: {available_combinations}"
        )

    def _divide_by_length_unit(self, length_unit: "LengthUnit") -> "ForceUnit":
        """Helper method for MomentUnit / LengthUnit -> ForceUnit."""
        from .force_unit import ForceUnit as FU
        from .length_unit import LengthUnit as LU

        # Common combinations for moment/length -> force
        _MOMENT_LENGTH_COMBINATIONS: Final[dict[tuple[MomentUnit, LU], FU]] = {
            (MomentUnit.POUND_INCH, LU.INCH): FU.POUND,
            (MomentUnit.POUND_FOOT, LU.FOOT): FU.POUND,
            (MomentUnit.KIP_INCH, LU.INCH): FU.KIP,
            (MomentUnit.KIP_FOOT, LU.FOOT): FU.KIP,
            (MomentUnit.NEWTON_METER, LU.METER): FU.NEWTON,
            (MomentUnit.KILONEWTON_METER, LU.METER): FU.KILONEWTON,
            (MomentUnit.NEWTON_MILLIMETER, LU.MILLIMETER): FU.NEWTON,
            (MomentUnit.KILONEWTON_MILLIMETER, LU.MILLIMETER): FU.KILONEWTON,
            (MomentUnit.NEWTON_CENTIMETER, LU.CENTIMETER): FU.NEWTON,
            (MomentUnit.KILONEWTON_CENTIMETER, LU.CENTIMETER): FU.KILONEWTON,
        }

        combination = (self, length_unit)
        if combination in _MOMENT_LENGTH_COMBINATIONS:
            return _MOMENT_LENGTH_COMBINATIONS[combination]

        available_combinations = [f"{m.symbol}/{l.symbol}" for m, l in _MOMENT_LENGTH_COMBINATIONS.keys()]
        raise TypeError(
            f"No moment/length unit mapping for {self.symbol} / {length_unit.symbol}. "
            f"Available combinations: {available_combinations}"
        )

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (k-in)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (k-in)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "MomentUnit":
        """Get the standard unit for this unit type."""
        return cls.KIP_INCH

    @classmethod
    def list_all(cls) -> list["MomentUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "MomentUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching MomentUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown moment unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["MomentUnit"]
