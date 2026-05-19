from typing import Callable, Any

from src.algebras.abelian_group import AbelianGroup
from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.axiom import DistributivityAxiom
from src.algebras.binary_operation import FiniteBinaryOperation
from src.algebras.carrier_set import FiniteCarrierSet
from src.algebras.semigroup import Semigroup
from src.utils.validator import FiniteAxiomValidator
from src.utils.analysis.finite_magma_analyzer import FiniteMagmaAnalyzer


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
        # We define a temporary magma to use the analysis for identity
        self._mult_magma = Semigroup(elements, mul_op)

        super().__init__(
            carrier=self.carrier,
            operations=[self._addition, self._multiplication]
        )
        self.axioms = super().axioms + [DistributivityAxiom()]

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
        analyzer = FiniteMagmaAnalyzer()
        return analyzer.find_identity(self._mult_magma)

    @property
    def constants(self) -> set[Any]:
        constants = {self.zero}
        if self.unity is not None:
            constants.add(self.unity)
        return constants
