from collections.abc import Callable
from typing import Optional, Any

from src.domain.entities.axioms.commutativity import CommutativityAxiom
from src.domain.entities.algebras.group import Group


class AbelianGroup(Group):
    """A commutative Group."""

    def __init__(self, elements: set, operation: Callable[[Any, Any], Any], identity: Optional[Any] = None):
        super().__init__(elements=elements, operation=operation, identity=identity)
        self.axioms = super().axioms + [CommutativityAxiom()]
        self.validate(self.validator)
