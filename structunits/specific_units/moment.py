from __future__ import annotations

from typing import Final, Mapping, ClassVar, overload, Literal, Self, TYPE_CHECKING
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.moment_unit import MomentUnit as MU
from structunits.utilities import Utilities
from structunits.unit import UnitBase

if TYPE_CHECKING:
    from .length_unit import LengthUnit
    from .force_unit import ForceUnit
    from .force import Force
    from .length import Length


class Moment(Result):
    """
    A moment value with unit handling (force × distance).
    
    Standard unit: kip·inch (kip-in).
    
    Examples
    --------
    >>> moment = Moment.from_lb_ft(1000)
    >>> moment.k_in
    83.333...
    """

    _EQ_TOL: Final[float] = 1e-2  # kip-in

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[MU, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in MU
    })
    _FROM_STD: ClassVar[Mapping[MU, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in MU
    })

    def __init__(self, value: float, unit: MU) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.MOMENT, std_value, unit, unit)


    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> MU:
        return MU.KIP_INCH

    @staticmethod
    def zero() -> "Moment":
        """Create a zero moment value."""
        return Moment(0.0, MU.KIP_INCH)

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_lb_in(cls, value: float) -> Self:
        return cls(value, MU.POUND_INCH)

    @classmethod
    def from_lb_ft(cls, value: float) -> Self:
        return cls(value, MU.POUND_FOOT)

    @classmethod
    def from_k_in(cls, value: float) -> Self:
        return cls(value, MU.KIP_INCH)

    @classmethod
    def from_k_ft(cls, value: float) -> Self:
        return cls(value, MU.KIP_FOOT)

    @classmethod
    def from_N_m(cls, value: float) -> Self:
        return cls(value, MU.NEWTON_METER)

    @classmethod
    def from_kN_m(cls, value: float) -> Self:
        return cls(value, MU.KILONEWTON_METER)

    @classmethod
    def from_N_mm(cls, value: float) -> Self:
        return cls(value, MU.NEWTON_MILLIMETER)

    @classmethod
    def from_kN_mm(cls, value: float) -> Self:
        return cls(value, MU.KILONEWTON_MILLIMETER)

    @classmethod
    def from_N_cm(cls, value: float) -> Self:
        return cls(value, MU.NEWTON_CENTIMETER)

    @classmethod
    def from_kN_cm(cls, value: float) -> Self:
        return cls(value, MU.KILONEWTON_CENTIMETER)

    # ---- Value accessors ----
    @property
    def lb_in(self) -> float:
        return self.to_value(MU.POUND_INCH)

    @property
    def lb_ft(self) -> float:
        return self.to_value(MU.POUND_FOOT)

    @property
    def k_in(self) -> float:
        return self.to_value(MU.KIP_INCH)

    @property
    def k_ft(self) -> float:
        return self.to_value(MU.KIP_FOOT)

    @property
    def N_m(self) -> float:
        return self.to_value(MU.NEWTON_METER)

    @property
    def kN_m(self) -> float:
        return self.to_value(MU.KILONEWTON_METER)

    @property
    def N_mm(self) -> float:
        return self.to_value(MU.NEWTON_MILLIMETER)

    @property
    def kN_mm(self) -> float:
        return self.to_value(MU.KILONEWTON_MILLIMETER)

    @property
    def N_cm(self) -> float:
        return self.to_value(MU.NEWTON_CENTIMETER)

    @property
    def kN_cm(self) -> float:
        return self.to_value(MU.KILONEWTON_CENTIMETER)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[MU.POUND_INCH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.POUND_FOOT]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.KIP_INCH]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.KIP_FOOT]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.NEWTON_METER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.KILONEWTON_METER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.NEWTON_MILLIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.KILONEWTON_MILLIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.NEWTON_CENTIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[MU.KILONEWTON_CENTIMETER]) -> float: ...
    @overload
    def to_value(self, target_unit: MU) -> float: ...

    def to_value(self, target_unit: MU) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    # Satisfy Result abstract; delegate after narrowing
    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, MU):
            raise ValueError(f"Expected MomentUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    # Widen signature to match base (UnitBase | None); narrow before use
    def to_latex_string(self, display_unit: UnitBase | None = None) -> str:
        du = self.display_unit if display_unit is None else display_unit
        if not isinstance(du, MU):
            du = self.default_unit()
        return Utilities.to_latex_string(self.to_value(du), du)

    # --- Division operators for unit decomposition ---
    @overload
    def __truediv__(self, other: "LengthUnit") -> "Force": ...
    @overload
    def __truediv__(self, other: "ForceUnit") -> "Length": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        from .length_unit import LengthUnit as LU
        from .force_unit import ForceUnit as FU
        
        if isinstance(other, LU):
            # Moment / LengthUnit -> Force
            from .force import Force
            from .moment_unit import MomentUnit as MU
            
            # Get the moment unit and decompose it
            moment_display_unit = self.display_unit
            moment_unit = moment_display_unit if isinstance(moment_display_unit, MU) else MU.KIP_INCH
            
            # Use the MomentUnit division to get the corresponding ForceUnit
            decomposed_unit = moment_unit / other  # Returns LengthUnit | ForceUnit
            
            # Type narrow: we know that MomentUnit / LengthUnit -> ForceUnit
            if not isinstance(decomposed_unit, FU):
                raise TypeError(f"Expected ForceUnit from moment/length division, got {type(decomposed_unit)}")
            force_unit = decomposed_unit
            
            # Get moment value in the moment unit, then create force
            moment_value = self.to_value(moment_unit)
            return Force(moment_value, force_unit)
            
        elif isinstance(other, FU):
            # Moment / ForceUnit -> Length
            from .length import Length
            from .moment_unit import MomentUnit as MU
            
            # Get the moment unit and decompose it
            moment_display_unit = self.display_unit
            moment_unit = moment_display_unit if isinstance(moment_display_unit, MU) else MU.KIP_INCH
            
            # Use the MomentUnit division to get the corresponding LengthUnit
            decomposed_unit = moment_unit / other  # Returns LengthUnit | ForceUnit
            
            # Type narrow: we know that MomentUnit / ForceUnit -> LengthUnit
            if not isinstance(decomposed_unit, LU):
                raise TypeError(f"Expected LengthUnit from moment/force division, got {type(decomposed_unit)}")
            length_unit = decomposed_unit
            
            # Get moment value in the moment unit, then create length
            moment_value = self.to_value(moment_unit)
            return Length(moment_value, length_unit)

        return super().__truediv__(other)  # type: ignore[misc]

    # ---- Normalization ----
    @staticmethod
    def normalize_value(value: float, unit: MU) -> float:
        try:
            return float(value) * Moment._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e


__all__ = ["Moment"]