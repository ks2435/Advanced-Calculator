from __future__ import annotations

from .calculator import Calculator
from .calculator_config import CalculatorConfig
from .exceptions import CalculatorError
from .logger import Logger

from colorama import Fore, Style, init
init(autoreset=True)

def main() -> None:
    """
    Entry-point REPL.
    Run with: python -m app
    """
    config = CalculatorConfig.load()
    logger = Logger(config)
    calc = Calculator(config=config, logger=logger)

    print("Advanced Calculator REPL. Type 'help' for commands.")

    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()

            if cmd in {"exit", "quit"}:
                print("Goodbye.")
                return

            if cmd == "help":
                print(calc.help_text())
                continue

            if cmd == "history":
                hist = calc.history_list()
                if not hist:
                    print("(history is empty)")
                else:
                    for i, c in enumerate(hist, start=1):
                        print(f"{i}. {c.operation}({c.a}, {c.b}) = {c.result} @ {c.timestamp}")
                continue

            if cmd == "clear":
                calc.clear_history()
                print("History cleared.")
                continue

            if cmd == "undo":
                calc.undo()
                print("Undo OK.")
                continue

            if cmd == "redo":
                calc.redo()
                print("Redo OK.")
                continue

            if cmd == "save":
                calc.save_history()
                print(f"Saved history to {config.history_file_path}")
                continue

            if cmd == "load":
                calc.load_history()
                print(f"Loaded history from {config.history_file_path}")
                continue

            # otherwise treat as operation command
            if len(parts) != 3:
                print("Usage: <operation> <a> <b>  (example: add 2 3)")
                continue

            a_s, b_s = parts[1], parts[2]
            calculation = calc.calculate(cmd, a_s, b_s)
            print(f"{calculation.result}")

        except CalculatorError as e:
            # user-friendly errors
            print(f"Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            return
        except Exception as e:  # pragma: no cover
            # unexpected errors
            print(f"Unexpected error: {e}")


if __name__ == "__main__":  # pragma: no cover
    main()