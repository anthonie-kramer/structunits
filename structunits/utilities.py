# structunits/utilities.py
from __future__ import annotations

from structunits.unit import UnitBase

class Utilities:
    """Utility functions for unit conversion."""

    @staticmethod
    def to_latex_string(value: float, unit: UnitBase | None = None) -> str:
        """
        Convert a value (and optional unit) to a LaTeX-ready string.

        Parameters
        ----------
        value : float
            The numeric value.
        unit : UnitBase | None
            The unit (optional). Works with both class-based units and Enum units.

        Returns
        -------
        str
            LaTeX formatted string, e.g. "12.34 \\, \\mathrm{kip}".
        """
        if unit is None:
            return f"{value:.4g}"
        return f"{value:.4g} \\, \\mathrm{{{unit.symbol}}}"
