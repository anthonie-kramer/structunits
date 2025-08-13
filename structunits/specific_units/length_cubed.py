from __future__ import annotations

from typing import Final, Dict, overload, Literal, Self

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.length_cubed_unit import LengthCubedUnit as LCU
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)
from structunits.unit import UnitBase
from structunits.utilities import Utilities


class LengthCubed(Result):
    """
    A length-cubed (volume) value. Standard unit: in³.
    """

    _EQ_TOL: Final[float] = 1e-3  # in³

    # in³  <- from unit
    _TO_STD: Dict[LCU, float] = {
        LCU.INCHES_CUBED: 1.0,
        LCU.FEET_CUBED: INCHES_PER_FOOT ** 3,
        LCU.MILLIMETERS_CUBED: (INCHES_PER_METER / MILLIMETERS_PER_METER) ** 3,
        LCU.METERS_CUBED: INCHES_PER_METER ** 3,
        LCU.CENTIMETERS_CUBED: (INCHES_PER_METER / CENTIMETERS_PER_METER) ** 3,
    }

    # unit <- from in³
    _FROM_STD: Dict[LCU, float] = {
        LCU.INCHES_CUBED: 1.0,
        LCU.FEET_CUBED: 1.0 / (INCHES_PER_FOOT ** 3),
        LCU.MILLIMETERS_CUBED: (MILLIMETERS_PER_METER ** 3) / (INCHES_PER_METER ** 3),
        LCU.METERS_CUBED: 1.0 / (INCHES_PER_METER ** 3),
        LCU.CENTIMETERS_CUBED: (CENTIMETERS_PER_METER ** 3) / (INCHES_PER_METER ** 3),
    }

    # in structunits/specific_units/length_cubed.py
    def __init__(self, value: float, unit: LCU):
        std_value = self.normalize_value(value, unit)
        super().__init__(FLT.LENGTH_CUBED, std_value, unit, unit)


    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return self._EQ_TOL

    @staticmethod
    def default_unit() -> LCU:
        return LCU.INCHES_CUBED

    # ---- Convenience constructors ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> Self:
        return cls(value, cls.default_unit())

    @classmethod
    def from_in3(cls, value: float) -> Self:
        return cls(value, LCU.INCHES_CUBED)

    @classmethod
    def from_ft3(cls, value: float) -> Self:
        return cls(value, LCU.FEET_CUBED)

    @classmethod
    def from_mm3(cls, value: float) -> Self:
        return cls(value, LCU.MILLIMETERS_CUBED)

    @classmethod
    def from_m3(cls, value: float) -> Self:
        return cls(value, LCU.METERS_CUBED)

    @classmethod
    def from_cm3(cls, value: float) -> Self:
        return cls(value, LCU.CENTIMETERS_CUBED)

    # ---- Value accessors ----
    @property
    def in3(self) -> float:
        return self.to_value(LCU.INCHES_CUBED)

    @property
    def ft3(self) -> float:
        return self.to_value(LCU.FEET_CUBED)

    @property
    def mm3(self) -> float:
        return self.to_value(LCU.MILLIMETERS_CUBED)

    @property
    def m3(self) -> float:
        return self.to_value(LCU.METERS_CUBED)

    @property
    def cm3(self) -> float:
        return self.to_value(LCU.CENTIMETERS_CUBED)

    # ---- Typed conversion API ----
    @overload
    def to_value(self, target_unit: Literal[LCU.INCHES_CUBED]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LCU.FEET_CUBED]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LCU.MILLIMETERS_CUBED]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LCU.METERS_CUBED]) -> float: ...
    @overload
    def to_value(self, target_unit: Literal[LCU.CENTIMETERS_CUBED]) -> float: ...
    @overload
    def to_value(self, target_unit: LCU) -> float: ...

    def to_value(self, target_unit: LCU) -> float:
        try:
            return self.value * self._FROM_STD[target_unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert to the target unit: {target_unit!r}") from e

    # Fluent alias
    in_ = to_value

    def convert_to(self, target_unit: UnitBase) -> float:
        from structunits.specific_units.length_cubed_unit import LengthCubedUnit as LCU
        if not isinstance(target_unit, LCU):
            raise ValueError(f"Expected LengthCubedUnit, got {type(target_unit).__name__}")
        return self.to_value(target_unit)


    def to_latex_string(self, display_unit: LCU | None = None) -> str:
        """
        LaTeX string of the value in `display_unit` (default: current display unit if it's LCU).
        """
        if display_unit is None:
            du = self.display_unit
            display_unit = du if isinstance(du, LCU) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    # ---- Normalization ----
    @staticmethod
    def normalize_value(value: float, unit: LCU) -> float:
        try:
            return float(value) * LengthCubed._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e


__all__ = ["LengthCubed"]
