from typing import Any, Callable, Set

from src.algebras.abelian_group import AbelianGroup
from src.algebras.base import AlgebraicStructure, BinaryOperation
from src.algebras.semigroup import Semigroup


class Ring(AlgebraicStructure):
    """
    A Ring (R, +, *) is an algebraic structure where:
    1. (R, +) is an Abelian Group.
    2. (R, *) is a Semigroup.
    3. Multiplication distributes over addition.
    """

    def __init__(self, elements: Set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any]):
        self.additive_abelian_group = AbelianGroup(elements, add_op)
        self.multiplicative_semigroup = Semigroup(elements, mul_op)
        super().__init__(elements, self.additive_abelian_group.op, self.multiplicative_semigroup.op)

        self.validate()

    def validate(self) -> None:
        """Validates ring axioms: additive ab. group, multiplicative semigroup, and distributivity."""
        if not self._is_distributive():
            raise ValueError("Distributivity violated: Structure is not a Ring.")

    def _is_distributive(self) -> bool:
        """Checks if multiplication distributes over addition: a*(b+c) = a*b + a*c and (a+b)*c = a*c + b*c."""
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    # Left distributivity: a * (b + c) = (a * b) + (a * c)
                    if self.multiplicative_semigroup.op(a, self.additive_abelian_group.op(b, c)) != self.additive_abelian_group.op(self.multiplicative_semigroup.op(a, b), self.multiplicative_semigroup.op(a, c)):
                        return False
                    # Right distributivity: (a + b) * c = (a * c) + (b * c)
                    if self.multiplicative_semigroup.op(self.additive_abelian_group.op(a, b), c) != self.additive_abelian_group.op(self.multiplicative_semigroup.op(a, c), self.multiplicative_semigroup.op(b, c)):
                        return False
        return True
