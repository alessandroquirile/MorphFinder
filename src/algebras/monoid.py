from typing import Callable, Optional, Set, Any

from src.algebras.axiom import IdentityExistenceAxiom
from src.algebras.semigroup import Semigroup


class Monoid(Semigroup):
    """A Semigroup with an identity element e."""

    def __init__(self, elements: Set, operation: Callable, identity: Optional[Any] = None):
        super().__init__(elements=elements, operation=operation)
        self.axioms = super().axioms + [IdentityExistenceAxiom()]
        self.validate(self.validator)
        self._identity = identity or super().identity

    @property
    def identity(self) -> Any:
        """Returns the identity element of the monoid."""
        return self._identity

    @property
    def constants(self) -> Set[Any]:
        return {self.identity}
