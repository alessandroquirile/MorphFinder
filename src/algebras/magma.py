import itertools
from typing import Any, Callable, Set

from src.algebras.base import AlgebraicStructure, BinaryOperation


class Magma(AlgebraicStructure):
    """
    A Magma (S, *) consists of a set S and a single binary operation *.
    """

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], op_name: str = "*"):
        self.op = BinaryOperation(elements, operation, name=op_name)
        super().__init__(elements, self.op)
        self.validate()

    def op_bin(self, a: Any, b: Any) -> Any:
        """Applies the binary operation a * b."""
        return self.op(a, b)

    def validate(self) -> None:
        """Validates closure: ∀ a, b ∈ S, a * b ∈ S."""
        for result in self.op.table.values():
            if result not in self._elements:
                raise ValueError(f"Closure violated: {result} is not in the carrier set.")

    def is_associative(self) -> bool:
        """Checks ∀ a, b, c ∈ S, (a * b) * c = a * (b * c)."""
        for a in self._elements:
            for b in self._elements:
                for c in self._elements:
                    if self.op(self.op(a, b), c) != self.op(a, self.op(b, c)):
                        return False
        return True

    def is_commutative(self) -> bool:
        """Checks ∀ a, b ∈ S, a * b = b * a."""
        for a in self._elements:
            for b in self._elements:
                if self.op(a, b) != self.op(b, a):
                    return False
        return True

    def idempotents(self) -> Set[Any]:
        """Returns the set of idempotent elements: {x ∈ S | x * x = x}."""
        return {x for x in self._elements if self.op(x, x) == x}

    def center(self) -> Set[Any]:
        """Returns the center of the magma: {c ∈ S | ∀ x ∈ S, c * x = x * c}."""
        return {
            c
            for c in self._elements
            if all(self.op(c, x) == self.op(x, c) for x in self._elements)
        }

    def find_generating_set(self) -> Set[Any]:
        """
        Finds a minimal set of generators G ⊆ S such that the closure of G under op is S.
        """
        sorted_elements = sorted(list(self._elements), key=str)

        for size in range(1, len(sorted_elements) + 1):
            for subset in itertools.combinations(sorted_elements, size):
                if self._is_generating_set(set(subset)):
                    return set(subset)
        return set(sorted_elements)

    def _is_generating_set(self, subset: Set[Any]) -> bool:
        """Checks if a subset generates the entire carrier set S."""
        generated = set(subset)
        while True:
            new_elements = {
                self.op(a, b) for a in generated for b in generated
            }
            if new_elements.issubset(generated):
                break
            generated.update(new_elements)
        return generated == self._elements
