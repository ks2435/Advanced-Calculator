import builtins
import pytest
from app import main


def test_help_and_exit(monkeypatch, capsys):
    inputs = iter(["help", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out


def test_add_command(monkeypatch, capsys):
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    assert "5" in captured.out

def test_history_and_clear(monkeypatch, capsys):
    inputs = iter([
        "add 1 2",
        "history",
        "clear",
        "history",
        "exit"
    ])

    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    main()

    output = capsys.readouterr().out
    assert "3" in output

def _run_repl(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(it))
    main()


def test_repl_usage_error(monkeypatch, capsys):
    _run_repl(monkeypatch, ["add 1", "exit"])
    out = capsys.readouterr().out
    assert "Usage:" in out


def test_repl_unknown_command_error(monkeypatch, capsys):
    # Unknown operation triggers CalculatorError -> printed as "Error: ..."
    _run_repl(monkeypatch, ["not_real 1 2", "exit"])
    out = capsys.readouterr().out
    assert "Error:" in out


def test_repl_save_then_load(monkeypatch, capsys, tmp_path):
    # Force config to use temp dirs by setting env vars before main() loads config
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "history.csv")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")  # keep deterministic

    _run_repl(monkeypatch, ["add 2 3", "save", "clear", "load", "history", "exit"])
    out = capsys.readouterr().out
    assert "5" in out  # result and/or history output


def test_repl_undo_redo_and_empty_history(monkeypatch, capsys):
    _run_repl(monkeypatch, ["add 1 2", "undo", "redo", "clear", "history", "exit"])
    out = capsys.readouterr().out
    assert "Undo OK." in out
    assert "Redo OK." in out
    assert "(history is empty)" in out


def test_repl_exit_on_eof(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: (_ for _ in ()).throw(EOFError))
    main()
    out = capsys.readouterr().out
    assert "Goodbye." in out