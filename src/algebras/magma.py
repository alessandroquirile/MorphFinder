from typing import Any, Callable, Set

from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.binary_operation import BinaryOperation


class Magma(AlgebraicStructure):
    """
    A Magma (S, *) consists of a set S and a single binary operation *.
    """

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any]):
        self.op = BinaryOperation(elements, operation)
        super().__init__(elements, self.op)

        self.validate()

    def validate(self) -> None:
        """ Nothing to validate."""
        pass
