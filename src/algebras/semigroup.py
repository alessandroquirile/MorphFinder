from collections.abc import Callable
from typing import Any

from src.algebras.axiom import AssociativityAxiom
from src.algebras.magma import Magma


class Semigroup(Magma):
    """An associative Magma."""

    def __init__(self, elements: set[Any], operation: Callable[[Any, Any], Any]):
        super().__init__(elements=elements, operation=operation)
        self.axioms = self.axioms + [AssociativityAxiom()]
        self.validate(self.validator)
