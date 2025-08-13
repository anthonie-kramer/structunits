from __future__ import annotations

from typing import Final, Dict, overload, Literal, Self

from structunits.result import Result
from structunits.flt import FLT
from structunits.specific_units.length_to_the_4th_unit import LengthToThe4thUnit as L4U
from structunits.constants import (
    INCHES_PER_FOOT,
    INCHES_PER_METER,
    MILLIMETERS_PER_METER,
    CENTIMETERS_PER_METER,
)
from structunits.unit import UnitBase
from structunits.utilities import Utilities


class LengthToThe4th(Result):
    """
    A length^4 value (e.g., area moment of inertia). Standard unit: in⁴.
    """

    _EQ_TOL: Final[float] = 1e-3  # in⁴

    # in⁴  <- from unit
    _TO_STD: Dict[L4U, float] = {
        L4U.INCHES_TO_THE_4TH: 1.0,
        L4U.FEET_TO_THE_4TH: INCHES_PER_FOOT ** 4,
        L4U.MILLIMETERS_TO_THE_4TH: (INCHES_PER_METER / MILLIMETERS_PER_METER) ** 4,
        L4U.METERS_TO_THE_4TH: INCHES_PER_METER ** 4,
        L4U.CENTIMETERS_TO_THE_4TH: (INCHES_PER_METER / CENTIMETERS_PER_METER) ** 4,
    }

    # unit <- from in⁴
    _FROM_STD: Dict[L4U, float] = {
        L4U.INCHES_TO_THE_4TH: 1.0,
        L4U.FEET_TO_THE_4TH: 1.0 / (INCHES_PER_FOOT ** 4),
        L4U.MILLIMETERS_TO_THE_4TH: (MILLIMETERS_PER_METER ** 4) / (INCHES_PER_METER ** 4),
        L4U.METERS_TO_THE_4TH: 1.0 / (INCHES_PER_METER ** 4),
        L4U.CENTIMETERS_TO_THE_4TH: (CENTIMETERS_PER_METER ** 4) / (INCHES_PER_METER ** 4),
    }

    # in structunits/specific_units/length_to_the_4th.py
    def __init__(self, value: float, unit: L4U):
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
            from structunits.specific_units.length_to_the_4th_unit import LengthToThe4thUnit as L4U
            if not isinstance(target_unit, L4U):
                raise ValueError(f"Expected LengthToThe4thUnit, got {type(target_unit).__name__}")
            return self.to_value(target_unit)


    def to_latex_string(self, display_unit: L4U | None = None) -> str:
        """
        LaTeX string of the value in `display_unit` (default: current display unit if it's L4U).
        """
        if display_unit is None:
            du = self.display_unit
            display_unit = du if isinstance(du, L4U) else self.default_unit()
        return Utilities.to_latex_string(self.to_value(display_unit), display_unit)

    # ---- Normalization ----
    @staticmethod
    def normalize_value(value: float, unit: L4U) -> float:
        try:
            return float(value) * LengthToThe4th._TO_STD[unit]
        except KeyError as e:
            raise ValueError(f"Cannot convert from the source unit: {unit!r}") from e


__all__ = ["LengthToThe4th"]
