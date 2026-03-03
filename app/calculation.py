from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()