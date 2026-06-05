from typing import Callable, Optional, Any

from src.domain.services.analysis.finite_magma_analyzer import FiniteMagmaAnalyzer
from src.domain.entities.axioms.identity_existence import IdentityExistenceAxiom
from src.domain.entities.algebras.semigroup import Semigroup


class Monoid(Semigroup):
    """A Semigroup with an identity element e."""

    def __init__(self, elements: set[Any], operation: Callable[[Any, Any], Any], identity: Optional[Any] = None):
        super().__init__(elements=elements, operation=operation)
        self.axioms = self.axioms + [IdentityExistenceAxiom()]
        self.validate(self.validator)

        if identity is None:
            analyzer = FiniteMagmaAnalyzer()
            identity = analyzer.find_identity(self)
        self._identity = identity

    @property
    def identity(self) -> Any:
        """Returns the identity element of the monoid."""
        if self._identity is None:
            raise ValueError("Identity element not defined for Monoid.")
        return self._identity

    @property
    def constants(self) -> dict[str, Any]:
        return {"identity": self.identity}
