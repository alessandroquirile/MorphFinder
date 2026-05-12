from typing import Callable, Optional, Set, Any

from src.algebras.group import Group


class AbelianGroup(Group):
    """A commutative Group."""

    def __init__(self, elements: Set, operation: Callable, identity: Optional[Any] = None):
        super().__init__(elements, operation, identity)
        self.validate()

    def validate(self) -> None:
        """Validates group axioms and commutativity."""
        super().validate()
        if not self.op.is_commutative:
            raise ValueError("Commutativity violated: Group is not Abelian.")
