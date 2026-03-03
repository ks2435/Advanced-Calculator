from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .calculator_config import CalculatorConfig
from .calculator_memento import CalculatorMemento
from .calculation import Calculation
from .exceptions import OperationError, ValidationError
from .history import History
from .input_validators import parse_number, validate_range
from .logger import Logger
from .operations import OperationFactory


class Observer(Protocol):
    def update(self, calculation: Calculation, calculator: "Calculator") -> None:
        ...


class LoggingObserver:
    def update(self, calculation: Calculation, calculator: "Calculator") -> None:
        calculator.logger.info(
            f"calc | op={calculation.operation} a={calculation.a} b={calculation.b} "
            f"result={calculation.result} ts={calculation.timestamp}"
        )


class AutoSaveObserver:
    def update(self, calculation: Calculation, calculator: "Calculator") -> None:
        if calculator.config.auto_save:
            calculator.save_history()


@dataclass
class Calculator:
    config: CalculatorConfig
    logger: Logger

    def __post_init__(self) -> None:
        self.history = History(max_size=self.config.max_history_size)
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []
        self._observers: list[Observer] = []

        # register observers
        self.register_observer(LoggingObserver())
        self.register_observer(AutoSaveObserver())

        # ensure dirs exist
        self.config.log_dir.mkdir(parents=True, exist_ok=True)
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("Calculator started.")

    def register_observer(self, obs: Observer) -> None:
        self._observers.append(obs)

    def _notify(self, calculation: Calculation) -> None:
        for obs in self._observers:
            obs.update(calculation, self)

    def _push_undo(self) -> None:
        self._undo_stack.append(CalculatorMemento(self.history.snapshot()))

    def _push_redo(self) -> None:
        self._redo_stack.append(CalculatorMemento(self.history.snapshot()))

    def calculate(self, operation_name: str, a_input: str, b_input: str) -> Calculation:
        a = validate_range(parse_number(a_input), self.config.max_input_value)
        b = validate_range(parse_number(b_input), self.config.max_input_value)

        op = OperationFactory.create(operation_name)
        self.logger.info(f"request | op={operation_name} a={a} b={b}")

        # Save state for undo BEFORE mutating history, then clear redo
        self._push_undo()
        self._redo_stack.clear()

        try:
            result = op.compute(a, b)
        except Exception as e:
            # revert undo push since operation did not succeed
            self._undo_stack.pop()
            self.logger.error(f"operation_failed | op={operation_name} err={e}")
            if isinstance(e, (OperationError, ValidationError)):
                raise
            raise OperationError(str(e)) from e

        # precision rounding
        result = round(float(result), self.config.precision)

        calc = Calculation(
            operation=op.name,
            a=a,
            b=b,
            result=result,
            timestamp=Calculation.now_iso(),
        )
        self.history.add(calc)
        self._notify(calc)
        return calc

    def history_list(self) -> list[Calculation]:
        return list(self.history.items)

    def clear_history(self) -> None:
        self._push_undo()
        self._redo_stack.clear()
        self.history.clear()
        self.logger.info("history_cleared")

    def undo(self) -> None:
        if not self._undo_stack:
            raise OperationError("Nothing to undo.")
        self._push_redo()
        m = self._undo_stack.pop()
        self.history.restore(m.history_snapshot)
        self.logger.info("undo")

    def redo(self) -> None:
        if not self._redo_stack:
            raise OperationError("Nothing to redo.")
        self._push_undo()
        m = self._redo_stack.pop()
        self.history.restore(m.history_snapshot)
        self.logger.info("redo")

    def save_history(self) -> None:
        self.history.save_csv(self.config.history_file_path, encoding=self.config.default_encoding)
        self.logger.info(f"history_saved | path={self.config.history_file_path}")

    def load_history(self) -> None:
        # Loading is also state-changing -> make undoable
        self._push_undo()
        self._redo_stack.clear()
        self.history.load_csv(self.config.history_file_path)
        self.logger.info(f"history_loaded | path={self.config.history_file_path}")

    def help_text(self) -> str:
        entries = OperationFactory.help_entries()
        lines = ["Commands:", ""]

        lines.append("Operations (each takes 2 numbers):")
        for key, desc in entries:
            lines.append(f"  {key:<12} {desc}")

        lines.append("")
        lines.append("Other commands:")
        lines.append("  history       Show calculation history")
        lines.append("  clear         Clear calculation history")
        lines.append("  undo          Undo last calculation")
        lines.append("  redo          Redo last undone calculation")
        lines.append("  save          Save history to CSV")
        lines.append("  load          Load history from CSV")
        lines.append("  help          Show this help menu")
        lines.append("  exit          Exit the application")

        return "\n".join(lines)