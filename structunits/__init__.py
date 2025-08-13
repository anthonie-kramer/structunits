"""
structunits: A Python unit conversion framework with operator overloading.
"""

from __future__ import annotations

__version__ = "0.1.0"

# Re-export core things that do NOT cause cycles
from .flt import FLT
from .unit import UnitBase, Unit
from .unit_type import UnitType
from .result import Result
from .utilities import Utilities

# ---- Lazy forwarding of specific_units symbols (NO eager import!) ----
# This lets users do: from structunits import Force, LengthUnit, ...
# without importing the subpackage while structunits itself is still initializing.
import importlib

# Names we want to forward from structunits.specific_units
_FORWARD = [
    # Length and length-derived
    "Length", "LengthUnit",
    "LengthCubed", "LengthCubedUnit",
    "LengthToThe4th", "LengthToThe4thUnit",
    # Force and related
    "Force", "ForceUnit",
    "ForcePerLength", "ForcePerLengthUnit",
    # Moments
    "Moment", "MomentUnit",
    # Stress
    "Stress", "StressUnit",
    # Misc
    "Unitless", "Undefined",
    # Handy aliases (if you export these in specific_units/__init__.py)
    "kip", "lb", "kN", "N",
    "inch", "ft", "mm", "cm", "m",
]

def __getattr__(name: str):
    if name in _FORWARD:
        mod = importlib.import_module("structunits.specific_units")
        return getattr(mod, name)
    raise AttributeError(f"module 'structunits' has no attribute {name!r}")

def __dir__():
    return sorted(list(globals().keys()) + _FORWARD + ["specific_units"])

# Public API
__all__ = [
    # Core
    "FLT", "UnitBase", "Unit", "UnitType", "Result", "Utilities",
    # Subpackage itself (so users can: from structunits import specific_units)
    "specific_units",
] + _FORWARD
