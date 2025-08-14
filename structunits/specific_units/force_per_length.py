from __future__ import annotations

from typing import Final, Mapping, ClassVar, overload, Literal, Self, TYPE_CHECKING
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from structunits.unit import UnitBase
from structunits.specific_units.force_per_length_unit import ForcePerLengthUnit as FPLU
from structunits.utilities import Utilities

if TYPE_CHECKING:
    from structunits.specific_units.unitless import Unitless


class ForcePerLength(Result):
    """
    A distributed load with unit handling (force per length).
    
    Standard unit: kip per inch (k/in).
    
    Examples
    --------
    >>> load = ForcePerLength.from_lb_per_ft(100)
    >>> load.kip_per_in
    0.00694...
    """

    _EQ_TOL: Final[float] = 1e-4  # kips/inch

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[FPLU, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in FPLU
    })
    _FROM_STD: ClassVar[Mapping[FPLU, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in FPLU
    })

    def __init__(self, value: float, unit: FPLU) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.FORCE_PER_LENGTH, std_value, unit, unit)


    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> FPLU:
        return FPLU.KIP_PER_INCH

    @staticmethod
    def zero() -> "ForcePerLength":
        """Create a zero distributed load value."""
        return ForcePerLength(0.0, FPLU.KIP_PER_INCH)

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_lb_per_in(cls, value: float) -> Self:
        return cls(value, FPLU.POUND_PER_INCH)

    @classmethod
    def from_lb_per_ft(cls, value: float) -> Self:
        return cls(value, FPLU.POUND_PER_FOOT)

    @classmethod
    def from_kip_per_in(cls, value: float) -> Self:
        return cls(value, FPLU.KIP_PER_INCH)

    @classmethod
    def from_kip_per_ft(cls, value: float) -> Self:
        return cls(value, FPLU.KIP_PER_FOOT)

    @classmethod
    def from_N_per_m(cls, value: float) -> Self:
        return cls(value, FPLU.NEWTON_PER_METER)

    @classmethod
    def from_kN_per_m(cls, value: float) -> Self:
        return cls(value, FPLU.KILONEWTON_PER_METER)

    @classmethod
    def from_N_per_mm(cls, value: float) -> Self:
        return cls(value, FPLU.NEWTON_PER_MILLIMETER)

    @classmethod
    def from_kN_per_mm(cls, value: float) -> Self:
        return cls(value, FPLU.KILONEWTON_PER_MILLIMETER)

    @classmethod
    def from_N_per_cm(cls, value: float) -> Self:
        return cls(value, FPLU.NEWTON_PER_CENTIMETER)

    @classmethod
    def from_kN_per_cm(cls, value: float) -> Self:
        return cls(value, FPLU.KILONEWTON_PER_CENTIMETER)

    # ---- Value accessors ----
    @property
    def lb_per_in(self) -> float:
        return self.to_value(FPLU.POUND_PER_INCH)

    @property
    def lb_per_ft(self) -> float:
        return self.to_value(FPLU.POUND_PER_FOOT)

    @property
    def kip_per_in(self) -> float:
        return self.to_value(FPLU.KIP_PER_INCH)

    @property
    def kip_per_ft(self) -> float:
        return self.to_value(FPLU.KIP_PER_FOOT)

    @property
    def N_per_m(self) -> float:
        return self.to_value(FPLU.NEWTON_PER_METER)

    @property
    def kN_per_m(self) -> float:
        return self.to_value(FPLU.KILONEWTON_PER_METER)

    @property
    def N_per_mm(self) -> float:
        return self.to_value(FPLU.NEWTON_PER_MILLIMETER)

    @property
    def kN_per_mm(self) -> float:
        return self.to_value(FPLU.KILONEWTON_PER_MILLIMETER)

    @property
    def N_per_cm(self) -> float:
        return self.to_value(FPLU.NEWTON_PER_CENTIMETER)

    @property
    def kN_per_cm(self) -> float:
        return self.to_value(FPLU.KILONEWTON_PER_CENTIMETER)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[FPLU.POUND_PER_INCH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.POUND_PER_FOOT]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.KIP_PER_INCH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.KIP_PER_FOOT]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.NEWTON_PER_METER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.KILONEWTON_PER_METER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.NEWTON_PER_MILLIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.KILONEWTON_PER_MILLIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.NEWTON_PER_CENTIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[FPLU.KILONEWTON_PER_CENTIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: FPLU) -> float: ...

    def to_value(self, target_unit: FPLU) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, FPLU):
            raise ValueError(f"Expected ForcePerLengthUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    def to_latex_string(self, display_unit: FPLU | None = None) -> str:
        """LaTeX string of the value in display_unit."""
        if display_unit is None:
            du = self.display_unit
            display_unit = du if isinstance(du, FPLU) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    @staticmethod
    def normalize_value(value: float, unit: FPLU) -> float:
        try:
            return float(value) * ForcePerLength._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e

    # --- Division operators ---
    @overload
    def __truediv__(self, other: FPLU) -> "Unitless": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        if isinstance(other, FPLU):
            # ForcePerLength / ForcePerLengthUnit -> Unitless ratio
            from structunits.specific_units.unitless import Unitless
            
            # Get this distributed load's value in the target unit
            value_in_unit = self.to_value(other)
            return Unitless(value_in_unit)

        return super().__truediv__(other)  # type: ignore[misc]

__all__ = ["ForcePerLength"]