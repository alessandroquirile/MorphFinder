from typing import Any, Callable, Dict, Optional, Set

from src.algebras.semigroup import Semigroup


class Monoid(Semigroup):
    """A Semigroup with an identity element e."""

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], identity: Optional[Any] = None):
        self._identity = identity
        super().__init__(elements, operation)

    @property
    def identity(self) -> Any:
        """Returns the identity element of the monoid."""
        return self._identity

    def validate(self) -> None:
        """Validates Semigroup axioms and existence of identity."""
        super().validate()

        if self._identity is None:
            self._identity = self._find_identity()

        if self._identity is None or self._identity not in self.elements:
            raise ValueError("Identity element not found or invalid for Monoid.")

    def element_orders(self) -> Dict[Any, Optional[int]]:
        """
        Computes the order of each element in the monoid.
        The order of x is the smallest n > 0 such that x^n = e.
        """
        orders = {}
        for x in self.elements:
            current = x
            order = 1
            seen = {x}
            while current != self.identity:
                current = self.op(current, x)
                order += 1
                if current in seen and current != self.identity:
                    order = None
                    break
                seen.add(current)
            orders[x] = order
        return orders

    def _find_identity(self) -> Optional[Any]:
        """Finds the identity element e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a."""
        for e in self.elements:
            is_identity = True
            for a in self.elements:
                if self.op(e, a) != a or self.op(a, e) != a:
                    is_identity = False
                    break
            if is_identity:
                return e
        return None
