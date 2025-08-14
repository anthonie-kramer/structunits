"""Public exports for all specific unit classes.

This makes `from structunits.specific_units import *` bring all classes into scope.
"""

# Length and length-derived
from .length import Length
from .length_unit import LengthUnit
from .area import Area
from .area_unit import AreaUnit
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

# Force unit aliases
kip:  Final[ForceUnit] = ForceUnit.KIP
kips: Final[ForceUnit] = ForceUnit.KIP
lb:   Final[ForceUnit] = ForceUnit.POUND
lbs:  Final[ForceUnit] = ForceUnit.POUND
pound: Final[ForceUnit] = ForceUnit.POUND
pounds: Final[ForceUnit] = ForceUnit.POUND
kN:   Final[ForceUnit] = ForceUnit.KILONEWTON
N:    Final[ForceUnit] = ForceUnit.NEWTON

# Length unit aliases
inch: Final[LengthUnit] = LengthUnit.INCH
inches: Final[LengthUnit] = LengthUnit.INCH
ft:   Final[LengthUnit] = LengthUnit.FOOT
foot: Final[LengthUnit] = LengthUnit.FOOT
feet: Final[LengthUnit] = LengthUnit.FOOT
mm:   Final[LengthUnit] = LengthUnit.MILLIMETER
cm:   Final[LengthUnit] = LengthUnit.CENTIMETER
m:    Final[LengthUnit] = LengthUnit.METER
meter: Final[LengthUnit] = LengthUnit.METER
meters: Final[LengthUnit] = LengthUnit.METER

# Area unit aliases
in2:  Final[AreaUnit] = AreaUnit.SQUARE_INCH
ft2:  Final[AreaUnit] = AreaUnit.SQUARE_FOOT
mm2:  Final[AreaUnit] = AreaUnit.SQUARE_MILLIMETER
cm2:  Final[AreaUnit] = AreaUnit.SQUARE_CENTIMETER
m2:   Final[AreaUnit] = AreaUnit.SQUARE_METER
sq_in: Final[AreaUnit] = AreaUnit.SQUARE_INCH
sq_ft: Final[AreaUnit] = AreaUnit.SQUARE_FOOT
sq_mm: Final[AreaUnit] = AreaUnit.SQUARE_MILLIMETER
sq_cm: Final[AreaUnit] = AreaUnit.SQUARE_CENTIMETER
sq_m:  Final[AreaUnit] = AreaUnit.SQUARE_METER

# Volume unit aliases
in3:  Final[LengthCubedUnit] = LengthCubedUnit.INCHES_CUBED
ft3:  Final[LengthCubedUnit] = LengthCubedUnit.FEET_CUBED
mm3:  Final[LengthCubedUnit] = LengthCubedUnit.MILLIMETERS_CUBED
cm3:  Final[LengthCubedUnit] = LengthCubedUnit.CENTIMETERS_CUBED
m3:   Final[LengthCubedUnit] = LengthCubedUnit.METERS_CUBED

# Length^4 unit aliases (for moment of inertia)
in4:  Final[LengthToThe4thUnit] = LengthToThe4thUnit.INCHES_TO_THE_4TH
ft4:  Final[LengthToThe4thUnit] = LengthToThe4thUnit.FEET_TO_THE_4TH
mm4:  Final[LengthToThe4thUnit] = LengthToThe4thUnit.MILLIMETERS_TO_THE_4TH
cm4:  Final[LengthToThe4thUnit] = LengthToThe4thUnit.CENTIMETERS_TO_THE_4TH
m4:   Final[LengthToThe4thUnit] = LengthToThe4thUnit.METERS_TO_THE_4TH

# Moment unit aliases
lb_in: Final[MomentUnit] = MomentUnit.POUND_INCH
lb_ft: Final[MomentUnit] = MomentUnit.POUND_FOOT
k_in:  Final[MomentUnit] = MomentUnit.KIP_INCH
k_ft:  Final[MomentUnit] = MomentUnit.KIP_FOOT
kip_in: Final[MomentUnit] = MomentUnit.KIP_INCH
kip_ft: Final[MomentUnit] = MomentUnit.KIP_FOOT
N_m:   Final[MomentUnit] = MomentUnit.NEWTON_METER
kN_m:  Final[MomentUnit] = MomentUnit.KILONEWTON_METER
N_mm:  Final[MomentUnit] = MomentUnit.NEWTON_MILLIMETER
kN_mm: Final[MomentUnit] = MomentUnit.KILONEWTON_MILLIMETER
N_cm:  Final[MomentUnit] = MomentUnit.NEWTON_CENTIMETER
kN_cm: Final[MomentUnit] = MomentUnit.KILONEWTON_CENTIMETER

