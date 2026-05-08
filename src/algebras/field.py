from typing import Any, Callable, Optional, Set

from src.algebras.commutative_ring import CommutativeRing
from src.algebras.unity_rings import UnityRing


class Field(CommutativeRing, UnityRing):
    """
    A Field is a Commutative Unity Ring where every non-zero element has a multiplicative inverse.

    Examples:
    (ℚ,+,⋅), (ℝ,+,⋅) are fields.
    ℘(S,△,∩) is a field iff |S|=1.
    """

    def __init__(self, elements: Set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any],
                 unity: Optional[Any] = None):
        super().__init__(elements, add_op, mul_op, unity=unity)

    def validate(self) -> None:
        """Validates ring axioms, commutativity, unity, and existence of inverses."""
        super().validate()

        zero = self.zero
        for a in self.elements:
            if a != zero and not self.is_invertible(a):
                raise ValueError(
                    f"Non-zero element {a} does not have a multiplicative inverse: Structure is not a Field.")
