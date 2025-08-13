from __future__ import annotations

from typing import ClassVar, Final
from structunits.unit_type import UnitType


class FLT:
    """
    Force-Length-Time exponents describing physical dimensions.

    The tuple (F, L, T) means:
      F = exponent of Force
      L = exponent of Length
      T = exponent of Time

    Examples
    --------
    >>> FORCE == FLT(1, 0, 0)
    True
    >>> (MOMENT / LENGTH) == FORCE
    True
    """

    # ClassVar annotations let IDEs/linters know these are static attributes.
    AREA: ClassVar["FLT"]
    DENSITY: ClassVar["FLT"]
    FORCE: ClassVar["FLT"]
    FORCE_PER_LENGTH: ClassVar["FLT"]
    FLEXURAL_STIFFNESS: ClassVar["FLT"]
    LENGTH: ClassVar["FLT"]
    LENGTH_CUBED: ClassVar["FLT"]
    LENGTH_TO_THE_4TH: ClassVar["FLT"]
    LENGTH_TO_THE_6TH: ClassVar["FLT"]
    MOMENT: ClassVar["FLT"]
    STRESS: ClassVar["FLT"]
    TIME: ClassVar["FLT"]
    UNITLESS: ClassVar["FLT"]
    ACCELERATION: ClassVar["FLT"]

    def __init__(self, force_degree: int, length_degree: int, time_degree: int):
        self.force_degree = int(force_degree)
        self.length_degree = int(length_degree)
        self.time_degree = int(time_degree)

    # ---------- Classification ----------
    def get_type(self) -> UnitType:
        """Map this FLT to a higher-level UnitType (used by factories)."""
        if self == AREA:
            return UnitType.AREA
        if self == DENSITY:
            return UnitType.DENSITY
        if self == FORCE:
            return UnitType.FORCE
        if self == FORCE_PER_LENGTH:
            return UnitType.FORCE_PER_LENGTH
        if self == FLEXURAL_STIFFNESS:
            return UnitType.FLEXURAL_STIFFNESS
        if self == LENGTH:
            return UnitType.LENGTH
        if self == LENGTH_CUBED:
            return UnitType.LENGTH_CUBED
        if self == LENGTH_TO_THE_4TH:
            return UnitType.LENGTH_TO_THE_4TH
        if self == LENGTH_TO_THE_6TH:
            return UnitType.LENGTH_TO_THE_6TH
        if self == MOMENT:
            return UnitType.MOMENT
        if self == STRESS:
            return UnitType.STRESS
        if self == TIME:
            return UnitType.TIME
        if self == UNITLESS:
            return UnitType.UNITLESS
        if self == ACCELERATION:
            return UnitType.ACCELERATION
        return UnitType.UNDEFINED

    # ---------- Equality / hashing ----------
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FLT)
            and self.force_degree == other.force_degree
            and self.length_degree == other.length_degree
            and self.time_degree == other.time_degree
        )

    def __hash__(self) -> int:
        return hash((self.force_degree, self.length_degree, self.time_degree))

    # ---------- Algebra on exponents ----------
    def __add__(self, other: "FLT") -> "FLT":
        if not isinstance(other, FLT):
            return NotImplemented  # type: ignore[return-value]
        return FLT(
            self.force_degree + other.force_degree,
            self.length_degree + other.length_degree,
            self.time_degree + other.time_degree,
        )

    def __sub__(self, other: "FLT") -> "FLT":
        if not isinstance(other, FLT):
            return NotImplemented  # type: ignore[return-value]
        return FLT(
            self.force_degree - other.force_degree,
            self.length_degree - other.length_degree,
            self.time_degree - other.time_degree,
        )

    def __neg__(self) -> "FLT":
        return FLT(-self.force_degree, -self.length_degree, -self.time_degree)

    def __mul__(self, other: int | float) -> "FLT":
        if not isinstance(other, (int, float)):
            return NotImplemented  # type: ignore[return-value]
        F = self.force_degree * other
        L = self.length_degree * other
        T = self.time_degree * other

        # If multiplied by a float, allow near-integers; otherwise return UNITLESS
        def _snap(x: float) -> int | float:
            r = round(x)
            return r if abs(x - r) < 1e-10 else x

        if isinstance(other, float):
            F = _snap(F)
            L = _snap(L)
            T = _snap(T)
            if not all(isinstance(x, int) for x in (F, L, T)):
                return UNITLESS  # fractional exponents → dimensionless result by convention

        return FLT(int(F), int(L), int(T))

    def __rmul__(self, other: int | float) -> "FLT":
        return self.__mul__(other)

    def __truediv__(self, other: int | float) -> "FLT":
        if not isinstance(other, (int, float)):
            return NotImplemented  # type: ignore[return-value]
        F = self.force_degree / other
        L = self.length_degree / other
        T = self.time_degree / other
        if all(abs(x - round(x)) < 1e-10 for x in (F, L, T)):
            return FLT(int(round(F)), int(round(L)), int(round(T)))
        return UNITLESS

    # ---------- Display ----------
    def __str__(self) -> str:
        parts: list[str] = []
        if self.force_degree:
            parts.append("F" if self.force_degree == 1 else f"F^{self.force_degree}")
        if self.length_degree:
            parts.append("L" if self.length_degree == 1 else f"L^{self.length_degree}")
        if self.time_degree:
            parts.append("T" if self.time_degree == 1 else f"T^{self.time_degree}")
        return "·".join(parts) if parts else "1"

    def __repr__(self) -> str:
        return f"FLT({self.force_degree}, {self.length_degree}, {self.time_degree})"


