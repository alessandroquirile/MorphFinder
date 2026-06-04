from typing import Callable, Any

from src.algebras.structures.base import AlgebraicStructure
from src.algebras.structures.binary_operation import FiniteBinaryOperation
from src.algebras.structures.carrier_set import FiniteCarrierSet
from src.algebras.validation.finite_axiom_validator import FiniteAxiomValidator


class Magma(AlgebraicStructure):
    """
    A Magma (S, *) consists of a set S and a single binary operation *.
    """

    def __init__(self, elements: set[Any], operation: Callable[[Any, Any], Any]):
        self.carrier = FiniteCarrierSet(elements)
        self._op = FiniteBinaryOperation(self.carrier, operation)
        super().__init__(carrier=self.carrier, operations=[self._op])

        self.validator = FiniteAxiomValidator(self._op.table)
        self.axioms = super().axioms
        self.validate(self.validator)

    @property
    def operation(self) -> FiniteBinaryOperation:
        return self._op
