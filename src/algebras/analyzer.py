from typing import Set, Any

from src.algebras.binary_operation import BinaryOperation


class StructureAnalyzer:
    """
    Service class for mathematical analysis of algebraic structures.
    """

    @staticmethod
    def is_associative(binary_op: BinaryOperation) -> bool:
        """Checks ∀ a, b, c ∈ S, (a * b) * c = a * (b * c)."""
        elements = binary_op.elements
        for a in elements:
            for b in elements:
                for c in elements:
                    if binary_op(binary_op(a, b), c) != binary_op(a, binary_op(b, c)):
                        return False
        return True

    @staticmethod
    def is_commutative(binary_op: BinaryOperation) -> bool:
        """Checks ∀ a, b ∈ S, a * b = b * a."""
        elements = binary_op.elements
        for a in elements:
            for b in elements:
                if binary_op(a, b) != binary_op(b, a):
                    return False
        return True

    @staticmethod
    def is_distributive(ring) -> bool:
        """Checks if multiplication distributes over addition: a*(b+c) = a*b + a*c and (a+b)*c = a*c + b*c."""
        elements = ring.elements
        add_op = ring.additive_abelian_group.op
        mul_op = ring.multiplicative_semigroup.op
        for a in elements:
            for b in elements:
                for c in elements:
                    # Left distributivity: a * (b + c) = (a * b) + (a * c)
                    if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)):
                        return False
                    # Right distributivity: (a + b) * c = (a * c) + (b * c)
                    if mul_op(add_op(a, b), c) != add_op(mul_op(a, c), mul_op(b, c)):
                        return False
        return True

    @staticmethod
    def find_zero_divisors(ring) -> Set[Any]:
        """
        Finds all zero divisors of the ring.
        An element a ∈ R, a ≠ 0, is a zero divisor if there exists
        b ∈ R, b ≠ 0, such that a ⋅ b = 0 or b ⋅ a = 0.
        """
        zero_divisors = set()
        zero = ring.zero
        mul_op = ring.multiplicative_semigroup.op
        for a in ring.elements:
            if a == zero:
                continue
            for b in ring.elements:
                if b == zero:
                    continue
                if mul_op(a, b) == zero or mul_op(b, a) == zero:
                    zero_divisors.add(a)
                    break
        return zero_divisors

    @staticmethod
    def is_invertible(ring, a: Any) -> bool:
        """Checks if an element has a multiplicative inverse (requires unity)."""
        unity = ring.unity
        mul_op = ring.multiplicative_semigroup.op
        if unity is None:
            return False
        for b in ring.elements:
            if mul_op(a, b) == unity and mul_op(b, a) == unity:
                return True
        return False

    @staticmethod
    def find_invertible_elements(ring) -> Set[Any]:
        """Returns the set of all units (invertible elements)."""
        return {a for a in ring.elements if StructureAnalyzer.is_invertible(ring, a)}
