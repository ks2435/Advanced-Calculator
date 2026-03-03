from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .calculation import Calculation
from .exceptions import PersistenceError


COLUMNS = ["operation", "a", "b", "result", "timestamp"]


@dataclass
class History:
    max_size: int
    items: list[Calculation] = field(default_factory=list)

    def add(self, calc: Calculation) -> None:
        self.items.append(calc)
        self._trim()

    def clear(self) -> None:
        self.items.clear()

    def _trim(self) -> None:
        if self.max_size == 0:
            self.items.clear()
            return
        if len(self.items) > self.max_size:
            # trim oldest
            overflow = len(self.items) - self.max_size
            del self.items[:overflow]

    def snapshot(self) -> list[Calculation]:
        # immutable Calculation objects -> shallow copy list is enough
        return list(self.items)

    def restore(self, snapshot: list[Calculation]) -> None:
        self.items = list(snapshot)
        self._trim()

    def to_dataframe(self) -> pd.DataFrame:
        rows = [
            {
                "operation": c.operation,
                "a": c.a,
                "b": c.b,
                "result": c.result,
                "timestamp": c.timestamp,
            }
            for c in self.items
        ]
        return pd.DataFrame(rows, columns=COLUMNS)

    @staticmethod
    def from_dataframe(df: pd.DataFrame, max_size: int) -> "History":
        for col in COLUMNS:
            if col not in df.columns:
                raise PersistenceError(f"CSV missing required column: {col}")

        items: list[Calculation] = []
        for _, row in df.iterrows():
            items.append(
                Calculation(
                    operation=str(row["operation"]),
                    a=float(row["a"]),
                    b=float(row["b"]),
                    result=float(row["result"]),
                    timestamp=str(row["timestamp"]),
                )
            )

        hist = History(max_size=max_size, items=items)
        hist._trim()
        return hist

    def save_csv(self, path: Path, encoding: str = "utf-8") -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            df = self.to_dataframe()
            df.to_csv(path, index=False, encoding=encoding)
        except Exception as e:
            raise PersistenceError(f"Failed to save history to CSV: {e}") from e

    def load_csv(self, path: Path) -> None:
        try:
            df = pd.read_csv(path)
            new_hist = History.from_dataframe(df, max_size=self.max_size)
            self.items = new_hist.items
        except FileNotFoundError as e:
            raise PersistenceError(f"History file not found: {path}") from e
        except Exception as e:
            raise PersistenceError(f"Failed to load history from CSV: {e}") from e