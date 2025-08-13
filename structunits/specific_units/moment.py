from __future__ import annotations

from typing import Final, Dict, overload, Literal, Self

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.moment_unit import MomentUnit as MU
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
    POUNDS_PER_KIP,
    NEWTONS_PER_KILONEWTON,
    KIPS_PER_KILONEWTON,
)
from structunits.utilities import Utilities
from structunits.unit import UnitBase


class Moment(Result):
    """
    A moment value with unit handling (force × distance).
    Standard unit: kip·inch (kip-in).
    """

    _EQ_TOL: Final[float] = 1e-2  # kip-in

    # kip-in  <- from unit
    _TO_STD: Dict[MU, float] = {
        MU.POUND_INCH: 1.0 / POUNDS_PER_KIP,
        MU.POUND_FOOT: (1.0 / POUNDS_PER_KIP) * INCHES_PER_FOOT,
        MU.KIP_INCH: 1.0,
        MU.KIP_FOOT: INCHES_PER_FOOT,
        MU.NEWTON_METER: KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON * INCHES_PER_METER,
        MU.KILONEWTON_METER: KIPS_PER_KILONEWTON * INCHES_PER_METER,
        MU.KILONEWTON_MILLIMETER: KIPS_PER_KILONEWTON * INCHES_PER_METER / MILLIMETERS_PER_METER,
        MU.NEWTON_MILLIMETER: KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON * INCHES_PER_METER / MILLIMETERS_PER_METER,
        MU.KILONEWTON_CENTIMETER: KIPS_PER_KILONEWTON * INCHES_PER_METER / CENTIMETERS_PER_METER,
        MU.NEWTON_CENTIMETER: KIPS_PER_KILONEWTON / NEWTONS_PER_KILONEWTON * INCHES_PER_METER / CENTIMETERS_PER_METER,
    }

    # unit <- from kip-in
    _FROM_STD: Dict[MU, float] = {
        MU.POUND_INCH: POUNDS_PER_KIP,
        MU.POUND_FOOT: POUNDS_PER_KIP / INCHES_PER_FOOT,
        MU.KIP_INCH: 1.0,
        MU.KIP_FOOT: 1.0 / INCHES_PER_FOOT,
        MU.NEWTON_METER: NEWTONS_PER_KILONEWTON / KIPS_PER_KILONEWTON / INCHES_PER_METER,
        MU.KILONEWTON_METER: 1.0 / KIPS_PER_KILONEWTON / INCHES_PER_METER,
        MU.KILONEWTON_MILLIMETER: 1.0 / KIPS_PER_KILONEWTON * (MILLIMETERS_PER_METER / INCHES_PER_METER),
        MU.NEWTON_MILLIMETER: NEWTONS_PER_KILONEWTON / KIPS_PER_KILONEWTON * (MILLIMETERS_PER_METER / INCHES_PER_METER),
        MU.KILONEWTON_CENTIMETER: 1.0 / KIPS_PER_KILONEWTON * (CENTIMETERS_PER_METER / INCHES_PER_METER),
        MU.NEWTON_CENTIMETER: NEWTONS_PER_KILONEWTON / KIPS_PER_KILONEWTON * (CENTIMETERS_PER_METER / INCHES_PER_METER),
    }

    # in structunits/specific_units/moment.py
    def __init__(self, value: float, unit: MU):
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

    # ---- Normalization ----
    @staticmethod
    def normalize_value(value: float, unit: MU) -> float:
        try:
            return float(value) * Moment._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e


__all__ = ["Moment"]
