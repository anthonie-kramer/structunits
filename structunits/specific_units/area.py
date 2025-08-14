from __future__ import annotations

from typing import Final, Mapping, ClassVar, overload, Literal, Self, TYPE_CHECKING
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.area_unit import AreaUnit as AU
from structunits.unit import UnitBase
from structunits.utilities import Utilities

if TYPE_CHECKING:
    from structunits.specific_units.unitless import Unitless


class Area(Result):
    """
    An area value with unit handling (length^2).
    
    Standard unit: square inch (in²).
    
    Examples
    --------
    >>> area = Area.from_ft2(1.0)
    >>> area.in2
    144.0
    >>> area = Area.from_m2(1.0)
    >>> round(area.ft2, 3)
    10.764
    """

    _EQ_TOL: Final[float] = 1e-3  # in²

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[AU, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in AU
    })
    _FROM_STD: ClassVar[Mapping[AU, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in AU
    })

    def __init__(self, value: float, unit: AU) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.AREA, std_value, unit, unit)

    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> AU:
        return AU.SQUARE_INCH

    @staticmethod
    def zero() -> "Area":
        """Create a zero area value."""
        return Area(0.0, AU.SQUARE_INCH)

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_in2(cls, value: float) -> Self:
        return cls(value, AU.SQUARE_INCH)

    @classmethod
    def from_ft2(cls, value: float) -> Self:
        return cls(value, AU.SQUARE_FOOT)

    @classmethod
    def from_mm2(cls, value: float) -> Self:
        return cls(value, AU.SQUARE_MILLIMETER)

    @classmethod
    def from_cm2(cls, value: float) -> Self:
        return cls(value, AU.SQUARE_CENTIMETER)

    @classmethod
    def from_m2(cls, value: float) -> Self:
        return cls(value, AU.SQUARE_METER)

    # ---- Value accessors ----
    @property
    def in2(self) -> float:
        return self.to_value(AU.SQUARE_INCH)

    @property
    def ft2(self) -> float:
        return self.to_value(AU.SQUARE_FOOT)

    @property
    def mm2(self) -> float:
        return self.to_value(AU.SQUARE_MILLIMETER)

    @property
    def cm2(self) -> float:
        return self.to_value(AU.SQUARE_CENTIMETER)

    @property
    def m2(self) -> float:
        return self.to_value(AU.SQUARE_METER)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[AU.SQUARE_INCH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[AU.SQUARE_FOOT]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[AU.SQUARE_MILLIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[AU.SQUARE_CENTIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[AU.SQUARE_METER]) -> float: ...
    @overload
    def to_value(self, target_unit: AU) -> float: ...

    def to_value(self, target_unit: AU) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, AU):
            raise ValueError(f"Expected AreaUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    def to_latex_string(self, display_unit: AU | None = None) -> str:
        """LaTeX string of the value in display_unit."""
        if display_unit is None:
            du = self.display_unit
            display_unit = du if isinstance(du, AU) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    @staticmethod
    def normalize_value(value: float, unit: AU) -> float:
        try:
            return float(value) * Area._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e

    # --- Division operators ---
    @overload
    def __truediv__(self, other: AU) -> "Unitless": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        if isinstance(other, AU):
            # Area / AreaUnit -> Unitless ratio
            from structunits.specific_units.unitless import Unitless
            
            # Get this area's value in the target unit
            value_in_unit = self.to_value(other)
            return Unitless(value_in_unit)

        return super().__truediv__(other)  # type: ignore[misc]


__all__ = ["Area"]
