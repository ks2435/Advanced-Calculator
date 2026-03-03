# Advanced Calculator

![Python CI](https://github.com/ks2435/Advanced-Calculator/actions/workflows/python-app.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

## Project Overview

The **Advanced Calculator** is a Python-based command-line application that performs arithmetic calculations with extended functionality. The system supports multiple arithmetic operations, maintains calculation history, implements undo/redo functionality, logs events, and automatically saves history to CSV files.

The project demonstrates several software engineering design patterns including:

- Factory Pattern – Used to create operation instances dynamically.
- Memento Pattern – Used to implement undo and redo functionality.
- Observer Pattern – Used for logging and automatic history saving.
- Decorator Pattern (Optional Feature) – Used to dynamically generate the help menu from registered operations.

The calculator is implemented with modular design principles, strong error handling, and automated testing with CI/CD integration.

---

## Features

### Arithmetic Operations

The calculator supports the following operations:

| Operation | Description |
|-----------|-------------|
| add | Adds two numbers |
| subtract | Subtracts two numbers |
| multiply | Multiplies two numbers |
| divide | Divides two numbers |
| power | Raises a number to a power |
| root | Calculates the nth root of a number |
| modulus | Computes remainder of division |
| int_divide | Performs integer division |
| percent | Calculates percentage `(a / b) * 100` |
| abs_diff | Calculates absolute difference |

Each operation accepts **exactly two numeric inputs**.

---

## Command Line Interface (REPL)

The calculator uses a **Read–Eval–Print Loop (REPL)** interface.

Start the calculator:

```bash
python -m app
```

Example usage:

```
> add 2 3
5

> power 2 8
256

> history
1. add(2, 3) = 5
```

---

## Available Commands

### Operations

```
add a b
subtract a b
multiply a b
divide a b
power a b
root a b
modulus a b
int_divide a b
percent a b
abs_diff a b
```

### Other Commands

```
history     Show calculation history
clear       Clear calculation history
undo        Undo last calculation
redo        Redo last undone calculation
save        Save history to CSV
load        Load history from CSV
help        Show help menu
exit        Exit application
```

---

## Configuration

Application configuration is managed using a `.env` file with the **python-dotenv** package.

Example `.env` file:

```
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=history.csv
```

Configuration controls:

- log file location
- history file location
- history size
- automatic history saving
- precision of calculations
- maximum allowed input values

---

## History Persistence

The calculator stores history using **pandas DataFrames**.

History files include:

| Column | Description |
|--------|-------------|
| operation | operation name |
| a | first operand |
| b | second operand |
| result | computed result |
| timestamp | calculation time |

History can be saved or loaded using:

```
save
load
```

---

## Undo and Redo (Memento Pattern)

The application uses the **Memento Pattern** to support undo and redo operations.

Commands:

```
undo
redo
```

This allows users to revert or restore previous calculations.

---

## Logging (Observer Pattern)

All calculations are logged using Python's `logging` module.

Example log entry:

```
calc | op=add a=2 b=3 result=5 ts=2026-03-04T10:15:32
```

Logs are written to the directory defined in the `.env` configuration.

---

## Dynamic Help Menu (Decorator Pattern)

The help menu is dynamically generated using the **Decorator Pattern**.

Operations register themselves using a decorator:

```python
@OperationFactory.register("add", "Add two numbers")
class Add(Operation):
```

This means:

- Adding a new operation automatically updates the help menu.
- No manual changes to the help system are required.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ks2435/Advanced-Calculator.git
cd Advanced-Calculator
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

- pandas
- python-dotenv
- pytest
- pytest-cov

---

## Running the Application

Start the calculator:

```bash
python -m app
```

---

## Running Tests

Unit tests are implemented using **pytest**.

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-fail-under=90
```

The project enforces **minimum 90% test coverage**.

---

## Continuous Integration (CI/CD)

GitHub Actions automatically runs tests on every push.

Workflow steps:

1. Checkout repository
2. Setup Python environment
3. Install dependencies
4. Run pytest
5. Enforce 90% coverage requirement

Workflow file location:

```
.github/workflows/python-app.yml
```

---

## Project Structure

```
project_root/

app/
 ├── __init__.py
 ├── __main__.py
 ├── calculator.py
 ├── calculator_config.py
 ├── calculator_memento.py
 ├── calculation.py
 ├── exceptions.py
 ├── history.py
 ├── input_validators.py
 ├── logger.py
 └── operations.py

tests/
 ├── __init__.py
 ├── test_calculator.py
 ├── test_operations.py
 └── test_calculation.py

.github/workflows/
 └── python-app.yml

requirements.txt
.env
README.md
```

---

## Design Principles

This project follows software engineering best practices:

- DRY Principle – Avoids duplicate logic across modules
- Modular Design – Each component has a single responsibility
- Error Handling – Custom exceptions provide meaningful error messages
- Logging – System activity is recorded for debugging and auditing
- Automated Testing – High test coverage ensures reliability

---

## Author

Kamalesh S  
Advanced Calculator Project