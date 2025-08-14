from __future__ import annotations

from typing import Final

from structunits.result import Result
from structunits.flt import FLT
from structunits.unit import UnitBase

# Sentinel unit so we never pass None into Result.__init__
_UNITLESS_UNIT: Final[UnitBase] = UnitBase("1", "unitless")


class Unitless(Result):
    """
    Unitless quantity for dimensionless values.
    
    This class represents pure numbers without physical units,
    such as ratios, percentages, or other dimensionless quantities.
    
    Examples
    --------
    >>> ratio = Unitless(1.5)
    >>> ratio.value
    1.5
    >>> str(ratio)
    '1.5'
    """

    def __init__(self, value: float) -> None:
        super().__init__(FLT.UNITLESS, float(value), _UNITLESS_UNIT, _UNITLESS_UNIT)

    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return 1e-10

    @staticmethod
    def zero() -> "Unitless":
        """Create a zero unitless value."""
        return Unitless(0.0)

    def to_latex_string(self, display_unit: UnitBase | None = None) -> str:
        # Unitless: ignore any requested display unit
        return f"{self.value}"

    def convert_to(self, target_unit: UnitBase) -> float:
        # Only the sentinel "unitless unit" is valid
        if target_unit is _UNITLESS_UNIT:
            return self.value
        raise ValueError("Cannot convert unitless value to a unit")

    @classmethod
    def create_with_standard_units(cls, value: float) -> "Unitless":
        return cls(value)


__all__ = ["Unitless"]
