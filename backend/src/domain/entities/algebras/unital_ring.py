from typing import Any, Callable, Optional, Set

from src.domain.entities.axioms.distributivity import DistributivityAxiom
from src.domain.entities.axioms.identity_existence import IdentityExistenceAxiom
from src.domain.entities.algebras.monoid import Monoid
from src.domain.entities.algebras.ring import Ring


class UnitalRing(Ring):
    """
    A Unital Ring is a Ring (R,+,⋅) where (R,⋅) is a Monoid
    """

    def __init__(self, elements: Set, add_op: Callable, mul_op: Callable, unity: Optional[Any] = None):
        super().__init__(elements=elements, add_op=add_op, mul_op=mul_op)
        self.multiplicative_semigroup = Monoid(elements, mul_op, unity)
        self.axioms = super().axioms + [DistributivityAxiom(), IdentityExistenceAxiom()]
        self.validate(self.validator)

    @property
    def constants(self) -> dict[Any, Any]:
        return {"zero": self.zero, "unity": self.unity}
