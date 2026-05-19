from src.algebras.axioms.base import Axiom


class CommutativityAxiom(Axiom):
    name = "Commutativity"
    description = "∀ a, b ∈ S, a * b = b * a"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_commutativity(self, structure)
