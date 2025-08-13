from __future__ import annotations

from typing import Self

from structunits.result import Result
from structunits.flt import FLT
from structunits.unit import UnitBase


# Sentinel unit so we don't pass None to Result.__init__
_UNDEFINED_UNIT = UnitBase("-", "undefined")


class Undefined(Result):
    """Undefined unit type, used for custom FLT combinations."""

    def __init__(self, flt: FLT, value: float):
        # display_unit / input_unit use a harmless sentinel
        super().__init__(flt, float(value), _UNDEFINED_UNIT, _UNDEFINED_UNIT)

    def __repr__(self) -> str:
        return self.to_latex_string()

    @property
    def equality_tolerance(self) -> float:
        return 1e-10

    def to_latex_string(self, display_unit: UnitBase | None = None) -> str:
        # Plain textual form; we don't have a real unit symbol here
        return f"{self.value} [{self.flt}]"

    def convert_to(self, target_unit: UnitBase) -> float:
        # Conversions are not meaningful for Undefined.
        # Allow a no-op only if the sentinel is explicitly requested.
        if target_unit is _UNDEFINED_UNIT:
            return self.value
        raise ValueError(f"Cannot convert undefined unit to target unit: {target_unit}")

    # ---- Scalar arithmetic overrides to preserve this instance's FLT ----
    def __mul__(self, other: float | int | Result) -> Result:
        if isinstance(other, (int, float)):
            return Undefined(self.flt, self.value * float(other))
        return super().__mul__(other)

    def __rmul__(self, other: float | int) -> Result:
        if isinstance(other, (int, float)):
            return Undefined(self.flt, float(other) * self.value)
        return super().__rmul__(other)

    def __truediv__(self, other: float | int | Result) -> Result:
        if isinstance(other, (int, float)):
            return Undefined(self.flt, self.value / float(other))
        return super().__truediv__(other)

    def __rtruediv__(self, other: float | int) -> Result:
        if isinstance(other, (int, float)):
            # other / self -> FLT becomes -self.flt (as in base); keep base behavior
            return super().__rtruediv__(other)
        return super().__rtruediv__(other)

    # For +/- with scalars, keep base behavior (which requires unitless),
    # because adding a pure scalar only makes sense for unitless quantities.

    # ---- Factory used by base class when operating on unitless Undefined ----
    @classmethod
    def create_with_standard_units(cls, value: float) -> "Undefined":
        # This is only called by base ops that first confirm unitless.
        # So we return a unitless Undefined.
        return cls(FLT.UNITLESS, value)


__all__ = ["Undefined"]
