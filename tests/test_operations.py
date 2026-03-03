import pytest

from app.exceptions import OperationError
from app.operations import OperationFactory


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add", 2, 3, 5),
        ("subtract", 10, 4, 6),
        ("multiply", 6, 7, 42),
        ("divide", 8, 2, 4),
        ("power", 2, 5, 32),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 1, 4, 25),
        ("abs_diff", 7, 10, 3),
    ],
)
def test_operations_basic(op, a, b, expected):
    operation = OperationFactory.create(op)
    assert operation.compute(a, b) == expected


def test_divide_by_zero():
    operation = OperationFactory.create("divide")
    with pytest.raises(OperationError):
        operation.compute(1, 0)


def test_modulus_by_zero():
    operation = OperationFactory.create("modulus")
    with pytest.raises(OperationError):
        operation.compute(1, 0)


def test_int_divide_by_zero():
    operation = OperationFactory.create("int_divide")
    with pytest.raises(OperationError):
        operation.compute(1, 0)


def test_percent_by_zero():
    operation = OperationFactory.create("percent")
    with pytest.raises(OperationError):
        operation.compute(1, 0)


def test_root_even_of_negative_errors():
    operation = OperationFactory.create("root")
    with pytest.raises(OperationError):
        operation.compute(-16, 2)


def test_root_odd_of_negative_ok():
    operation = OperationFactory.create("root")
    assert operation.compute(-8, 3) == pytest.approx(-2.0)


def test_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create("not_real")