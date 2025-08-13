from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable as CIterable
from typing import TypeVar, Generic, overload
import math

from structunits.unit import UnitBase
from structunits.flt import FLT
from structunits.unit_type import UnitType
from structunits.utilities import Utilities  # (subclasses usually call this)

# Covariant-ish helper for overloads on functions that return the same concrete subtype
ResultT = TypeVar("ResultT", bound="Result")


class Result(ABC, Generic[ResultT]):
    """Abstract base class for results with units."""

    flt: FLT
    value: float
    display_unit: UnitBase
    _input_unit: UnitBase

    def __init__(self, flt: FLT, value: float, display_unit: UnitBase, input_unit: UnitBase):
        self.flt = flt
        self.value = float(value)
        self.display_unit = display_unit
        self._input_unit = input_unit

    @property
    def input_unit(self) -> UnitBase:
        """The unit this value was created with."""
        return self._input_unit

    @property
    def input_unit_value(self) -> float:
        """The value of this result expressed in the input units."""
        return self.convert_to(self.input_unit)

    @property
    @abstractmethod
    def equality_tolerance(self) -> float:  # in standard units of the concrete type
        ...

    @abstractmethod
    def to_latex_string(self, display_unit: UnitBase | None = None) -> str:
        """LaTeX string of the value in `display_unit` (or `self.display_unit` if None)."""
        ...

    @abstractmethod
    def convert_to(self, target_unit: UnitBase) -> float:
        """Return the numeric value converted to `target_unit`."""
        ...

    # ------------------ Comparisons ------------------
    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, Result):
            return False
        if self is other:
            return True
        if self.flt == other.flt:
            return abs(self.value - other.value) <= self.equality_tolerance
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: "Result") -> bool:
        Result._confirm_units_match(self, other)
        return self.value < other.value

    def __le__(self, other: "Result") -> bool:
        Result._confirm_units_match(self, other)
        return self.value <= other.value

    def __gt__(self, other: "Result") -> bool:
        Result._confirm_units_match(self, other)
        return self.value > other.value

    def __ge__(self, other: "Result") -> bool:
        Result._confirm_units_match(self, other)
        return self.value >= other.value

    # ------------------ Arithmetic ------------------
    def __add__(self: ResultT, other: "Result | float | int") -> ResultT | "Result":
        if isinstance(other, Result):
            Result._confirm_units_match(self, other)
            return self._build_typed_result(self.flt, self.value + other.value)  # type: ignore[return-value]
        if isinstance(other, (int, float)):
            Result._confirm_unitless(self)
            return self.__class__.create_with_standard_units(self.value + float(other))  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __radd__(self: ResultT, other: "float | int") -> ResultT | "Result":
        if isinstance(other, (int, float)):
            Result._confirm_unitless(self)
            return self.__class__.create_with_standard_units(float(other) + self.value)  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __sub__(self: ResultT, other: "Result | float | int") -> ResultT | "Result":
        if isinstance(other, Result):
            Result._confirm_units_match(self, other)
            return self._build_typed_result(self.flt, self.value - other.value)  # type: ignore[return-value]
        if isinstance(other, (int, float)):
            Result._confirm_unitless(self)
            return self.__class__.create_with_standard_units(self.value - float(other))  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __rsub__(self: ResultT, other: "float | int") -> ResultT | "Result":
        if isinstance(other, (int, float)):
            Result._confirm_unitless(self)
            return self.__class__.create_with_standard_units(float(other) - self.value)  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __mul__(self: ResultT, other: "Result | float | int") -> ResultT | "Result":
        if isinstance(other, Result):
            return self._build_typed_result(self.flt + other.flt, self.value * other.value)  # type: ignore[return-value]
        if isinstance(other, (int, float)):
            return self.__class__.create_with_standard_units(self.value * float(other))  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __rmul__(self: ResultT, other: "float | int") -> ResultT | "Result":
        if isinstance(other, (int, float)):
            return self.__class__.create_with_standard_units(float(other) * self.value)  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __truediv__(self: ResultT, other: "Result | float | int") -> ResultT | "Result":
        if isinstance(other, Result):
            return self._build_typed_result(self.flt - other.flt, self.value / other.value)  # type: ignore[return-value]
        if isinstance(other, (int, float)):
            return self.__class__.create_with_standard_units(self.value / float(other))  # type: ignore[return-value]
        return NotImplemented  # type: ignore[return-value]

    def __rtruediv__(self, other: "float | int") -> "Result":
        if isinstance(other, (int, float)):
            return self._build_typed_result(-self.flt, float(other) / self.value)
        return NotImplemented  # type: ignore[return-value]

    def __neg__(self: ResultT) -> ResultT | "Result":
        return self._build_typed_result(self.flt, -self.value)  # type: ignore[return-value]

    def __pow__(self, exponent: "Result | float | int") -> "Result":
        if isinstance(exponent, Result):
            Result._confirm_unitless(exponent)
            exponent_value = exponent.value
        else:
            exponent_value = float(exponent)

        if float(exponent_value).is_integer():
            return self._build_typed_result(self.flt * int(round(exponent_value)), self.value ** exponent_value)
        else:
            # Non-integer exponent => unitless
            return self._build_typed_result(FLT.UNITLESS, self.value ** exponent_value)

    # ------------------ Factories & utils ------------------
    @classmethod
    def _build_typed_result(cls, flt: FLT, value: float) -> "Result":
        """Build a typed result based on the FLT."""
        unit_type = flt.get_type()

        # Local imports to avoid circular dependencies
        from structunits.specific_units.unitless import Unitless
        from structunits.specific_units.undefined import Undefined

        if unit_type == UnitType.LENGTH:
            from structunits.specific_units.length import Length
            return Length.create_with_standard_units(value)
        if unit_type == UnitType.FORCE:
            from structunits.specific_units.force import Force
            return Force.create_with_standard_units(value)
        if unit_type == UnitType.MOMENT:
            from structunits.specific_units.moment import Moment
            return Moment.create_with_standard_units(value)
        if unit_type == UnitType.FORCE_PER_LENGTH:
            from structunits.specific_units.force_per_length import ForcePerLength
            return ForcePerLength.create_with_standard_units(value)
        if unit_type == UnitType.STRESS:
            from structunits.specific_units.stress import Stress
            return Stress.create_with_standard_units(value)
        if unit_type == UnitType.LENGTH_TO_THE_4TH:
            from structunits.specific_units.length_to_the_4th import LengthToThe4th
            return LengthToThe4th.create_with_standard_units(value)
        if unit_type == UnitType.LENGTH_CUBED:
            from structunits.specific_units.length_cubed import LengthCubed
            return LengthCubed.create_with_standard_units(value)
        if unit_type == UnitType.UNITLESS:
            return Unitless(value)
        return Undefined(flt, value)

    @staticmethod
    def _confirm_units_match(a: "Result", b: "Result") -> None:
        if a.flt != b.flt:
            raise ValueError(f"Expected units to match: {a.flt} vs {b.flt}")

    @staticmethod
    def _confirm_unitless(a: "Result") -> None:
        if a.flt != FLT.UNITLESS:
            raise ValueError("Expected unitless argument")

    # ------------------ Math helpers with explicit annotations ------------------
    @staticmethod
    def sqrt(a: "Result") -> "Result":
        return Result._build_typed_result(a.flt / 2, math.sqrt(a.value))

    @staticmethod
    def third_root(a: "Result") -> "Result":
        return Result._build_typed_result(a.flt / 3, a.value ** (1 / 3))

    @staticmethod
    def fourth_root(a: "Result") -> "Result":
        return Result._build_typed_result(a.flt / 4, a.value ** (1 / 4))

    @staticmethod
    def abs(a: "Result") -> "Result":
        return Result._build_typed_result(a.flt, abs(a.value))

    # ------------------ Min / Max with overloads and narrowing ------------------
    @overload
    @staticmethod
    def min(a: CIterable[ResultT]) -> ResultT: ...
    @overload
    @staticmethod
    def min(a: ResultT, b: ResultT) -> ResultT: ...

    @staticmethod
    def min(a: CIterable[ResultT] | ResultT, b: ResultT | None = None) -> ResultT:
        if b is None:
            if not isinstance(a, CIterable):
                # Single value passed; return it unchanged
                return a
            all_results = list(a)
            if not all_results:
                raise ValueError("Expected at least one value")
            for r in all_results[1:]:
                Result._confirm_units_match(all_results[0], r)
            m = all_results[0]
            for r in all_results[1:]:
                if r.value < m.value:
                    m = r
            return m
        else:
            if isinstance(a, CIterable):
                raise TypeError("When b is provided, 'a' must be a Result, not an Iterable")
            Result._confirm_units_match(a, b)
            return a if a.value < b.value else b

    @overload
    @staticmethod
    def max(a: CIterable[ResultT]) -> ResultT: ...
    @overload
    @staticmethod
    def max(a: ResultT, b: ResultT) -> ResultT: ...

    @staticmethod
    def max(a: CIterable[ResultT] | ResultT, b: ResultT | None = None) -> ResultT:
        if b is None:
            if not isinstance(a, CIterable):
                return a
            all_results = list(a)
            if not all_results:
                raise ValueError("Expected at least one value")
            for r in all_results[1:]:
                Result._confirm_units_match(all_results[0], r)
            m = all_results[0]
            for r in all_results[1:]:
                if r.value > m.value:
                    m = r
            return m
        else:
            if isinstance(a, CIterable):
                raise TypeError("When b is provided, 'a' must be a Result, not an Iterable")
            Result._confirm_units_match(a, b)
            return a if a.value > b.value else b

    # ------------------ Envelopes ------------------
    @overload
    @staticmethod
    def absolute_value_envelope(a: CIterable[ResultT]) -> ResultT: ...
    @overload
    @staticmethod
    def absolute_value_envelope(a: ResultT, b: ResultT) -> ResultT: ...

    @staticmethod
    def absolute_value_envelope(a: CIterable[ResultT] | ResultT, b: ResultT | None = None) -> ResultT:
        if b is None:
            if not isinstance(a, CIterable):
                # Single value, just its abs
                return Result.abs(a)  # type: ignore[return-value]
            all_results = list(a)
            if not all_results:
                raise ValueError("Expected at least one value")
            for r in all_results[1:]:
                Result._confirm_units_match(all_results[0], r)
            return Result.max([Result.abs(r) for r in all_results])  # type: ignore[return-value]
        else:
            if isinstance(a, CIterable):
                raise TypeError("When b is provided, 'a' must be a Result, not an Iterable")
            Result._confirm_units_match(a, b)
            return Result.max(Result.abs(a), Result.abs(b))  # type: ignore[return-value]

    @staticmethod
    def absolute_value_signed_envelope(a: "Result", b: "Result") -> "Result":
        Result._confirm_units_match(a, b)
        abs_a = Result.abs(a)
        abs_b = Result.abs(b)
        if abs_a.value > abs_b.value:
            return abs_a * (1 if a.value >= 0 else -1)
        else:
            return abs_b * (1 if b.value >= 0 else -1)

    @staticmethod
    def min_value_envelope(a: "Result", b: "Result") -> "Result":
        return Result.min(a, b)

    @staticmethod
    def max_value_envelope(a: "Result", b: "Result") -> "Result":
        return Result.max(a, b)


__all__ = ["Result"]
