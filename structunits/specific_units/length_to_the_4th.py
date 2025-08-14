from __future__ import annotations

from typing import Final, Mapping, ClassVar, overload, Literal, Self, TYPE_CHECKING
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.length_to_the_4th_unit import LengthToThe4thUnit as L4U
from structunits.unit import UnitBase
from structunits.utilities import Utilities

if TYPE_CHECKING:
    from structunits.specific_units.unitless import Unitless


class LengthToThe4th(Result):
    """
    A length^4 value with unit handling (e.g., area moment of inertia).

    Standard unit: in⁴.

    Examples
    --------
    >>> inertia = LengthToThe4th.from_ft4(1.0)
    >>> inertia.in4
    20736.0
    """

    _EQ_TOL: Final[float] = 1e-3  # in⁴

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[L4U, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in L4U
    })
    _FROM_STD: ClassVar[Mapping[L4U, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in L4U
    })

    def __init__(self, value: float, unit: L4U) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.LENGTH_TO_THE_4TH, std_value, unit, unit)

    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> L4U:
        return L4U.INCHES_TO_THE_4TH

    @staticmethod
    def zero() -> "LengthToThe4th":
        """Create a zero length^4 value."""
        return LengthToThe4th(0.0, L4U.INCHES_TO_THE_4TH)

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_in4(cls, value: float) -> Self:
        return cls(value, L4U.INCHES_TO_THE_4TH)

    @classmethod
    def from_ft4(cls, value: float) -> Self:
        return cls(value, L4U.FEET_TO_THE_4TH)

    @classmethod
    def from_mm4(cls, value: float) -> Self:
        return cls(value, L4U.MILLIMETERS_TO_THE_4TH)

    @classmethod
    def from_m4(cls, value: float) -> Self:
        return cls(value, L4U.METERS_TO_THE_4TH)

    @classmethod
    def from_cm4(cls, value: float) -> Self:
        return cls(value, L4U.CENTIMETERS_TO_THE_4TH)

    # ---- Value accessors ----
    @property
    def in4(self) -> float:
        return self.to_value(L4U.INCHES_TO_THE_4TH)

    @property
    def ft4(self) -> float:
        return self.to_value(L4U.FEET_TO_THE_4TH)

    @property
    def mm4(self) -> float:
        return self.to_value(L4U.MILLIMETERS_TO_THE_4TH)

    @property
    def m4(self) -> float:
        return self.to_value(L4U.METERS_TO_THE_4TH)

    @property
    def cm4(self) -> float:
        return self.to_value(L4U.CENTIMETERS_TO_THE_4TH)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[L4U.INCHES_TO_THE_4TH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[L4U.FEET_TO_THE_4TH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[L4U.MILLIMETERS_TO_THE_4TH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[L4U.METERS_TO_THE_4TH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[L4U.CENTIMETERS_TO_THE_4TH]) -> float: ...
    @overload
    def to_value(self, target_unit: L4U) -> float: ...

    def to_value(self, target_unit: L4U) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, L4U):
            raise ValueError(f"Expected LengthToThe4thUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    def to_latex_string(self, display_unit: L4U | None = None) -> str:
        """LaTeX string of the value in display_unit."""
        if display_unit is None:
            du = self.display_unit
            display_unit = du if isinstance(du, L4U) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    @staticmethod
    def normalize_value(value: float, unit: L4U) -> float:
        try:
            return float(value) * LengthToThe4th._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e

    # --- Division operators ---
    @overload
    def __truediv__(self, other: L4U) -> "Unitless": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        if isinstance(other, L4U):
            # LengthToThe4th / LengthToThe4thUnit -> Unitless ratio
            from structunits.specific_units.unitless import Unitless
            
            # Get this length^4's value in the target unit
            value_in_unit = self.to_value(other)
            return Unitless(value_in_unit)

        return super().__truediv__(other)  # type: ignore[misc]


__all__ = ["LengthToThe4th"]