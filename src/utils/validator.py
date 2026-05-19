from abc import ABC, abstractmethod
from typing import Any

from src.algebras.axiom import (
    Axiom, AssociativityAxiom, CommutativityAxiom,
    IdentityExistenceAxiom, InverseExistenceAxiom, DistributivityAxiom,
    MultiplicativeInversesAxiom
)
from src.algebras.binary_operation import CayleyTable


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


class FiniteAxiomValidator(Validator):
    """
    Validator implementation for finite algebraic structures using CayleyTable and Visitor Pattern.
    """

    def __init__(self, table: CayleyTable):
        self.table = table

    def validate(self, structure: Any, axiom: Axiom) -> bool:
        return axiom.accept(self, structure)

    def visit_associativity(self, axiom: AssociativityAxiom, structure: Any) -> bool:
        elements = structure.carrier.elements
        for a in elements:
            for b in elements:
                for c in elements:
                    # (a * b) * c
                    ab = self.table[(a, b)]
                    left = self.table[(ab, c)]
                    # a * (b * c)
                    bc = self.table[(b, c)]
                    right = self.table[(a, bc)]
                    if left != right:
                        return False
        return True

    def visit_commutativity(self, axiom: CommutativityAxiom, structure: Any) -> bool:
        elements = structure.carrier.elements
        for a in elements:
            for b in elements:
                if self.table[(a, b)] != self.table[(b, a)]:
                    return False
        return True

    def visit_identity_existence(self, axiom: IdentityExistenceAxiom, structure: Any) -> bool:
        elements = structure.carrier.elements
        for e in elements:
            if all(self.table[(e, a)] == a and self.table[(a, e)] == a for a in elements):
                return True
        return False

    def visit_inverse_existence(self, axiom: InverseExistenceAxiom, structure: Any) -> bool:
        elements = structure.carrier.elements
        # Find identity first
        identity = None
        for e in elements:
            if all(self.table[(e, a)] == a and self.table[(a, e)] == a for a in elements):
                identity = e
                break

        if identity is None:
            return False

        for a in elements:
            found_inverse = False
            for b in elements:
                if self.table[(a, b)] == identity and self.table[(b, a)] == identity:
                    found_inverse = True
                    break
            if not found_inverse:
                return False
        return True

    def visit_distributivity(self, axiom: DistributivityAxiom, structure: Any) -> bool:
        if len(structure.operations) < 2:
            return False

        elements = structure.carrier.elements
        add_op = structure.operations[0]
        mul_op = structure.operations[1]

        for a in elements:
            for b in elements:
                for c in elements:
                    if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)):
                        return False
                    if mul_op(add_op(a, b), c) != add_op(mul_op(a, c), mul_op(b, c)):
                        return False
        return True

    def visit_multiplicative_inverses(self, axiom: MultiplicativeInversesAxiom, structure: Any) -> bool:
        elements = structure.carrier.elements
        zero = getattr(structure, 'zero', None)
        unity = getattr(structure, 'unity', None)

        if unity is None:
            return False

        mul_op = structure.operations[1]

        for a in elements:
            if a == zero:
                continue
            found_inverse = False
            for b in elements:
                if mul_op(a, b) == unity and mul_op(b, a) == unity:
                    found_inverse = True
                    break
            if not found_inverse:
                return False
        return True
