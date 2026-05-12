import inspect
from typing import Callable, Dict, Set, Tuple, Any


class CayleyTable:
    """
    Handles the data representation of a binary operation.
    Maps (a, b) -> result for elements in the carrier set.
    """

    def __init__(self, elements: Set, operation: Callable):
        self._table: Dict[Tuple, Any] = {
            (a, b): operation(a, b) for a in elements for b in elements
        }

    def __getitem__(self, pair: Tuple) -> Any:
        return self._table[pair]

    def values(self):
        return self._table.values()


class BinaryOperation:
    """
    Responsible for the behavior and evaluation of a binary operation.
    Wraps a Callable and its pre-computed CayleyTable.
    """

    def __init__(self, elements: Set, operation: Callable):
        self._elements = frozenset(elements)
        self._operation = operation
        self._validate_arity()
        self._table = CayleyTable(elements, operation)
        self._validate_closure()

    def __call__(self, a: Any, b: Any) -> Any:
        """Evaluates the operation a * b using the Cayley table."""
        return self._table[(a, b)]

    @property
    def table(self) -> CayleyTable:
        return self._table

    def _validate_arity(self) -> None:
        """Validates that the operation is binary (arity 2)."""
        signature = inspect.signature(self._operation)
        arity = len(signature.parameters)
        if arity != 2:
            raise TypeError(f"Operation must be binary (arity 2), but got arity {arity}.")

    def _validate_closure(self) -> None:
        """Validates that the operation is closed on the carrier set."""
        for result in self._table.values():
            if result not in self._elements:
                raise ValueError(f"Operation is not closed on the given set: result {result} not in S.")
