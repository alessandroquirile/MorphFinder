from typing import Callable, Optional, Set, Any

from src.algebras.semigroup import Semigroup


class Monoid(Semigroup):
    """A Semigroup with an identity element e."""

    def __init__(self, elements: Set, operation: Callable, identity: Optional[Any] = None):
        self._identity = identity
        super().__init__(elements, operation)

    @property
    def identity(self) -> Any:
        """Returns the identity element of the monoid."""
        return self._identity

    @property
    def constants(self) -> Set[Any]:
        return {self.identity}

    def validate(self) -> None:
        """Validates Semigroup axioms and existence of identity."""
        super().validate()

        if self._identity is None:
            self._identity = super().identity

        if self._identity is None or self._identity not in self.elements:
            raise ValueError("Identity element not found or invalid for Monoid.")
