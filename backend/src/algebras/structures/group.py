from typing import Callable, Dict, Optional, Set, Any

from src.algebras.axioms.inverse_existence import InverseExistenceAxiom
from src.algebras.structures.monoid import Monoid


class Group(Monoid):
    """A Monoid where every element has an inverse."""

    def __init__(self, elements: Set, operation: Callable, identity: Optional[Any] = None):
        super().__init__(elements=elements, operation=operation, identity=identity)
        self.axioms = super().axioms + [InverseExistenceAxiom()]
        self.validate(self.validator)
        self._inverse_map = self._build_inverse_map()

    @property
    def inverse_map(self) -> Dict:
        """Returns the mapping of elements to their inverses."""
        return self._inverse_map

    def inverse(self, a: Any) -> Any:
        """Returns the inverse of element a."""
        return self._inverse_map[a]

    def _build_inverse_map(self) -> dict:
        """Finds inverses: ∀ a ∈ S, ∃ b ∈ S s.t. a * b = b * a = e."""
        inv_map = {}
        for a in self.carrier.elements:
            for b in self.carrier.elements:
                if self.operation(a, b) == self.identity and self.operation(b, a) == self.identity:
                    inv_map[a] = b
                    break
        return inv_map
