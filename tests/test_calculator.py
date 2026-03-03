from pathlib import Path

import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, PersistenceError, ValidationError
from app.logger import Logger




def make_config(tmp_path: Path) -> CalculatorConfig:
    return CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        max_history_size=3,
        auto_save=False,
        precision=6,
        max_input_value=1000.0,
        default_encoding="utf-8",
        log_file_name="calculator.log",
        history_file_name="history.csv",
    )


def test_calculate_and_history(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    c1 = calc.calculate("add", "2", "3")
    assert c1.result == 5
    assert len(calc.history_list()) == 1


def test_history_trims_to_max_size(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    calc.calculate("add", "1", "1")       # 2
    calc.calculate("add", "2", "2")       # 4
    calc.calculate("add", "3", "3")       # 6
    calc.calculate("add", "4", "4")       # 8

    hist = calc.history_list()
    assert len(hist) == 3
    # oldest should be removed -> remaining are 4,6,8
    assert hist[0].result == 4


def test_undo_redo(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    calc.calculate("add", "1", "2")       # 3
    calc.calculate("multiply", "2", "5")  # 10
    assert [c.result for c in calc.history_list()] == [3, 10]

    calc.undo()
    assert [c.result for c in calc.history_list()] == [3]

    calc.redo()
    assert [c.result for c in calc.history_list()] == [3, 10]


def test_undo_empty(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    with pytest.raises(OperationError):
        calc.undo()


def test_redo_empty(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    with pytest.raises(OperationError):
        calc.redo()


def test_validation_invalid_number(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    with pytest.raises(ValidationError):
        calc.calculate("add", "abc", "2")


def test_validation_out_of_range(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    with pytest.raises(ValidationError):
        calc.calculate("add", "2000", "1")  # max_input_value is 1000


def test_save_and_load_history(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    calc.calculate("add", "2", "3")
    calc.calculate("power", "2", "4")
    calc.save_history()

    # new calculator instance loads
    calc2 = Calculator(config=config, logger=logger)
    calc2.load_history()
    results = [c.result for c in calc2.history_list()]
    assert results == [5, 16]


def test_load_missing_file_errors(tmp_path):
    config = make_config(tmp_path)
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    with pytest.raises(PersistenceError):
        calc.load_history()

def test_autosave_observer_writes_file(tmp_path: Path):
    cfg = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        max_history_size=10,
        auto_save=True,              # IMPORTANT: cover autosave branch
        precision=2,
        max_input_value=1000.0,
        default_encoding="utf-8",
        log_file_name="calc.log",
        history_file_name="history.csv",
    )
    logger = Logger(cfg)
    calc = Calculator(config=cfg, logger=logger)

    calc.calculate("add", "1", "2")

    assert cfg.history_file_path.exists()