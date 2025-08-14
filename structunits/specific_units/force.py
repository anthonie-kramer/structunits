from __future__ import annotations

from typing import TYPE_CHECKING, Final, Mapping, ClassVar, overload, Literal, Self
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from .force_unit import ForceUnit
from structunits.unit import UnitBase
from structunits.utilities import Utilities

if TYPE_CHECKING:
    from .length_unit import LengthUnit as LU
    from .force_per_length import ForcePerLength
    from .force_per_length_unit import ForcePerLengthUnit as FPLU
    from structunits.specific_units.unitless import Unitless


class Force(Result):
    """
    A force value with unit handling (standard unit: kip).

    Examples
    --------
    >>> F = Force.from_lb(1200)
    >>> F.kip
    1.2
    >>> round(F.to_value(ForceUnit.KILONEWTON), 3)
    5.338
    >>> round(Force.from_kN(10).lb, 3)
    2248.089
    """

    _EQ_TOL: Final[float] = 1e-4  # kips

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[ForceUnit, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in ForceUnit
    })
    _FROM_STD: ClassVar[Mapping[ForceUnit, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in ForceUnit
    })

    def __init__(self, value: float, unit: ForceUnit) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.FORCE, std_value, unit, unit)

    # Prefer a debug-friendly repr, keep LaTeX for __str__/to_latex_string.
    def __repr__(self) -> str:
        return f"Force({self.to_value(ForceUnit.KIP)!r} kip)"

    def __str__(self) -> str:
        return self.to_latex_string()

    # --- Division operators ---
    @overload
    def __truediv__(self, other: ForceUnit) -> "Unitless": ...
    @overload
    def __truediv__(self, other: "LU") -> "ForcePerLength": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        from .length_unit import LengthUnit as LU
        
        if isinstance(other, ForceUnit):
            # Force / ForceUnit -> Unitless ratio
            from structunits.specific_units.unitless import Unitless
            
            # Get this force's value in the target unit
            value_in_unit = self.to_value(other)
            return Unitless(value_in_unit)
            
        elif isinstance(other, LU):
            # Force / LengthUnit -> ForcePerLength (existing logic)
            from .force_per_length import ForcePerLength
            from .force_per_length_unit import ForcePerLengthUnit as FPLU

            du = self.display_unit
            fu: ForceUnit = du if isinstance(du, ForceUnit) else ForceUnit.KIP

            fplu: FPLU = fu / other  # ForceUnit.__truediv__(LengthUnit) -> ForcePerLengthUnit
            value_in_fu = self.to_value(fu)
            return ForcePerLength(value_in_fu, fplu)

        return super().__truediv__(other)  # type: ignore[misc]

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> ForceUnit:
        return ForceUnit.KIP

    @staticmethod
    def zero() -> "Force":
        """Create a zero force value."""
        return Force(0.0, ForceUnit.KIP)

    # --------- Constructors ---------
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_value(cls, value: float, unit: ForceUnit) -> Self:
        """Generic constructor when you already have the unit enum."""
        return cls(value, unit)

    @classmethod
    def from_lb(cls, value: float) -> Self:
        return cls(value, ForceUnit.POUND)

    @classmethod
    def from_kip(cls, value: float) -> Self:
        return cls(value, ForceUnit.KIP)

    @classmethod
    def from_N(cls, value: float) -> Self:
        return cls(value, ForceUnit.NEWTON)

    @classmethod
    def from_kN(cls, value: float) -> Self:
        return cls(value, ForceUnit.KILONEWTON)

    # --------- Value accessors ---------
    @property
    def lb(self) -> float:
        return self.to_value(ForceUnit.POUND)

    @property
    def kip(self) -> float:
        return self.to_value(ForceUnit.KIP)

    @property
    def N(self) -> float:
        return self.to_value(ForceUnit.NEWTON)

    @property
    def kN(self) -> float:
        return self.to_value(ForceUnit.KILONEWTON)

    # --------- Typed conversion API (float) ---------
    @overload
    def to_value(self, target_unit: Literal[ForceUnit.POUND]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[ForceUnit.KIP]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[ForceUnit.NEWTON]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[ForceUnit.KILONEWTON]) -> float: ...
    @overload
    def to_value(self, target_unit: ForceUnit) -> float: ...

    def to_value(self, target_unit: ForceUnit) -> float:
        """Convert to a raw float in the given unit."""
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Aliases for ergonomics
    in_ = to_value
    value_in = to_value

    # --------- Object conversion (returns Force) ---------
    def as_unit(self, target_unit: ForceUnit) -> "Force":
        """Return a new Force whose display/source unit is `target_unit`."""
        return Force(self.to_value(target_unit), target_unit)

    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, ForceUnit):
            raise ValueError(f"Expected ForceUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    def to_latex_string(self, display_unit: ForceUnit | None = None) -> str:
        if display_unit is None:
            du = self.display_unit
            display_unit = du if isinstance(du, ForceUnit) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    @staticmethod
    def normalize_value(value: float, unit: ForceUnit) -> float:
        """Normalize an input (value, unit) to kips."""
        try:
            return float(value) * Force._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e

__all__ = ["Force"]