# Stress unit aliases
psi:  Final[StressUnit] = StressUnit.PSI
ksi:  Final[StressUnit] = StressUnit.KSI
psf:  Final[StressUnit] = StressUnit.PSF
ksf:  Final[StressUnit] = StressUnit.KSF
Pa:   Final[StressUnit] = StressUnit.PA
kPa:  Final[StressUnit] = StressUnit.KPA
MPa:  Final[StressUnit] = StressUnit.MPA

# Force per length unit aliases
lb_per_in: Final[ForcePerLengthUnit] = ForcePerLengthUnit.POUND_PER_INCH
lb_per_ft: Final[ForcePerLengthUnit] = ForcePerLengthUnit.POUND_PER_FOOT
k_per_in:  Final[ForcePerLengthUnit] = ForcePerLengthUnit.KIP_PER_INCH
k_per_ft:  Final[ForcePerLengthUnit] = ForcePerLengthUnit.KIP_PER_FOOT
kip_per_in: Final[ForcePerLengthUnit] = ForcePerLengthUnit.KIP_PER_INCH
kip_per_ft: Final[ForcePerLengthUnit] = ForcePerLengthUnit.KIP_PER_FOOT
N_per_m:   Final[ForcePerLengthUnit] = ForcePerLengthUnit.NEWTON_PER_METER
kN_per_m:  Final[ForcePerLengthUnit] = ForcePerLengthUnit.KILONEWTON_PER_METER
N_per_mm:  Final[ForcePerLengthUnit] = ForcePerLengthUnit.NEWTON_PER_MILLIMETER
kN_per_mm: Final[ForcePerLengthUnit] = ForcePerLengthUnit.KILONEWTON_PER_MILLIMETER
N_per_cm:  Final[ForcePerLengthUnit] = ForcePerLengthUnit.NEWTON_PER_CENTIMETER
kN_per_cm: Final[ForcePerLengthUnit] = ForcePerLengthUnit.KILONEWTON_PER_CENTIMETER

__all__: list[str] = [
    # Classes
    "Length", "LengthUnit",
    "Area", "AreaUnit", 
    "LengthCubed", "LengthCubedUnit",
    "LengthToThe4th", "LengthToThe4thUnit",
    "Force", "ForceUnit",
    "ForcePerLength", "ForcePerLengthUnit", 
    "Moment", "MomentUnit",
    "Stress", "StressUnit",
    "Unitless", "Undefined",
    
    # Force unit aliases
    "kip", "kips", "lb", "lbs", "pound", "pounds", "kN", "N",
    
    # Length unit aliases
    "inch", "inches", "ft", "foot", "feet", "mm", "cm", "m", "meter", "meters",
    
    # Area unit aliases
    "in2", "ft2", "mm2", "cm2", "m2", "sq_in", "sq_ft", "sq_mm", "sq_cm", "sq_m",
    
    # Volume unit aliases
    "in3", "ft3", "mm3", "cm3", "m3",
    
    # Length^4 unit aliases
    "in4", "ft4", "mm4", "cm4", "m4",
    
    # Moment unit aliases
    "lb_in", "lb_ft", "k_in", "k_ft", "kip_in", "kip_ft",
    "N_m", "kN_m", "N_mm", "kN_mm", "N_cm", "kN_cm",
    
    # Stress unit aliases
    "psi", "ksi", "psf", "ksf", "Pa", "kPa", "MPa",
    
    # Force per length unit aliases
    "lb_per_in", "lb_per_ft", "k_per_in", "k_per_ft", "kip_per_in", "kip_per_ft",
    "N_per_m", "kN_per_m", "N_per_mm", "kN_per_mm", "N_per_cm", "kN_per_cm",
]


