from __future__ import annotations

from typing import Final, Mapping, ClassVar, overload, Literal, Self, TYPE_CHECKING
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from .length_unit import LengthUnit as LU
from structunits.utilities import Utilities
from structunits.unit import UnitBase

if TYPE_CHECKING:
    from structunits.specific_units.unitless import Unitless


class Length(Result):
    """
    A length value with unit handling.
    
    Standard unit: inch (in).
    
    Examples
    --------
    >>> length = Length.from_ft(1.0)
    >>> length.inch
    12.0
    """

    _EQ_TOL: Final[float] = 1e-3  # inches

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[LU, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in LU
    })
    _FROM_STD: ClassVar[Mapping[LU, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in LU
    })

    def __init__(self, value: float, unit: LU) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.LENGTH, std_value, unit, unit)


    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> LU:
        return LU.INCH

    @staticmethod
    def zero() -> "Length":
        """Create a zero length value."""
        return Length(0.0, LU.INCH)

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_in(cls, value: float) -> Self:
        return cls(value, LU.INCH)

    @classmethod
    def from_ft(cls, value: float) -> Self:
        return cls(value, LU.FOOT)

    @classmethod
    def from_mm(cls, value: float) -> Self:
        return cls(value, LU.MILLIMETER)

    @classmethod
    def from_m(cls, value: float) -> Self:
        return cls(value, LU.METER)

    @classmethod
    def from_cm(cls, value: float) -> Self:
        return cls(value, LU.CENTIMETER)

    # ---- Value accessors ----
    @property
    def inch(self) -> float:
        return self.to_value(LU.INCH)

    @property
    def ft(self) -> float:
        return self.to_value(LU.FOOT)

    @property
    def mm(self) -> float:
        return self.to_value(LU.MILLIMETER)

    @property
    def m(self) -> float:
        return self.to_value(LU.METER)

    @property
    def cm(self) -> float:
        return self.to_value(LU.CENTIMETER)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[LU.INCH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LU.FOOT]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LU.MILLIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LU.METER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LU.CENTIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: LU) -> float: ...

    def to_value(self, target_unit: LU) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    # Satisfy Result's abstract method; delegate to to_value
    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, LU):
            raise ValueError(f"Expected LengthUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    # Widen signature to match base class (UnitBase | None), then narrow before use
    def to_latex_string(self, display_unit: UnitBase | None = None) -> str:
        """LaTeX string of the value in display_unit."""
        du = self.display_unit if display_unit is None else display_unit
        if not isinstance(du, LU):
            du = self.default_unit()
        return Utilities.to_latex_string(self.to_value(du), du)

    @staticmethod
    def normalize_value(value: float, unit: LU) -> float:
        try:
            return float(value) * Length._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e

    # --- Division operators ---
    @overload
    def __truediv__(self, other: LU) -> "Unitless": ...
    @overload  
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        from .length_unit import LengthUnit as LU
        if isinstance(other, LU):
            # Length / LengthUnit -> Unitless ratio
            from structunits.specific_units.unitless import Unitless
            
            # Get this length's value in the target unit
            value_in_unit = self.to_value(other)
            return Unitless(value_in_unit)

        return super().__truediv__(other)  # type: ignore[misc]

__all__ = ["Length"]
