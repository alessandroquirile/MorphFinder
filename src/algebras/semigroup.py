from typing import Any, Callable, Set

from src.algebras.magma import Magma


class Semigroup(Magma):
    """An associative Magma."""

    def validate(self) -> None:
        """Validates closure and associativity."""
        super().validate()
        if not self.is_associative():
            raise ValueError("Associativity violated: Structure is not a Semigroup.")
