from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from .exceptions import ValidationError


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    v = value.strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    raise ValidationError(f"Invalid boolean value: {value}")


def _parse_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(f"Invalid integer value: {value}") from e


@dataclass(frozen=True)
class CalculatorConfig:
    log_dir: Path
    history_dir: Path

    max_history_size: int
    auto_save: bool

    precision: int
    max_input_value: float
    default_encoding: str

    log_file_name: str
    history_file_name: str

    @property
    def log_file_path(self) -> Path:
        return self.log_dir / self.log_file_name

    @property
    def history_file_path(self) -> Path:
        return self.history_dir / self.history_file_name

    @staticmethod
    def load() -> "CalculatorConfig":
        load_dotenv()

        log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", "logs")).resolve()
        history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", "history")).resolve()

        max_history_size = _parse_int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE"), 100)
        auto_save = _parse_bool(os.getenv("CALCULATOR_AUTO_SAVE"), True)

        precision = _parse_int(os.getenv("CALCULATOR_PRECISION"), 6)

        max_input_value_raw = os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
        try:
            max_input_value = float(max_input_value_raw)
        except ValueError as e:
            raise ValidationError(f"Invalid float value: {max_input_value_raw}") from e

        default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        log_file_name = os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
        history_file_name = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")

        # validations
        if max_history_size < 0:
            raise ValidationError("CALCULATOR_MAX_HISTORY_SIZE must be >= 0")
        if precision < 0:
            raise ValidationError("CALCULATOR_PRECISION must be >= 0")
        if max_input_value <= 0:
            raise ValidationError("CALCULATOR_MAX_INPUT_VALUE must be > 0")

        return CalculatorConfig(
            log_dir=log_dir,
            history_dir=history_dir,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding,
            log_file_name=log_file_name,
            history_file_name=history_file_name,
        )