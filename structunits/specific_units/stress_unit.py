from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Final

from structunits.unit import UnitBase
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
    KILONEWTON_PER_MEGANEWTON,
)

if TYPE_CHECKING:
    from .stress import Stress
    from .force_unit import ForceUnit


class StressUnit(UnitBase, Enum):
    """
    Units for stress (force per area) quantities.

    The internal standard unit is ksi (kip/in²).
    Each member stores a conversion factor to convert FROM this unit TO ksi.
    
    This enum supports:
    - Scalar arithmetic: `50 * StressUnit.KSI` creates a Stress
    - Unit creation: Can be created from ForceUnit / AreaUnit combinations
    
    Examples
    --------
    >>> unit = StressUnit.PSI
    >>> unit.symbol
    'psi'
    >>> unit.get_conversion_factor()
    0.001
    >>> stress = 1000 * unit  # Creates Stress(1000, StressUnit.PSI)
    >>> stress.ksi
    1.0
    """

    # Instance attributes for static type checkers
    symbol: str
    label: str
    _conversion_factor: float

    # Unit definitions: (symbol, label, factor_to_standard_unit)
    PSI = ("psi", "pounds per square inch", 1.0 / POUNDS_PER_KIP)
    KSI = ("ksi", "kips per square inch", 1.0)
    PSF = ("psf", "pounds per square foot", 1.0 / POUNDS_PER_KIP / (INCHES_PER_FOOT * INCHES_PER_FOOT))
    KSF = ("ksf", "kips per square foot", 1.0 / (INCHES_PER_FOOT * INCHES_PER_FOOT))
    KPA = ("kPa", "kilopascals", 1.0 / (INCHES_PER_METER * INCHES_PER_METER) * KIPS_PER_KILONEWTON)
    MPA = ("MPa", "megapascals",
           1.0 / (INCHES_PER_METER * INCHES_PER_METER) * KIPS_PER_KILONEWTON * KILONEWTON_PER_MEGANEWTON)
    PA = ("Pa", "pascals",
          1.0 / (INCHES_PER_METER * INCHES_PER_METER) * KIPS_PER_KILONEWTON * NEWTONS_PER_KILONEWTON)

    def __new__(cls, symbol: str, label: str, conversion_factor: float) -> "StressUnit":
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
        return f"StressUnit.{self.name}({self.symbol!r})"

    # --- Scalar arithmetic for Stress creation ---
    def __rmul__(self, other: float | int) -> "Stress":
        """Enable: scalar * StressUnit -> Stress."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        from .stress import Stress
        return Stress(float(other), self)

    def __mul__(self, other: float | int) -> "Stress":
        """Enable: StressUnit * scalar -> Stress."""
        return self.__rmul__(other)

    def __call__(self, value: float | int) -> "Stress":
        """Enable: StressUnit(scalar) -> Stress."""
        from .stress import Stress
        return Stress(float(value), self)

    @classmethod
    def from_force_and_area(cls, force_unit: "ForceUnit", area_symbol: str) -> "StressUnit":
        """
        Create a StressUnit from a ForceUnit and area specification.
        
        Args:
            force_unit: The force unit (e.g., ForceUnit.KIP)
            area_symbol: Area specification (e.g., "in²", "ft²")
            
        Returns:
            The corresponding StressUnit
            
        Examples
        --------
        >>> StressUnit.from_force_and_area(ForceUnit.KIP, "in²")
        StressUnit.KSI
        >>> StressUnit.from_force_and_area(ForceUnit.POUND, "in²")
        StressUnit.PSI
        """
        from .force_unit import ForceUnit as FU

        # Common force/area combinations
        _FORCE_AREA_COMBINATIONS: Final[dict[tuple[FU, str], StressUnit]] = {
            (FU.POUND, "in²"): cls.PSI,
            (FU.KIP, "in²"): cls.KSI,
            (FU.POUND, "ft²"): cls.PSF,
            (FU.KIP, "ft²"): cls.KSF,
            (FU.NEWTON, "m²"): cls.PA,
            (FU.KILONEWTON, "m²"): cls.KPA,
        }

        combination = (force_unit, area_symbol.lower())
        if combination in _FORCE_AREA_COMBINATIONS:
            return _FORCE_AREA_COMBINATIONS[combination]

        available_combinations = [f"{f.symbol}/{a}" for f, a in _FORCE_AREA_COMBINATIONS.keys()]
        raise ValueError(
            f"No stress unit mapping for {force_unit.symbol}/{area_symbol}. "
            f"Available combinations: {available_combinations}"
        )

    def get_conversion_factor(self) -> float:
        """Get the conversion factor to the standard unit (ksi)."""
        return self._conversion_factor

    @property
    def conversion_factor(self) -> float:
        """Conversion factor to standard unit (ksi)."""
        return self._conversion_factor

    @classmethod
    def get_standard_unit(cls) -> "StressUnit":
        """Get the standard unit for this unit type."""
        return cls.KSI

    @classmethod
    def list_all(cls) -> list["StressUnit"]:
        """Get all available units in this enum."""
        return list(cls)

    @classmethod
    def from_symbol(cls, symbol: str) -> "StressUnit":
        """
        Find unit by symbol (case-insensitive).
        
        Args:
            symbol: The unit symbol to search for
            
        Returns:
            The matching StressUnit
            
        Raises:
            ValueError: If the symbol is not found
        """
        normalized_symbol = symbol.strip().lower()
        for unit in cls:
            if unit.symbol.lower() == normalized_symbol:
                return unit
        
        available_symbols = [u.symbol for u in cls]
        raise ValueError(
            f"Unknown stress unit symbol: {symbol!r}. "
            f"Available symbols: {available_symbols}"
        )

    # Legacy compatibility
    list = list_all


__all__ = ["StressUnit"]
