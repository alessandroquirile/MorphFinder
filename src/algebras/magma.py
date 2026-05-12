from typing import Callable, Set, Any, Optional

from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.binary_operation import BinaryOperation


class Magma(AlgebraicStructure):
    """
    A Magma (S, *) consists of a set S and a single binary operation *.
    """

    def __init__(self, elements: Set, operation: Callable):
        self.op = BinaryOperation(elements, operation)
        super().__init__(elements, self.op)
        self.validate()

    def validate(self) -> None:
        """ Nothing to validate."""
        pass

    @property
    def identity(self) -> Optional[Any]:
        """Returns the identity element e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a."""
        for e in self.elements:
            if all(self.op(e, a) == a and self.op(a, e) == a for a in self.elements):
                return e
        return None
