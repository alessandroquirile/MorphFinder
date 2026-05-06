from typing import Any, Callable, Set

from src.algebras.abelian_group import AbelianGroup
from src.algebras.base import AlgebraicStructure, BinaryOperation
from src.algebras.semigroup import Semigroup


class Ring(AlgebraicStructure):
    """
    A Ring (S, +, *) is an algebraic structure where:
    1. (S, +) is an Abelian Group.
    2. (S, *) is a Semigroup.
    3. Multiplication distributes over addition.
    """

    def __init__(self, elements: Set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any]):
        self.add = BinaryOperation(elements, add_op, name="+")
        self.mul = BinaryOperation(elements, mul_op, name="*")
        super().__init__(elements, self.add, self.mul)

        # Use composition to reuse validation logic
        self._additive_part = AbelianGroup(elements, add_op, op_name="+")
        self._multiplicative_part = Semigroup(elements, mul_op, op_name="*")
        self.validate()

    def validate(self) -> None:
        """Validates ring axioms: additive group, multiplicative semigroup, and distributivity."""
        # Validation for additive and multiplicative parts is handled during their instantiation.
        if not self._is_distributive():
            raise ValueError("Distributivity violated: Structure is not a Ring.")

    def _is_distributive(self) -> bool:
        """Checks if multiplication distributes over addition: a*(b+c) = a*b + a*c and (a+b)*c = a*c + b*c."""
        for a in self._elements:
            for b in self._elements:
                for c in self._elements:
                    # Left distributivity: a * (b + c) = (a * b) + (a * c)
                    if self.mul(a, self.add(b, c)) != self.add(self.mul(a, b), self.mul(a, c)):
                        return False
                    # Right distributivity: (a + b) * c = (a * c) + (b * c)
                    if self.mul(self.add(a, b), c) != self.add(self.mul(a, c), self.mul(b, c)):
                        return False
        return True
