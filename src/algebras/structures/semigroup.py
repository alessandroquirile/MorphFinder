from collections.abc import Callable
from typing import Any

from src.algebras.axioms.associativity import AssociativityAxiom
from src.algebras.structures.magma import Magma


class Semigroup(Magma):
    """An associative Magma."""

    def __init__(self, elements: set[Any], operation: Callable[[Any, Any], Any]):
        super().__init__(elements=elements, operation=operation)
        self.axioms = super().axioms + [AssociativityAxiom()]
        self.validate(self.validator)
