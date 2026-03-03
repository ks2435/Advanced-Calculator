import os
import pytest
from app.calculator_config import CalculatorConfig, _parse_bool, _parse_int
from app.exceptions import ValidationError


def test_config_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("CALCULATOR_MAX_HISTORY_SIZE", raising=False)

    config = CalculatorConfig.load()

    assert config.max_history_size >= 0
    assert config.precision >= 0
    assert config.max_input_value > 0


def test_config_env_override(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")

    config = CalculatorConfig.load()

    assert config.max_history_size == 50
    assert config.precision == 4


def test_parse_bool_values():
    assert _parse_bool("true", False) is True
    assert _parse_bool("false", True) is False


def test_parse_bool_invalid():
    with pytest.raises(ValidationError):
        _parse_bool("invalid", True)


def test_parse_int_valid():
    assert _parse_int("10", 5) == 10


def test_parse_int_invalid():
    with pytest.raises(ValidationError):
        _parse_int("abc", 5)