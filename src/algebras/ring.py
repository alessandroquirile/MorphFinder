from typing import Any, Callable, Set

from src.algebras.abelian_group import AbelianGroup
from src.algebras.base import AlgebraicStructure, BinaryOperation
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

    def __init__(self, elements: Set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any]):
        self.additive_abelian_group = AbelianGroup(elements, add_op)
        self.multiplicative_semigroup = Semigroup(elements, mul_op)
        super().__init__(elements, self.additive_abelian_group.op, self.multiplicative_semigroup.op)

        self.validate()

    @property
    def zero(self) -> Any:
        """Returns the additive identity (zero) of the ring."""
        return self.additive_abelian_group.identity

    def validate(self) -> None:
        """Validates ring axioms: additive ab. group, multiplicative semigroup, and distributivity."""
        if not self._is_distributive():
            raise ValueError("Distributivity violated: Structure is not a Ring.")

    def find_zero_divisors(self) -> Set[Any]:
        """
        Finds all zero divisors of the ring.
        An element a ∈ R, a ≠ 0, is a zero divisor if there exists
        b ∈ R, b ≠ 0, such that a ⋅ b = 0 or b ⋅ a = 0.
        """
        zero_divisors = set()
        zero = self.zero
        for a in self.elements:
            if a == zero:
                continue
            for b in self.elements:
                if b == zero:
                    continue
                if self.multiplicative_semigroup.op(a, b) == zero or self.multiplicative_semigroup.op(b, a) == zero:
                    zero_divisors.add(a)
                    break
        return zero_divisors

    def is_commutative(self) -> bool:
        """Checks if the multiplicative semigroup is commutative."""
        for a in self.elements:
            for b in self.elements:
                if self.multiplicative_semigroup.op(a, b) != self.multiplicative_semigroup.op(b, a):
                    return False
        return True

    def is_left_cancellable(self, a: Any) -> bool:
        """Checks if a is left-cancellable: a*b = a*c => b = c for all b, c."""
        for b in self.elements:
            for c in self.elements:
                if self.multiplicative_semigroup.op(a, b) == self.multiplicative_semigroup.op(a, c):
                    if b != c:
                        return False
        return True

    def find_left_cancellable_elements(self) -> Set[Any]:
        """Returns the set of all left-cancellable elements."""
        return {a for a in self.elements if self.is_left_cancellable(a)}

    def is_right_cancellable(self, a: Any) -> bool:
        """Checks if a is right-cancellable: b*a = c*a => b = c for all b, c."""
        for b in self.elements:
            for c in self.elements:
                if self.multiplicative_semigroup.op(b, a) == self.multiplicative_semigroup.op(c, a):
                    if b != c:
                        return False
        return True

    def find_right_cancellable_elements(self) -> Set[Any]:
        """Returns the set of all right-cancellable elements."""
        return {a for a in self.elements if self.is_right_cancellable(a)}

    def is_cancellable(self, a: Any) -> bool:
        """An element is cancellable if it is both left and right cancellable."""
        return self.is_left_cancellable(a) and self.is_right_cancellable(a)

    def find_cancellable_elements(self) -> Set[Any]:
        """Returns the set of all cancellable elements."""
        return {a for a in self.elements if self.is_cancellable(a)}

    @property
    def unity(self) -> Any:
        """Returns the multiplicative identity (1) if it exists, else None."""
        # Check if the multiplicative structure is already a Monoid
        from src.algebras.monoid import Monoid
        if isinstance(self.multiplicative_semigroup, Monoid):
            return self.multiplicative_semigroup.identity
        
        # Manual search if it's just a Semigroup
        for e in self.elements:
            is_identity = True
            for a in self.elements:
                if self.multiplicative_semigroup.op(e, a) != a or self.multiplicative_semigroup.op(a, e) != a:
                    is_identity = False
                    break
            if is_identity:
                return e
        return None

    def is_invertible(self, a: Any) -> bool:
        """Checks if an element has a multiplicative inverse (requires unity)."""
        u = self.unity
        if u is None:
            return False
        for b in self.elements:
            if self.multiplicative_semigroup.op(a, b) == u and self.multiplicative_semigroup.op(b, a) == u:
                return True
        return False

    def find_invertible_elements(self) -> Set[Any]:
        """Returns the set of all units (invertible elements)."""
        return {a for a in self.elements if self.is_invertible(a)}

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
