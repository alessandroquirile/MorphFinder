from typing import Any, Callable, Optional, Set

from src.algebras.group import Group


class AbelianGroup(Group):
    """A commutative Group."""

    def validate(self) -> None:
        """Validates group axioms and commutativity."""
        super().validate()
        if not self.is_commutative():
            raise ValueError("Commutativity violated: Group is not Abelian.")
