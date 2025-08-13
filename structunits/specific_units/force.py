from __future__ import annotations

from typing import TYPE_CHECKING, Final, Dict, overload, Literal, Self, cast

from structunits.result import Result
from structunits.flt import FLT
from .force_unit import ForceUnit
from structunits.constants import (
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
)
from structunits.unit import UnitBase
from structunits.utilities import Utilities

if TYPE_CHECKING:
    from .length_unit import LengthUnit as LU
    from .force_per_length import ForcePerLength
    from .force_unit import ForceUnit as FU
    from .force_per_length_unit import ForcePerLengthUnit as FPLU

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

    # Conversion maps (kip <-> target)
    _TO_KIP: Dict[ForceUnit, float] = {
        ForceUnit.POUND: 1.0 / POUNDS_PER_KIP,
        ForceUnit.KIP: 1.0,
        ForceUnit.NEWTON: KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON,
        ForceUnit.KILONEWTON: KIPS_PER_KILONEWTON,
    }
    _FROM_KIP: Dict[ForceUnit, float] = {
        ForceUnit.POUND: POUNDS_PER_KIP,
        ForceUnit.KIP: 1.0,
        ForceUnit.NEWTON: NEWTONS_PER_KILONEWTON / KIPS_PER_KILONEWTON,
        ForceUnit.KILONEWTON: 1.0 / KIPS_PER_KILONEWTON,
    }

    # in structunits/specific_units/force.py
    def __init__(self, value: float, unit: ForceUnit):
        std_value = self.normalize_value(value, unit)
        # was: super().__init__(FLT.FORCE, std_value, self.default_unit(), unit)
        super().__init__(FLT.FORCE, std_value, unit, unit)


    def __repr__(self) -> str:
        return self.to_latex_string()
        
    # --- add overloads so Pylance understands Force / LengthUnit ---
    @overload
    def __truediv__(self, other: "LU") -> "ForcePerLength": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        # Handle Force / LengthUnit -> ForcePerLength
        from .length_unit import LengthUnit as LU
        if isinstance(other, LU):
            from .force_unit import ForceUnit as FU
            from .force_per_length_unit import ForcePerLengthUnit as FPLU
            from .force_per_length import ForcePerLength

            # choose numerator unit: use current display unit if it's a ForceUnit
            du = self.display_unit
            fu: FU = du if isinstance(du, FU) else FU.KIP

            # map FU/LU -> ForcePerLengthUnit (uses ForceUnit.__truediv__)
            fplu: FPLU = fu / other  # type: ignore[operator]

            # numeric magnitude in that numerator unit
            value_in_fu = self.to_value(fu)
            return ForcePerLength(value_in_fu, fplu)

        # otherwise fall back to base behavior (Result / Result|scalar)
        return super().__truediv__(other)  # type: ignore[misc]


    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> ForceUnit:
        return ForceUnit.KIP

    # --------- Convenience constructors (autocomplete-friendly) ---------
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_lb(cls, value: float) -> Self:
        """Construct from pounds (lb)."""
        return cls(value, ForceUnit.POUND)

    @classmethod
    def from_kip(cls, value: float) -> Self:
        """Construct from kips (kip)."""
        return cls(value, ForceUnit.KIP)

    @classmethod
    def from_N(cls, value: float) -> Self:
        """Construct from newtons (N)."""
        return cls(value, ForceUnit.NEWTON)

    @classmethod
    def from_kN(cls, value: float) -> Self:
        """Construct from kilonewtons (kN)."""
        return cls(value, ForceUnit.KILONEWTON)

    # NOTE: removed aliases like `lb = from_lb` because they collide with
    # the property `.lb` below and trigger "FunctionType is not assignable to property".

    # --------- Value accessors (autocomplete-friendly) ---------
    @property
    def lb(self) -> float:
        """Value in pounds (lb)."""
        return self.to_value(ForceUnit.POUND)

    @property
    def kip(self) -> float:
        """Value in kips (kip)."""
        return self.to_value(ForceUnit.KIP)

    @property
    def N(self) -> float:
        """Value in newtons (N)."""
        return self.to_value(ForceUnit.NEWTON)

    @property
    def kN(self) -> float:
        """Value in kilonewtons (kN)."""
        return self.to_value(ForceUnit.KILONEWTON)

    # --------- Typed conversion API ---------
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
            return self.value * self._FROM_KIP[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    def convert_to(self, target_unit: UnitBase) -> float:
        from structunits.specific_units.force_unit import ForceUnit as FU
        if not isinstance(target_unit, FU):
            raise ValueError(f"Expected ForceUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)


    def to_latex_string(self, display_unit: ForceUnit | None = None) -> str:
        """
        LaTeX string of the value in `display_unit` (default: current display unit if it's
        a ForceUnit, otherwise the default unit).
        """
        if display_unit is None:
            # Narrow self.display_unit (which is typed as UnitBase in Result) to ForceUnit when possible.
            du = self.display_unit
            display_unit = du if isinstance(du, ForceUnit) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    @staticmethod
    def normalize_value(value: float, unit: ForceUnit) -> float:
        """Normalize an input (value, unit) to kips."""
        try:
            return float(value) * Force._TO_KIP[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e


__all__ = ["Force"]
