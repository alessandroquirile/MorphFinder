import itertools
from typing import Any, Callable, Set

from src.algebras.base import AlgebraicStructure, BinaryOperation


class Magma(AlgebraicStructure):
    """
    A Magma (S, *) consists of a set S and a single binary operation *.
    """

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any]):
        self.op = BinaryOperation(elements, operation)
        super().__init__(elements, self.op)

        self.validate()

    def validate(self) -> None:
        """ Nothing to validate."""
        pass

    def idempotents(self) -> Set[Any]:
        """Returns the set of idempotent elements: {x ∈ S | x * x = x}."""
        return {x for x in self.elements if self.op(x, x) == x}

    def center(self) -> Set[Any]:
        """Returns the center of the magma: {c ∈ S | ∀ x ∈ S, c * x = x * c}."""
        return {
            c
            for c in self.elements
            if all(self.op(c, x) == self.op(x, c) for x in self.elements)
        }

    def find_generating_set(self) -> Set[Any]:
        """
        Finds a minimal set of generators G ⊆ S such that the closure of G under op is S.
        """
        sorted_elements = sorted(list(self.elements), key=str)

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
        return generated == self.elements
