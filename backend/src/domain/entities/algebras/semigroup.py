from collections.abc import Callable
from typing import Any

from src.domain.entities.axioms.associativity import AssociativityAxiom
from src.domain.entities.algebras.magma import Magma


class Semigroup(Magma):
    """An associative Magma."""

    def __init__(self, elements: set[Any], operation: Callable[[Any, Any], Any]):
        super().__init__(elements=elements, operation=operation)
        self.axioms = super().axioms + [AssociativityAxiom()]
        self.validate(self.validator)
