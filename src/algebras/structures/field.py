from collections.abc import Callable
from typing import Any, Optional

from src.algebras.axioms.multiplicative_inverses import MultiplicativeInversesAxiom
from src.algebras.structures.commutative_ring import CommutativeRing
from src.algebras.structures.unital_ring import UnitalRing


class Field(CommutativeRing, UnitalRing):
    """
    A Field is a Commutative Unital Ring where every non-zero element has a multiplicative inverse.
    """

    def __init__(self, elements: set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any],
                 unity: Optional[Any] = None):
        UnitalRing.__init__(self, elements, add_op, mul_op, unity=unity)
        CommutativeRing.__init__(self, elements, add_op, mul_op)
        self.axioms = super().axioms + [MultiplicativeInversesAxiom()]
        self.validate(self.validator)
