from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from structunits.unit_type import UnitType


class FLT:
    """
    Force-Length-Time exponents describing physical dimensions.

    Each FLT represents a fundamental physical quantity with its dimensional exponents.
    The tuple format is (force_exp, length_exp, time_exp).

    Examples
    --------
    >>> FLT.FORCE
    FLT(1, 0, 0)
    >>> FLT.LENGTH
    FLT(0, 1, 0)
    >>> FLT.AREA  # L^2
    FLT(0, 2, 0)
    """

    def __init__(self, force_exp: int, length_exp: int, time_exp: int = 0):
        self.force_exp = force_exp
        self.length_exp = length_exp
        self.time_exp = time_exp

    def __repr__(self) -> str:
        return f"FLT({self.force_exp}, {self.length_exp}, {self.time_exp})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FLT):
            return False
        return (
            self.force_exp == other.force_exp
            and self.length_exp == other.length_exp
            and self.time_exp == other.time_exp
        )

    def __hash__(self) -> int:
        return hash((self.force_exp, self.length_exp, self.time_exp))

    def __add__(self, other: "FLT") -> "FLT":
        """Add two FLT instances (for multiplication of quantities)."""
        return FLT(
            self.force_exp + other.force_exp,
            self.length_exp + other.length_exp,
            self.time_exp + other.time_exp,
        )

    def __sub__(self, other: "FLT") -> "FLT":
        """Subtract two FLT instances (for division of quantities)."""
        return FLT(
            self.force_exp - other.force_exp,
            self.length_exp - other.length_exp,
            self.time_exp - other.time_exp,
        )

    def __mul__(self, scalar: int) -> "FLT":
        """Multiply FLT by a scalar (for exponentiation)."""
        return FLT(
            self.force_exp * scalar,
            self.length_exp * scalar,
            self.time_exp * scalar,
        )

    def __truediv__(self, scalar: int) -> "FLT":
        """Divide FLT by a scalar (for roots)."""
        return FLT(
            self.force_exp // scalar,
            self.length_exp // scalar,
            self.time_exp // scalar,
        )

    def __neg__(self) -> "FLT":
        """Negate FLT (for reciprocals)."""
        return FLT(-self.force_exp, -self.length_exp, -self.time_exp)

    def get_type(self) -> "UnitType":
        """Determine the unit type based on the dimensional exponents."""
        from structunits.unit_type import UnitType

        # Check for specific combinations using tuple comparison to avoid circular references
        exponents = (self.force_exp, self.length_exp, self.time_exp)
        
        if exponents == (0, 0, 0):  # UNITLESS
            return UnitType.UNITLESS
        elif exponents == (1, 0, 0):  # FORCE
            return UnitType.FORCE
        elif exponents == (0, 1, 0):  # LENGTH
            return UnitType.LENGTH
        elif exponents == (0, 2, 0):  # AREA (L^2)
            return UnitType.AREA
        elif exponents == (0, 3, 0):  # LENGTH_CUBED (L^3)
            return UnitType.LENGTH_CUBED
        elif exponents == (0, 4, 0):  # LENGTH_TO_THE_4TH (L^4)
            return UnitType.LENGTH_TO_THE_4TH
        elif exponents == (1, 1, 0):  # MOMENT (F*L)
            return UnitType.MOMENT
        elif exponents == (1, -1, 0):  # FORCE_PER_LENGTH (F/L)
            return UnitType.FORCE_PER_LENGTH
        elif exponents == (1, -2, 0):  # STRESS (F/L^2)
            return UnitType.STRESS
        else:
            return UnitType.UNDEFINED

    # Define common FLT instances as class variables with proper type annotations
    UNITLESS: ClassVar["FLT"]
    FORCE: ClassVar["FLT"]
    LENGTH: ClassVar["FLT"]
    AREA: ClassVar["FLT"]
    LENGTH_CUBED: ClassVar["FLT"]
    LENGTH_TO_THE_4TH: ClassVar["FLT"]
    MOMENT: ClassVar["FLT"]
    FORCE_PER_LENGTH: ClassVar["FLT"]
    STRESS: ClassVar["FLT"]


# Initialize the class constants after class definition
FLT.UNITLESS = FLT(0, 0, 0)
FLT.FORCE = FLT(1, 0, 0)
FLT.LENGTH = FLT(0, 1, 0)
FLT.AREA = FLT(0, 2, 0)  # L^2
FLT.LENGTH_CUBED = FLT(0, 3, 0)  # L^3
FLT.LENGTH_TO_THE_4TH = FLT(0, 4, 0)  # L^4
FLT.MOMENT = FLT(1, 1, 0)  # F*L
FLT.FORCE_PER_LENGTH = FLT(1, -1, 0)  # F/L
FLT.STRESS = FLT(1, -2, 0)  # F/L^2

__all__ = ["FLT"]