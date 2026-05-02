from abc import ABC
from typing import Any, Dict, Iterable, Optional, Set, Tuple


class AlgebraicStructure(ABC):
    def __init__(self, elements: Iterable[Any]):
        """
        Initializes an algebraic structure (a set of elements together with one or more operations).

        :param elements: An iterable of elements in the structure.
        """
        self.elements: Set[Any] = set(elements)


class Magma(AlgebraicStructure):
    def __init__(self, elements: Iterable[Any], cayley_table: Dict[Tuple[Any, Any], Any]):
        """
        Initializes a finite Magma (an algebraic structure with a single operation defined on it).

        :param elements: An iterable of elements in the magma.
        :param cayley_table: A dictionary mapping (a, b) to the result of a * b.
        :raises ValueError: If the magma is not closed or the table is incomplete.
        """
        super().__init__(elements)
        self.cayley_table = cayley_table
        self._validate()

    def _validate(self) -> None:
        """Validates closure and completeness of the operation table."""
        for a in self.elements:
            for b in self.elements:
                if (a, b) not in self.cayley_table:
                    raise ValueError(f"Cayley table is incomplete: ({a}, {b}) missing.")
                result = self.cayley_table[(a, b)]
                if result not in self.elements:
                    raise ValueError(f"Magma is not closed: {a} * {b} = {result}, which is not in elements.")

    def op(self, a: Any, b: Any) -> Any:
        """Returns the result of the binary operation a * b."""
        return self.cayley_table[(a, b)]

    def is_associative(self) -> bool:
        """Checks if the operation is associative: ∀ a, b, c ∈ elements, (a * b) * c = a * (b * c)."""
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    left_grouping = self.op(self.op(a, b), c)
                    right_grouping = self.op(a, self.op(b, c))
                    if left_grouping != right_grouping:
                        return False
        return True

    def find_identity(self) -> Optional[Any]:
        """Finds the identity element ∃ e ∈ elements s.t. ∀ a ∈ elements, e * a = a * e = a."""
        for e in self.elements:
            is_identity = True
            for a in self.elements:
                if self.op(e, a) != a or self.op(a, e) != a:
                    is_identity = False
                    break
            if is_identity:
                return e
        return None

    def has_inverses(self, identity: Any) -> bool:
        """Checks if ∀ a ∈ elements, ∃ b ∈ elements s.t. a * b = b * a = identity."""
        for a in self.elements:
            found_inverse = False
            for b in self.elements:
                if self.op(a, b) == identity and self.op(b, a) == identity:
                    found_inverse = True
                    break
            if not found_inverse:
                return False
        return True

    def is_commutative(self) -> bool:
        """Checks if the operation is commutative: ∀ a, b ∈ elements, a * b = b * a."""
        for a in self.elements:
            for b in self.elements:
                if self.op(a, b) != self.op(b, a):
                    return False
        return True


class Semigroup(Magma):
    """A semigroup is an associative magma."""
    pass


class Monoid(Semigroup):
    """A monoid is a semigroup with an identity element."""
    def __init__(self, elements: Iterable[Any], cayley_table: Dict[Tuple[Any, Any], Any], identity: Any):
        super().__init__(elements, cayley_table)
        self.identity = identity


class Group(Monoid):
    """A group is a monoid where every element has an inverse."""
    def __init__(self, elements: Iterable[Any], cayley_table: Dict[Tuple[Any, Any], Any], identity: Any):
        super().__init__(elements, cayley_table, identity)
        self._inverse_map: Dict[Any, Any] = self._build_inverse_map()

    def _build_inverse_map(self) -> Dict[Any, Any]:
        inv_map = {}
        for a in self.elements:
            for b in self.elements:
                if self.op(a, b) == self.identity and self.op(b, a) == self.identity:
                    inv_map[a] = b
                    break
        return inv_map

    def inverse(self, a: Any) -> Any:
        """Returns the inverse of element a."""
        return self._inverse_map[a]


class AbelianGroup(Group):
    """An abelian group is a group that is also commutative."""
    pass


def classify(elements: Iterable[Any], cayley_table: Dict[Tuple[Any, Any], Any]) -> Magma:
    """
    Analyzes the algebraic structure and returns an instance of the most specific subclass.
    """
    m = Magma(elements, cayley_table)
    
    associative = m.is_associative()
    if not associative:
        return m
    
    identity = m.find_identity()
    if identity is None:
        return Semigroup(elements, cayley_table)
    
    has_inv = m.has_inverses(identity)
    commutative = m.is_commutative()
    
    if has_inv:
        if commutative:
            return AbelianGroup(elements, cayley_table, identity)
        return Group(elements, cayley_table, identity)
    
    return Monoid(elements, cayley_table, identity)
