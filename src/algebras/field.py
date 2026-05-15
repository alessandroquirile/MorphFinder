from typing import Any, Callable, Optional, Set

from src.algebras.commutative_ring import CommutativeRing
from src.algebras.unital_ring import UnitalRing
from src.algebras.analyzer import StructureAnalyzer


class Field(CommutativeRing, UnitalRing):
    """
    A Field is a Commutative Unital Ring where every non-zero element has a multiplicative inverse.

    Examples:
    (ℚ,+,⋅), (ℝ,+,⋅) are fields.
    ℘(S,△,∩) is a field iff |S|=1.
    """

    def __init__(self, elements: Set, add_op: Callable, mul_op: Callable, unity: Optional[Any] = None):
        UnitalRing.__init__(self, elements, add_op, mul_op, unity=unity)
        CommutativeRing.__init__(self, elements, add_op, mul_op)

    def validate(self) -> None:
        """Validates ring axioms, commutativity, unity, and existence of inverses."""
        super().validate()
        zero = self.zero
        for a in self.elements:
            if a != zero and not StructureAnalyzer.is_invertible(self, a):
                raise ValueError(
                    f"Non-zero element {a} does not have a multiplicative inverse: Structure is not a Field.")
