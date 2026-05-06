from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Set, Tuple


class CayleyTable:
    """
    Handles the data representation of a binary operation.
    Maps (a, b) -> result for elements in the carrier set.
    """

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any]):
        self._table = {
            (a, b): operation(a, b) for a in elements for b in elements
        }

    def __getitem__(self, pair: Tuple[Any, Any]) -> Any:
        return self._table[pair]

    def values(self):
        return self._table.values()


class BinaryOperation:
    """
    Responsible for the behavior and evaluation of a binary operation.
    Wraps a Callable and its pre-computed CayleyTable.
    """

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], name: str = "*"):
        self.name = name
        self._operation = operation
        self._table = CayleyTable(elements, operation)

    def __call__(self, a: Any, b: Any) -> Any:
        """Evaluates the operation a * b using the Cayley table."""
        return self._table[(a, b)]

    @property
    def table(self) -> CayleyTable:
        return self._table


class AlgebraicStructure(ABC):
    """
    Abstract Base Class for all algebraic structures (S, op1, op2, ..., opn).
    Focuses on readability and proximity to mathematical representation.
    """

    def __init__(self, elements: Set[Any], *operations: BinaryOperation):
        self._elements = frozenset(elements)
        self._operations = tuple(operations)

    @property
    def elements(self) -> Set[Any]:
        return set(self._elements)

    @property
    def operations(self) -> Tuple[BinaryOperation, ...]:
        return self._operations

    @abstractmethod
    def validate(self) -> None:
        """Validates the axioms of the specific algebraic structure."""
        pass
