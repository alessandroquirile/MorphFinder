from abc import ABC, abstractmethod
from typing import Any

from src.algebras.axioms.base import Axiom
from src.algebras.axioms.associativity import AssociativityAxiom
from src.algebras.axioms.commutativity import CommutativityAxiom
from src.algebras.axioms.identity_existence import IdentityExistenceAxiom
from src.algebras.axioms.inverse_existence import InverseExistenceAxiom
from src.algebras.axioms.distributivity import DistributivityAxiom
from src.algebras.axioms.multiplicative_inverses import MultiplicativeInversesAxiom


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
