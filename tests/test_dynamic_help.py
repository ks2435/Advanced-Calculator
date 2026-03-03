from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.logger import Logger


def test_help_menu_is_dynamic(tmp_path):
    cfg = CalculatorConfig(
        log_dir=tmp_path / "logs",
        history_dir=tmp_path / "history",
        max_history_size=10,
        auto_save=False,
        precision=2,
        max_input_value=1000.0,
        default_encoding="utf-8",
        log_file_name="calc.log",
        history_file_name="history.csv",
    )
    calc = Calculator(config=cfg, logger=Logger(cfg))

    help_text = calc.help_text()
    assert "add" in help_text
    assert "power" in help_text
    assert "abs_diff" in help_text