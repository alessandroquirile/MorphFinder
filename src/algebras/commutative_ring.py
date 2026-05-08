from typing import Any, Callable, Set

from src.algebras.ring import Ring


class CommutativeRing(Ring):
    """A Ring where multiplication is commutative."""

    def __init__(self, elements: Set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any],
                 **kwargs):
        super().__init__(elements, add_op, mul_op)

    def validate(self) -> None:
        """Validates ring axioms and multiplicative commutativity."""
        super().validate()
        if not self.is_commutative():
            raise ValueError("Commutativity violated: Ring is not commutative.")
