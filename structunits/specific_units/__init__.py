"""Public exports for all specific unit classes.

This makes `from structunits.specific_units import *` bring all classes into scope.
"""

# Length and length-derived
from .length import Length
from .length_unit import LengthUnit
from .length_cubed import LengthCubed
from .length_cubed_unit import LengthCubedUnit
from .length_to_the_4th import LengthToThe4th
from .length_to_the_4th_unit import LengthToThe4thUnit

# Force and related
from .force import Force
from .force_unit import ForceUnit
from .force_per_length import ForcePerLength
from .force_per_length_unit import ForcePerLengthUnit

# Moments
from .moment import Moment
from .moment_unit import MomentUnit

# Stress
from .stress import Stress
from .stress_unit import StressUnit

# Misc
from .unitless import Unitless
from .undefined import Undefined

from typing import Final
kip:  Final[ForceUnit] = ForceUnit.KIP
kips: Final[ForceUnit] = ForceUnit.KIP
lb:   Final[ForceUnit] = ForceUnit.POUND
kN:   Final[ForceUnit] = ForceUnit.KILONEWTON
N:    Final[ForceUnit] = ForceUnit.NEWTON
inch: Final[LengthUnit] = LengthUnit.INCH
ft:   Final[LengthUnit] = LengthUnit.FOOT
foot: Final[LengthUnit] = LengthUnit.FOOT
mm:   Final[LengthUnit] = LengthUnit.MILLIMETER
cm:   Final[LengthUnit] = LengthUnit.CENTIMETER
m:    Final[LengthUnit] = LengthUnit.METER

__all__: list[str] = [
    "Length", "LengthUnit",
    "LengthCubed", "LengthCubedUnit",
    "LengthToThe4th", "LengthToThe4thUnit",
    "Force", "ForceUnit",
    "ForcePerLength", "ForcePerLengthUnit",
    "Moment", "MomentUnit",
    "Stress", "StressUnit",
    "Unitless", "Undefined",
    "kip", "kips", "lb", "kN", "N",
    "inch", "ft", "foot", "mm", "cm", "m",
]


