from typing import Callable, Set, Any

from src.algebras.abelian_group import AbelianGroup
from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.semigroup import Semigroup
from src.algebras.analyzer import StructureAnalyzer


class Ring(AlgebraicStructure):
    """
    A Ring (R, +, ⋅) is an algebraic structure where:
    1. (R, +) is an Abelian Group.
    2. (R, ⋅) is a Semigroup.
    3. Multiplication distributes over addition.

    Examples:
    (ℤ,+,⋅), (ℚ,+,⋅), (ℝ,+,⋅), ℘(S,△,∩) are rings.
    (ℕ,+,⋅) is not a ring.
    """

    def __init__(self, elements: Set, add_op: Callable, mul_op: Callable):
        self.additive_abelian_group = AbelianGroup(elements, add_op)
        self.multiplicative_semigroup = Semigroup(elements, mul_op)
        super().__init__(elements, self.additive_abelian_group.op, self.multiplicative_semigroup.op)
        self.validate()

    def validate(self) -> None:
        """Validates ring axioms: additive ab. group, multiplicative semigroup, and distributivity."""
        if not StructureAnalyzer.is_distributive(self):
            raise ValueError("Distributivity violated: Structure is not a Ring.")

    @property
    def zero(self) -> Any:
        """Returns the additive identity (zero) of the ring."""
        return self.additive_abelian_group.identity

    @property
    def unity(self) -> Any:
        """Returns the multiplicative identity (1) if it exists, else None."""
        return self.multiplicative_semigroup.identity

    @property
    def constants(self) -> Set[Any]:
        c = {self.zero}
        if self.unity is not None:
            c.add(self.unity)
        return c
