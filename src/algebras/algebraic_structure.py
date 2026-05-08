from abc import ABC, abstractmethod
from typing import Any, Set, Tuple

from src.algebras.binary_operation import BinaryOperation


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
