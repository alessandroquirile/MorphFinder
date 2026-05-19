from typing import Callable, Any, Optional

from src.algebras.algebraic_structure import AlgebraicStructure
from src.algebras.binary_operation import FiniteBinaryOperation
from src.algebras.carrier_set import FiniteCarrierSet
from src.algebras.validator import FiniteAxiomValidator


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

    @property
    def identity(self) -> Optional[Any]:
        """Returns the identity element e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a."""
        elements = self.carrier.elements
        for e in elements:
            if all(self.operation(e, a) == a and self.operation(a, e) == a for a in elements):
                return e
        return None
