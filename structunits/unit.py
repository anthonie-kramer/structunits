from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

class UnitBase:
    """
    Lightweight mixin for unit identity. Safe with Enum.
    NOTE: use 'label' (not 'name') to avoid Enum's reserved .name.
    """
    __slots__ = ("symbol", "label")

    def __init__(self, symbol: str, label: str) -> None:
        self.symbol = symbol
        self.label = label

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbol={self.symbol!r}, label={self.label!r})"

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and getattr(other, "symbol", None) == self.symbol

    def __hash__(self) -> int:
        return hash((type(self), self.symbol))

class Unit(UnitBase, ABC):
    """
    Abstract base for non-Enum units. If your unit has a fixed conversion factor,
    take it in your subclass __init__ and return it from get_conversion_factor().
    """
    __slots__ = ("_conversion_factor",)

    def __init__(self, symbol: str, label: str, conversion_factor: Optional[float] = None) -> None:
        super().__init__(symbol, label)
        self._conversion_factor = conversion_factor  # Optional by design

    @abstractmethod
    def get_conversion_factor(self) -> float:
        """Factor to convert FROM this unit TO the library's standard unit."""
        raise NotImplementedError


__all__ = ["UnitBase", "Unit"]
