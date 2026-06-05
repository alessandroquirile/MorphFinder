from src.domain.entities.axioms.base import Axiom


class AssociativityAxiom(Axiom):
    name = "Associativity"
    description = "∀ a, b, c ∈ S, (a * b) * c = a * (b * c)"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_associativity(self, structure)
