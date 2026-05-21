from abc import ABC
from collections.abc import Iterable
from typing import Any

from src.algebras.axioms.base import Axiom
from src.algebras.structures.binary_operation import BinaryOperation
from src.algebras.structures.carrier_set import CarrierSet
from src.algebras.validation.base import Validator


class AlgebraicStructure(ABC):
    """
    Abstract Base Class for all algebraic structures (S, op1, op2, ..., opn).
    Focuses on readability and proximity to mathematical representation.
    """

    def __init__(self, carrier: CarrierSet, operations: Iterable[BinaryOperation]):
        self.carrier = carrier
        self.operations = tuple(operations)
        self._axioms: list[Axiom] = []

    @property
    def elements(self) -> set[Any]:
        """Returns the elements of the algebraic structure."""
        return self.carrier.elements

    @property
    def constants(self) -> dict[str, Any]:
        """Returns a dictionary of distinguished elements (identity, zero, etc.)."""
        return {}

    @property
    def axioms(self) -> list[Axiom]:
        """Returns the list of axioms of the algebraic structure."""
        return self._axioms

    @axioms.setter
    def axioms(self, value: list[Axiom]):
        self._axioms = value

    def validate(self, validator: Validator) -> None:
        """Validates the axioms of the specific algebraic structure."""
        for axiom in self.axioms:
            if not validator.validate(self, axiom):
                raise ValueError(f"Axiom {axiom.name} is not satisfied.")
