from __future__ import annotations

from dataclasses import dataclass

from .calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    history_snapshot: list[Calculation]