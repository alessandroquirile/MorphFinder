from src.domain.entities.axioms.base import Axiom


class MultiplicativeInversesAxiom(Axiom):
    name = "Multiplicative Inverses"
    description = "∀ a ∈ S - {0}, ∃ b ∈ S s.t. a * b = b * a = 1"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_multiplicative_inverses(self, structure)
