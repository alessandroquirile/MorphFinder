from typing import Callable, Any

from src.algebras.abelian_group import AbelianGroup
from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.axiom import DistributivityAxiom
from src.algebras.binary_operation import FiniteBinaryOperation
from src.algebras.carrier_set import FiniteCarrierSet
from src.algebras.semigroup import Semigroup
from src.algebras.validator import FiniteAxiomValidator


class Ring(AlgebraicStructure):
    """
    A Ring (R, +, ⋅) is an algebraic structure where:
    1. (R, +) is an Abelian Group.
    2. (R, ⋅) is a Semigroup.
    3. Multiplication distributes over addition.
    """

    def __init__(self, elements: set[Any], add_op: Callable[[Any, Any], Any], mul_op: Callable[[Any, Any], Any]):
        self.carrier = FiniteCarrierSet(elements)
        self._addition = FiniteBinaryOperation(self.carrier, add_op)
        self._multiplication = FiniteBinaryOperation(self.carrier, mul_op)

        self.additive_abelian_group = AbelianGroup(elements, add_op)
        self.multiplicative_semigroup = Semigroup(elements, mul_op)

        super().__init__(
            carrier=self.carrier,
            operations=[self._addition, self._multiplication]
        )
        self.axioms = [DistributivityAxiom()]

        self.validator = FiniteAxiomValidator(self._multiplication.table)
        self.validate(self.validator)

    @property
    def addition(self) -> FiniteBinaryOperation:
        return self._addition

    @property
    def multiplication(self) -> FiniteBinaryOperation:
        return self._multiplication

    @property
    def zero(self) -> Any:
        return self.additive_abelian_group.identity

    @property
    def unity(self) -> Any:
        return self.multiplicative_semigroup.identity

    @property
    def constants(self) -> set[Any]:
        constants = {self.zero}
        if self.unity is not None:
            constants.add(self.unity)
        return constants

    def find_zero_divisors(self) -> set[Any]:
        zero_divisors = set()
        zero = self.zero
        for a in self.carrier.elements:
            if a == zero:
                continue
            for b in self.carrier.elements:
                if b == zero:
                    continue
                if self.multiplication(a, b) == zero or self.multiplication(b, a) == zero:
                    zero_divisors.add(a)
                    break
        return zero_divisors

    def is_invertible(self, a: Any) -> bool:
        unity = self.unity
        if unity is None:
            return False
        for b in self.carrier.elements:
            if self.multiplication(a, b) == unity and self.multiplication(b, a) == unity:
                return True
        return False

    def find_invertible_elements(self) -> set[Any]:
        return {a for a in self.carrier.elements if self.is_invertible(a)}
