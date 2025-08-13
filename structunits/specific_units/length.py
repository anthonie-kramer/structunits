from __future__ import annotations

from typing import Final, Dict, overload, Literal, Self

from structunits.result import Result
from structunits.flt import FLT
from .length_unit import LengthUnit as LU
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)
from structunits.utilities import Utilities
from structunits.unit import UnitBase  # <-- for convert_to and widened to_latex_string


class Length(Result):
    """
    A length value with unit handling. Standard unit: inch (in).
    """

    _EQ_TOL: Final[float] = 1e-3  # inches

    # in  <- from unit
    _TO_STD: Dict[LU, float] = {
        LU.INCH: 1.0,
        LU.FOOT: INCHES_PER_FOOT,
        LU.MILLIMETER: INCHES_PER_METER / MILLIMETERS_PER_METER,
        LU.METER: INCHES_PER_METER,
        LU.CENTIMETER: INCHES_PER_METER / CENTIMETERS_PER_METER,
    }

    # unit <- from in
    _FROM_STD: Dict[LU, float] = {
        LU.INCH: 1.0,
        LU.FOOT: 1.0 / INCHES_PER_FOOT,
        LU.MILLIMETER: MILLIMETERS_PER_METER / INCHES_PER_METER,
        LU.METER: 1.0 / INCHES_PER_METER,
        LU.CENTIMETER: CENTIMETERS_PER_METER / INCHES_PER_METER,
    }

        # in structunits/specific_units/length.py
    def __init__(self, value: float, unit: LU):
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
        """
        LaTeX string of the value in `display_unit`
        (default: current display unit if it is a LengthUnit).
        """
        du = self.display_unit if display_unit is None else display_unit
        if not isinstance(du, LU):
            du = self.default_unit()
        return Utilities.to_latex_string(self.to_value(du), du)

    # ---- Normalization ----
    @staticmethod
    def normalize_value(value: float, unit: LU) -> float:
        try:
            return float(value) * Length._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e
