from __future__ import annotations

from enum import Enum


class UnitType(Enum):
    """Enumeration of unit types for different physical quantities."""
    
    UNITLESS = "unitless"
    FORCE = "force"
    LENGTH = "length"
    AREA = "area"
    LENGTH_CUBED = "length_cubed"
    LENGTH_TO_THE_4TH = "length_to_the_4th"
    MOMENT = "moment"
    FORCE_PER_LENGTH = "force_per_length"
    STRESS = "stress"
    UNDEFINED = "undefined"

__all__ = ["UnitType"]