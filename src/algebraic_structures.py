import inspect
from abc import ABC
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class AlgebraicStructure(ABC):
    def __init__(self, elements: Set[Any], *operations: Callable):
        """
        Initializes an algebraic structure (S, op1, op2, ..., opn).

        :param elements: A Set of elements in the structure (the carrier set S).
        :param operations: One or more callable functions representing the operations.
        """
        self.elements: Set[Any] = set(elements)
        self.operations: List[Callable] = list(operations)
        self._cayley_tables: List[Optional[Dict[Tuple[Any, Any], Any]]] = [
            self._generate_cayley_table(op) for op in operations
        ]

    def _generate_cayley_table(self, op: Callable) -> Optional[Dict[Tuple[Any, Any], Any]]:
        """
        Converts a callable binary operation into an internal table by evaluating it for all combinations in S.
        Returns None for non-binary operations (e.g., unary).
        """
        signature = inspect.signature(op)
        arity = len(signature.parameters)
        if arity == 2:
            return {(a, b): op(a, b) for a in self.elements for b in self.elements}
        return None


class Magma(AlgebraicStructure):
    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any]):
        """
        Initializes a finite Magma (S, op).
        A magma is an algebraic structure consisting of a set S and a single binary operation op: S x S -> S.

        :param elements: A Set of elements in the carrier set S.
        :param operation: A callable binary function representing op.
        :raises TypeError: If the operation is not binary or if more than one operation are detected.
        :raises ValueError: If the magma is not closed.
        """
        super().__init__(elements, operation)

        if len(self.operations) != 1:
            raise TypeError(f"Magma must have exactly one operation, but got {len(self.operations)}.")

        if self.cayley_table is None:
            signature = inspect.signature(operation)
            arity = len(signature.parameters)
            raise TypeError(f"Magma requires a binary operation (arity 2), but got arity {arity}.")

        self._validate()

    @property
    def cayley_table(self) -> Dict[Tuple[Any, Any], Any]:
        """Returns the primary internal Cayley table for this Magma."""
        return self._cayley_tables[0]

    def _validate(self) -> None:
        """Validates closure of the operation: ∀ a, b ∈ S, a * b ∈ S."""
        for a in self.elements:
            for b in self.elements:
                result = self.cayley_table[(a, b)]
                if result not in self.elements:
                    raise ValueError(f"Magma is not closed: {a} * {b} = {result}, which is not in S.")

    def op(self, a: Any, b: Any) -> Any:
        """Applies the binary operation a * b."""
        return self.operations[0](a, b)

    def is_associative(self) -> bool:
        """Checks if the operation is associative: ∀ a, b, c ∈ S, (a * b) * c = a * (b * c)."""
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    left_grouping = self.op(self.op(a, b), c)
                    right_grouping = self.op(a, self.op(b, c))
                    if left_grouping != right_grouping:
                        return False
        return True

    def find_identity(self) -> Optional[Any]:
        """Finds the identity element ∃ e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a."""
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
        """Checks if ∀ a ∈ S, ∃ b ∈ S s.t. a * b = b * a = e."""
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
        """Checks if the operation is commutative: ∀ a, b ∈ S, a * b = b * a."""
        for a in self.elements:
            for b in self.elements:
                if self.op(a, b) != self.op(b, a):
                    return False
        return True


class Semigroup(Magma):
    """A semigroup is an associative magma."""
    pass


class Monoid(Semigroup):
    """A monoid is a semigroup with an identity element e ∈ S."""

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], identity: Any):
        super().__init__(elements, operation)
        self.identity = identity


class Group(Monoid):
    """A group is a monoid where every element has an inverse."""

    def __init__(self, elements: Set[Any], operation: Callable[[Any, Any], Any], identity: Any):
        super().__init__(elements, operation, identity)
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


def classify(elements: Set[Any], operation: Callable[[Any, Any], Any]) -> Magma:
    """
    Analyzes the algebraic structure (S, op1, op2, ..., opn) and returns an instance of the most specific subclass.
    """
    magma = Magma(elements, operation)

    # Semigroup: associative magma
    if not magma.is_associative():
        return magma

    # Monoid: semigroup with one identity
    identity = magma.find_identity()
    if identity is None:
        return Semigroup(elements, operation)

    # Group: Monoid where every element has an inverse
    if not magma.has_inverses(identity):
        return Monoid(elements, operation, identity)

    # Abelian Group: commutative group
    if not magma.is_commutative():
        return Group(elements, operation, identity)

    return AbelianGroup(elements, operation, identity)
