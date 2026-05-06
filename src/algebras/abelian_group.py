from typing import Any, Callable, Optional, Set

from src.algebras.group import Group


class AbelianGroup(Group):
    """A commutative Group."""

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], identity: Optional[Any] = None):
        super().__init__(elements, operation, identity)
        self.validate()

    def validate(self) -> None:
        """Validates group axioms and commutativity."""
        super().validate()
        if not self.is_commutative():
            raise ValueError("Commutativity violated: Group is not Abelian.")

    def is_commutative(self) -> bool:
        """Checks ∀ a, b ∈ S, a * b = b * a."""
        for a in self.elements:
            for b in self.elements:
                if self.op(a, b) != self.op(b, a):
                    return False
        return True
