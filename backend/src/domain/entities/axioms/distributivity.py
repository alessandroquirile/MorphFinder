from src.domain.entities.axioms.base import Axiom


class DistributivityAxiom(Axiom):
    name = "Distributivity"
    description = "∀ a,b,c ∈ S, a * (b + c) = (a * b) + (a * c) and (a + b) * c = (a * c) + (b * c)"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_distributivity(self, structure)
