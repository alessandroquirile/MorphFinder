from typing import Any, Callable, Dict, Optional, Set

from src.algebras.monoid import Monoid


class Group(Monoid):
    """A Monoid where every element has an inverse."""

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], identity: Optional[Any] = None, op_name: str = "*"):
        self._inverse_map: Dict[Any, Any] = {}
        super().__init__(elements, operation, identity, op_name=op_name)

    @property
    def inverse_map(self) -> Dict[Any, Any]:
        """Returns the mapping of elements to their inverses."""
        return self._inverse_map

    def inverse(self, a: Any) -> Any:
        """Returns the inverse of element a."""
        return self._inverse_map[a]

    def _build_inverse_map(self) -> Dict[Any, Any]:
        """Finds inverses: ∀ a ∈ S, ∃ b ∈ S s.t. a * b = b * a = e."""
        inv_map = {}
        for a in self._elements:
            for b in self._elements:
                if self.op(a, b) == self.identity and self.op(b, a) == self.identity:
                    inv_map[a] = b
                    break
        return inv_map

    def validate(self) -> None:
        """Validates closure, associativity, identity, and inverses."""
        super().validate()
        self._inverse_map = self._build_inverse_map()
        if len(self._inverse_map) != len(self._elements):
            raise ValueError("Inverse elements not found for all elements in the Group.")

    def element_orders(self) -> Dict[Any, int]:
        """
        Computes the order of each element in the group.
        In a finite group, every element has a finite order.
        """
        orders = {}
        for x in self._elements:
            current = x
            order = 1
            while current != self.identity:
                current = self.op(current, x)
                order += 1
            orders[x] = order
        return orders
