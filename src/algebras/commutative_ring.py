from collections.abc import Callable
from typing import Any

from src.algebras.axiom import CommutativityAxiom
from src.algebras.ring import Ring


class CommutativeRing(Ring):
    """A Ring where multiplication is commutative."""

    def __init__(self, elements: set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any]):
        super().__init__(elements=elements, add_op=add_op, mul_op=mul_op)
        self.axioms = super().axioms + [CommutativityAxiom()]
        self.validate(self.validator)
