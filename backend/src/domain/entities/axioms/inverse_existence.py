from src.domain.entities.axioms.base import Axiom


class InverseExistenceAxiom(Axiom):
    name = "Inverse Existence"
    description = "∀ a ∈ S, ∃ b ∈ S s.t. a * b = b * a = e"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_inverse_existence(self, structure)
