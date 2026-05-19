from typing import Any, Callable, Optional, Set

from src.algebras.axiom import IdentityExistenceAxiom, DistributivityAxiom
from src.algebras.monoid import Monoid
from src.algebras.ring import Ring


class UnitalRing(Ring):
    """
    A Unital Ring is a Ring (R,+,⋅) where (R,⋅) is a Monoid
    """

    def __init__(self, elements: Set, add_op: Callable, mul_op: Callable, unity: Optional[Any] = None):
        super().__init__(elements=elements, add_op=add_op, mul_op=mul_op)
        self.multiplicative_semigroup = Monoid(elements, mul_op, unity)
        self.axioms = [DistributivityAxiom(), IdentityExistenceAxiom()]
        self.validate(self.validator)
