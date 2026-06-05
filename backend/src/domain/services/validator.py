from abc import ABC, abstractmethod
from typing import Any

from src.domain.entities.axioms.associativity import AssociativityAxiom
from src.domain.entities.axioms.base import Axiom
from src.domain.entities.axioms.commutativity import CommutativityAxiom
from src.domain.entities.axioms.distributivity import DistributivityAxiom
from src.domain.entities.axioms.identity_existence import IdentityExistenceAxiom
from src.domain.entities.axioms.inverse_existence import InverseExistenceAxiom
from src.domain.entities.axioms.multiplicative_inverses import MultiplicativeInversesAxiom


class Validator(ABC):
    """
    Interface for validating axioms on algebraic structures using the Visitor Pattern.
    """

    @abstractmethod
    def validate(self, structure: Any, axiom: Axiom) -> bool:
        """
        Entry point for validation. Dispatches to the axiom's accept method.
        """
        pass

    @abstractmethod
    def visit_associativity(self, axiom: AssociativityAxiom, structure: Any) -> bool:
        pass

    @abstractmethod
    def visit_commutativity(self, axiom: CommutativityAxiom, structure: Any) -> bool:
        pass

    @abstractmethod
    def visit_identity_existence(self, axiom: IdentityExistenceAxiom, structure: Any) -> bool:
        pass

    @abstractmethod
    def visit_inverse_existence(self, axiom: InverseExistenceAxiom, structure: Any) -> bool:
        pass

    @abstractmethod
    def visit_distributivity(self, axiom: DistributivityAxiom, structure: Any) -> bool:
        pass

    @abstractmethod
    def visit_multiplicative_inverses(self, axiom: MultiplicativeInversesAxiom, structure: Any) -> bool:
        pass
