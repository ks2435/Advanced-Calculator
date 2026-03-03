from pathlib import Path
from app.history import History
from app.calculation import Calculation


def test_history_save_and_load(tmp_path: Path):
    history = History(max_size=10)

    calc = Calculation(
        operation="add",
        a=1,
        b=2,
        result=3,
        timestamp="now"
    )

    history.add(calc)

    file = tmp_path / "history.csv"

    history.save_csv(file)

    new_history = History(max_size=10)
    new_history.load_csv(file)

    assert len(new_history.items) == 1
    assert new_history.items[0].result == 3

from pathlib import Path
import pandas as pd
import pytest

from app.history import History
from app.calculation import Calculation
from app.exceptions import PersistenceError


def test_history_max_size_zero_clears():
    h = History(max_size=0)
    h.add(Calculation("add", 1, 2, 3, "t"))
    assert h.items == []


def test_from_dataframe_missing_column_raises():
    df = pd.DataFrame([{"operation": "add", "a": 1, "b": 2, "result": 3}])  # missing timestamp
    with pytest.raises(PersistenceError):
        History.from_dataframe(df, max_size=10)


def test_save_csv_failure(monkeypatch, tmp_path: Path):
    h = History(max_size=10)
    h.add(Calculation("add", 1, 2, 3, "t"))
    bad_path = tmp_path / "history.csv"

    # Force pandas to raise to hit PersistenceError branch
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")))
    with pytest.raises(PersistenceError):
        h.save_csv(bad_path)


def test_load_csv_malformed(monkeypatch, tmp_path: Path):
    h = History(max_size=10)
    p = tmp_path / "history.csv"

    # Force pandas read_csv to raise generic error
    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("bad csv")))
    with pytest.raises(PersistenceError):
        h.load_csv(p)