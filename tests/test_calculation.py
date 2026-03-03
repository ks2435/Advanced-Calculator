from app.calculation import Calculation


def test_calculation_timestamp_iso():
    ts = Calculation.now_iso()
    assert "T" in ts
    assert ts.endswith("+00:00") or ts.endswith("Z") or "+00:00" in ts