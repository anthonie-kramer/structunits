from __future__ import annotations

from typing import Final, Mapping, ClassVar, overload, Literal, Self, TYPE_CHECKING
from types import MappingProxyType

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.stress_unit import StressUnit as SU
from structunits.utilities import Utilities
from structunits.unit import UnitBase

if TYPE_CHECKING:
    from structunits.specific_units.unitless import Unitless


class Stress(Result):
    """
    A stress value with unit handling (force per area).
    
    Standard unit: ksi (kip/in²).
    
    Examples
    --------
    >>> stress = Stress.from_psi(1000)
    >>> stress.ksi
    1.0
    """

    _EQ_TOL: Final[float] = 1e-4  # ksi

    # Conversion maps derived from unit enum for consistency
    _TO_STD: ClassVar[Mapping[SU, float]] = MappingProxyType({
        u: u.get_conversion_factor() for u in SU
    })
    _FROM_STD: ClassVar[Mapping[SU, float]] = MappingProxyType({
        u: 1.0 / u.get_conversion_factor() for u in SU
    })

    def __init__(self, value: float, unit: SU) -> None:
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.STRESS, std_value, unit, unit)


    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> SU:
        return SU.KSI

    @staticmethod
    def zero() -> "Stress":
        """Create a zero stress value."""
        return Stress(0.0, SU.KSI)

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_psi(cls, value: float) -> Self: return cls(value, SU.PSI)
    @classmethod
    def from_ksi(cls, value: float) -> Self: return cls(value, SU.KSI)
    @classmethod
    def from_psf(cls, value: float) -> Self: return cls(value, SU.PSF)
    @classmethod
    def from_ksf(cls, value: float) -> Self: return cls(value, SU.KSF)
    @classmethod
    def from_kPa(cls, value: float) -> Self: return cls(value, SU.KPA)
    @classmethod
    def from_MPa(cls, value: float) -> Self: return cls(value, SU.MPA)
    @classmethod
    def from_Pa(cls, value: float) -> Self:  return cls(value, SU.PA)

    # ---- Value accessors ----
    @property
    def psi(self) -> float: return self.to_value(SU.PSI)
    @property
    def ksi(self) -> float: return self.to_value(SU.KSI)
    @property
    def psf(self) -> float: return self.to_value(SU.PSF)
    @property
    def ksf(self) -> float: return self.to_value(SU.KSF)
    @property
    def kPa(self) -> float: return self.to_value(SU.KPA)
    @property
    def MPa(self) -> float: return self.to_value(SU.MPA)
    @property
    def Pa(self) -> float:  return self.to_value(SU.PA)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[SU.PSI]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[SU.KSI]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[SU.PSF]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[SU.KSF]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[SU.KPA]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[SU.MPA]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[SU.PA]) -> float: ...
    @overload
    def to_value(self, target_unit: SU) -> float: ...

    def to_value(self, target_unit: SU) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    # Satisfy Result abstract; delegate after narrowing
    def convert_to(self, target_unit: UnitBase) -> float:
        if not isinstance(target_unit, SU):
            raise ValueError(f"Expected StressUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)

    # Widen signature to match base (UnitBase | None); narrow before use
    def to_latex_string(self, display_unit: UnitBase | None = None) -> str:
        du = self.display_unit if display_unit is None else display_unit
        if not isinstance(du, SU):
            du = self.default_unit()
        return Utilities.to_latex_string(self.to_value(du), du)

    @staticmethod
    def normalize_value(value: float, unit: SU) -> float:
        try:
            return float(value) * Stress._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e

    # --- Division operators ---
    @overload
    def __truediv__(self, other: SU) -> "Unitless": ...
    @overload
    def __truediv__(self, other: "Result | float | int") -> "Result": ...

    def __truediv__(self, other: object) -> "Result":  # type: ignore[override]
        if isinstance(other, SU):
            # Stress / StressUnit -> Unitless ratio
            from structunits.specific_units.unitless import Unitless
            
            # Get this stress's value in the target unit
            value_in_unit = self.to_value(other)
            return Unitless(value_in_unit)

        return super().__truediv__(other)  # type: ignore[misc]


__all__ = ["Stress"]
