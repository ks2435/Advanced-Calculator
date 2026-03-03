class CalculatorError(Exception):
    """Base exception for calculator application."""


class ValidationError(CalculatorError):
    """Raised when user input is invalid."""


class OperationError(CalculatorError):
    """Raised when an operation fails (domain errors, divide by zero, etc.)."""


class PersistenceError(CalculatorError):
    """Raised when saving/loading history fails."""