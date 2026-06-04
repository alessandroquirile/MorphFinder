import inspect
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from src.algebras.structures.carrier_set import CarrierSet


class CayleyTable:
    """
    Handles the data representation of a binary operation.
    Maps (a, b) -> result for elements in the carrier set.
    """

    def __init__(self, elements: set[Any], operation: Callable[[Any, Any], Any]):
        self._table: dict[tuple[Any, Any], Any] = {
            (a, b): operation(a, b) for a in elements for b in elements
        }

    def __getitem__(self, pair: tuple[Any, Any]) -> Any:
        return self._table[pair]

    def values(self):
        return self._table.values()

    def is_associative(self, elements: set[Any]) -> bool:
        """Checks if the operation is associative: (a*b)*c == a*(b*c)."""
        for a in elements:
            for b in elements:
                for c in elements:
                    if self[(self[(a, b)], c)] != self[(a, self[(b, c)])]:
                        return False
        return True

    def is_commutative(self, elements: set[Any]) -> bool:
        """Checks if the operation is commutative: a*b == b*a."""
        for a in elements:
            for b in elements:
                if self[(a, b)] != self[(b, a)]:
                    return False
        return True

    def find_identity(self, elements: set[Any]) -> Any | None:
        """Returns the identity element if it exists, else None."""
        for e in elements:
            if all(self[(e, a)] == a and self[(a, e)] == a for a in elements):
                return e
        return None


class BinaryOperation(ABC):
    """
    Abstract Base Class for a binary operation.
    Responsible for the behavior and evaluation of a binary operation.
    """

    def __init__(self, carrier: CarrierSet, operation: Callable[[Any, Any], Any]):
        self.carrier = carrier
        self.operation = operation
        self._validate_arity()

    @abstractmethod
    def __call__(self, a: Any, b: Any) -> Any:
        """Evaluates the operation a * b."""
        pass

    @property
    def elements(self) -> set[Any]:
        return self.carrier.elements

    def _validate_arity(self) -> None:
        """Validates that the operation is binary (arity 2)."""
        signature = inspect.signature(self.operation)
        arity = len(signature.parameters)
        if arity != 2:
            raise TypeError(f"Operation must be binary (arity 2), but got arity {arity}.")


class FiniteBinaryOperation(BinaryOperation):
    """
    Implementation of a binary operation for finite structures using a CayleyTable.
    """

    def __init__(self, carrier: CarrierSet, operation: Callable[[Any, Any], Any]):
        super().__init__(carrier, operation)
        self._table = CayleyTable(self.elements, operation)
        self._validate_closure()

    def __call__(self, a: Any, b: Any) -> Any:
        """Evaluates the operation a * b using the Cayley table."""
        return self._table[(a, b)]

    @property
    def table(self) -> CayleyTable:
        return self._table

    def _validate_closure(self) -> None:
        """Validates that the operation is closed on the carrier set."""
        for result in self._table.values():
            if result not in self.carrier:
                raise ValueError(f"Operation is not closed on the given set: result {result} not in S.")
