from typing import Callable, Set, Any

from src.algebras.abelian_group import AbelianGroup
from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.semigroup import Semigroup


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
        if not self._is_distributive():
            raise ValueError("Distributivity violated: Structure is not a Ring.")

    @property
    def zero(self) -> Any:
        """Returns the additive identity (zero) of the ring."""
        return self.additive_abelian_group.identity

    @property
    def unity(self) -> Any:
        """Returns the multiplicative identity (1) if it exists, else None."""
        return self.multiplicative_semigroup.identity

    def find_zero_divisors(self) -> Set:
        """
        Finds all zero divisors of the ring.
        An element a ∈ R, a ≠ 0, is a zero divisor if there exists
        b ∈ R, b ≠ 0, such that a ⋅ b = 0 or b ⋅ a = 0.
        """
        zero_divisors = set()
        zero = self.zero
        mul_op = self.multiplicative_semigroup.op
        for a in self.elements:
            if a == zero:
                continue
            for b in self.elements:
                if b == zero:
                    continue
                if mul_op(a,b) == zero or mul_op(b,a) == zero:
                    zero_divisors.add(a)
                    break
        return zero_divisors

    def is_commutative(self) -> bool:
        """Checks if the multiplicative semigroup is commutative."""
        mul_op = self.multiplicative_semigroup.op
        for a in self.elements:
            for b in self.elements:
                if mul_op(a,b) != mul_op(b,a):
                    return False
        return True

    def is_invertible(self, a: Any) -> bool:
        """Checks if an element has a multiplicative inverse (requires unity)."""
        unity = self.unity
        mul_op = self.multiplicative_semigroup.op
        if unity is None:
            return False
        for b in self.elements:
            if mul_op(a,b) == unity and mul_op(b,a) == unity:
                return True
        return False

    def find_invertible_elements(self) -> Set:
        """Returns the set of all units (invertible elements)."""
        return {a for a in self.elements if self.is_invertible(a)}

    def _is_distributive(self) -> bool:
        """Checks if multiplication distributes over addition: a*(b+c) = a*b + a*c and (a+b)*c = a*c + b*c."""
        add_op = self.additive_abelian_group.op
        mul_op = self.multiplicative_semigroup.op
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    # Left distributivity: a * (b + c) = (a * b) + (a * c)
                    if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)):
                        return False
                    # Right distributivity: (a + b) * c = (a * c) + (b * c)
                    if mul_op(add_op(a, b), c) != add_op(mul_op(a, c), mul_op(b, c)):
                        return False
        return True
