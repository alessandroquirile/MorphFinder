from src.algebras.axioms.base import Axiom


class IdentityExistenceAxiom(Axiom):
    name = "Identity Existence"
    description = "∃ e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_identity_existence(self, structure)
