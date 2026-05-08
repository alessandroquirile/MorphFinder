import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Set, Tuple


class CayleyTable:
    """
    Handles the data representation of a binary operation.
    Maps (a, b) -> result for elements in the carrier set.
    """

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any]):
        self._table: Dict[Tuple[Any, Any], Any] = {
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

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any]):
        self._elements = frozenset(elements)
        self._operation = operation

        self._validate_arity()
        self._table = CayleyTable(elements, operation)
        self.validate()

    def __call__(self, a: Any, b: Any) -> Any:
        """Evaluates the operation a * b using the Cayley table."""
        return self._table[(a, b)]

    @property
    def table(self) -> CayleyTable:
        return self._table

    def validate(self) -> None:
        """Validates the properties of the binary operation."""
        self._validate_arity()
        self._validate_closure()

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


class AlgebraicStructure(ABC):
    """
    Abstract Base Class for all algebraic structures (S, op1, op2, ..., opn).
    Focuses on readability and proximity to mathematical representation.
    """

    def __init__(self, elements: Set[Any], *operations: BinaryOperation):
        self.elements = frozenset(elements)
        self.operations = tuple(operations)

    def elements(self) -> Set[Any]:
        return set(self.elements)

    def operations(self) -> Tuple[BinaryOperation, ...]:
        return self.operations

    @abstractmethod
    def validate(self) -> None:
        """Validates the axioms of the specific algebraic structure."""
        pass
