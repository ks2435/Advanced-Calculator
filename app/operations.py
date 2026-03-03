from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Type

from .exceptions import OperationError


class Operation(ABC):
    name: str

    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        raise NotImplementedError


@dataclass(frozen=True)
class OperationMeta:
    key: str
    description: str
    cls: Type[Operation]


class OperationFactory:
    """
    Factory + Decorator Registry
    - @OperationFactory.register("add", "Adds a + b") registers the class.
    - Help menu is generated dynamically from the registry.
    """

    _registry: Dict[str, OperationMeta] = {}

    @classmethod
    def register(cls, key: str, description: str) -> Callable[[Type[Operation]], Type[Operation]]:
        """
        Decorator that registers an Operation class.
        """
        def decorator(op_cls: Type[Operation]) -> Type[Operation]:
            k = key.strip().lower()
            if not k:
                raise ValueError("Operation key cannot be empty.")
            cls._registry[k] = OperationMeta(key=k, description=description, cls=op_cls)
            # keep the class 'name' consistent with the command key
            op_cls.name = k  # type: ignore[attr-defined]
            return op_cls
        return decorator

    @classmethod
    def create(cls, name: str) -> Operation:
        key = name.strip().lower()
        meta = cls._registry.get(key)
        if not meta:
            raise OperationError(f"Unknown operation: {name}")
        return meta.cls()

    @classmethod
    def available_operations(cls) -> list[str]:
        return sorted(cls._registry.keys())

    @classmethod
    def help_entries(cls) -> list[tuple[str, str]]:
        """
        Returns list of (operation_key, description), sorted.
        """
        return sorted(((m.key, m.description) for m in cls._registry.values()), key=lambda x: x[0])


# ----------------------------
# Register Operations via Decorator
# ----------------------------

@OperationFactory.register("add", "Add two numbers: a + b")
class Add(Operation):
    def compute(self, a: float, b: float) -> float:
        return a + b


@OperationFactory.register("subtract", "Subtract two numbers: a - b")
class Subtract(Operation):
    def compute(self, a: float, b: float) -> float:
        return a - b


@OperationFactory.register("multiply", "Multiply two numbers: a * b")
class Multiply(Operation):
    def compute(self, a: float, b: float) -> float:
        return a * b


@OperationFactory.register("divide", "Divide two numbers: a / b (b != 0)")
class Divide(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Division by zero.")
        return a / b


@OperationFactory.register("power", "Power: a ^ b")
class Power(Operation):
    def compute(self, a: float, b: float) -> float:
        return a ** b


@OperationFactory.register("root", "Nth root: root(a, b) = a^(1/b). For negative a, b must be odd integer.")
class Root(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Root with n=0 is undefined.")
        if a < 0:
            if float(b).is_integer() and int(b) % 2 == 1:
                return -((-a) ** (1.0 / b))
            raise OperationError("Even root of a negative number is not a real number.")
        return a ** (1.0 / b)


@OperationFactory.register("modulus", "Remainder: a % b (b != 0)")
class Modulus(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Modulus by zero.")
        return a % b


@OperationFactory.register("int_divide", "Integer division: a // b (b != 0)")
class IntDivide(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Integer division by zero.")
        return float(a // b)


@OperationFactory.register("percent", "Percentage: (a / b) * 100 (b != 0)")
class Percent(Operation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Percentage with divisor 0.")
        return (a / b) * 100.0


@OperationFactory.register("abs_diff", "Absolute difference: |a - b|")
class AbsDiff(Operation):
    def compute(self, a: float, b: float) -> float:
        return abs(a - b)