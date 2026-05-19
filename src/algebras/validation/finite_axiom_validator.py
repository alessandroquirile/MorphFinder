from typing import Any

from src.algebras.axioms.base import Axiom
from src.algebras.axioms.associativity import AssociativityAxiom
from src.algebras.axioms.commutativity import CommutativityAxiom
from src.algebras.axioms.identity_existence import IdentityExistenceAxiom
from src.algebras.axioms.inverse_existence import InverseExistenceAxiom
from src.algebras.axioms.distributivity import DistributivityAxiom
from src.algebras.axioms.multiplicative_inverses import MultiplicativeInversesAxiom
from src.algebras.structures.binary_operation import CayleyTable
from src.algebras.validation.base import Validator


class FiniteAxiomValidator(Validator):
    """
    Validator implementation for finite algebraic structures using CayleyTable and Visitor Pattern.
    """

    def __init__(self, table: CayleyTable):
        self.table = table

    def validate(self, structure: Any, axiom: Axiom) -> bool:
        return axiom.accept(self, structure)

    def visit_associativity(self, axiom: AssociativityAxiom, structure: Any) -> bool:
        return self.table.is_associative(structure.carrier.elements)

    def visit_commutativity(self, axiom: CommutativityAxiom, structure: Any) -> bool:
        return self.table.is_commutative(structure.carrier.elements)

    def visit_identity_existence(self, axiom: IdentityExistenceAxiom, structure: Any) -> bool:
        return self.table.find_identity(structure.carrier.elements) is not None

    def visit_inverse_existence(self, axiom: InverseExistenceAxiom, structure: Any) -> bool:
        elements = structure.carrier.elements

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
