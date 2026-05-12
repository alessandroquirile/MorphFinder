from typing import Any, Callable, Optional, Set

from src.algebras.monoid import Monoid
from src.algebras.ring import Ring


class UnitalRing(Ring):
    """
    A Unital Ring is a Ring (R,+,⋅) where (R,⋅) is a Monoid
    """

    def __init__(self, elements: Set, add_op: Callable, mul_op: Callable, unity: Optional[Any] = None):
        super().__init__(elements, add_op, mul_op)
        self.multiplicative_semigroup = Monoid(elements, mul_op, unity)
        self.validate()

    def validate(self) -> None:
        """Validates ring axioms and existence of multiplicative identity."""
        super().validate()
        self.multiplicative_semigroup.validate()
        if self.unity is None:
            raise ValueError("Multiplicative identity (unity) not found: Structure is not a Unity Ring.")
