from typing import Callable, Set

from src.algebras.ring import Ring
from src.algebras.analyzer import StructureAnalyzer


class CommutativeRing(Ring):
    """A Ring where multiplication is commutative."""

    def __init__(self, elements: Set, add_op: Callable, mul_op: Callable):
        super().__init__(elements, add_op, mul_op)

    def validate(self) -> None:
        """Validates ring axioms and multiplicative commutativity."""
        super().validate()
        if not StructureAnalyzer.is_commutative(self.multiplicative_semigroup.op):
            raise ValueError("Commutativity violated: Ring is not commutative.")