# ----- Module-level singletons (preferred import path) -----
AREA: Final[FLT] = FLT(0, 2, 0)
DENSITY: Final[FLT] = FLT(1, -3, 0)
FORCE: Final[FLT] = FLT(1, 0, 0)
FORCE_PER_LENGTH: Final[FLT] = FLT(1, -1, 0)
FLEXURAL_STIFFNESS: Final[FLT] = FLT(1, 2, 0)
LENGTH: Final[FLT] = FLT(0, 1, 0)
LENGTH_CUBED: Final[FLT] = FLT(0, 3, 0)
LENGTH_TO_THE_4TH: Final[FLT] = FLT(0, 4, 0)
LENGTH_TO_THE_6TH: Final[FLT] = FLT(0, 6, 0)
MOMENT: Final[FLT] = FLT(1, 1, 0)
STRESS: Final[FLT] = FLT(1, -2, 0)
TIME: Final[FLT] = FLT(0, 0, 1)
UNITLESS: Final[FLT] = FLT(0, 0, 0)
ACCELERATION: Final[FLT] = FLT(0, 1, -2)

# ----- Optional: mirror onto the class for backward compatibility -----
FLT.AREA = AREA
FLT.DENSITY = DENSITY
FLT.FORCE = FORCE
FLT.FORCE_PER_LENGTH = FORCE_PER_LENGTH
FLT.FLEXURAL_STIFFNESS = FLEXURAL_STIFFNESS
FLT.LENGTH = LENGTH
FLT.LENGTH_CUBED = LENGTH_CUBED
FLT.LENGTH_TO_THE_4TH = LENGTH_TO_THE_4TH
FLT.LENGTH_TO_THE_6TH = LENGTH_TO_THE_6TH
FLT.MOMENT = MOMENT
FLT.STRESS = STRESS
FLT.TIME = TIME
FLT.UNITLESS = UNITLESS
FLT.ACCELERATION = ACCELERATION

__all__ = [
    # class
    "FLT",
    # preferred module-level singletons
    "AREA",
    "DENSITY",
    "FORCE",
    "FORCE_PER_LENGTH",
    "FLEXURAL_STIFFNESS",
    "LENGTH",
    "LENGTH_CUBED",
    "LENGTH_TO_THE_4TH",
    "LENGTH_TO_THE_6TH",
    "MOMENT",
    "STRESS",
    "TIME",
    "UNITLESS",
    "ACCELERATION",
]
