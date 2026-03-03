from __future__ import annotations

import logging
from pathlib import Path

from .calculator_config import CalculatorConfig


class Logger:
    """
    Central logger wrapper. Writes to config.log_file_path.
    """

    def __init__(self, config: CalculatorConfig) -> None:
        self.config = config
        self._logger = logging.getLogger("advanced_calculator")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        # avoid duplicate handlers in tests/REPL reruns
        if not self._logger.handlers:
            self._ensure_dir(config.log_dir)
            fh = logging.FileHandler(config.log_file_path, encoding=config.default_encoding)
            fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            fh.setFormatter(fmt)
            self._logger.addHandler(fh)

    @staticmethod
    def _ensure_dir(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def exception(self, msg: str) -> None:
        self._logger.exception(msg)