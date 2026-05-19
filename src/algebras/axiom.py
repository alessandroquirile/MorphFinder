from abc import ABC, abstractmethod


class Axiom(ABC):
    """
    Abstract Base Class for an algebraic axiom.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        """
        Accepts a validator and dispatches the validation to the appropriate visit method.
        """
        pass


class AssociativityAxiom(Axiom):
    name = "Associativity"
    description = "∀ a, b, c ∈ S, (a * b) * c = a * (b * c)"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_associativity(self, structure)


class CommutativityAxiom(Axiom):
    name = "Commutativity"
    description = "∀ a, b ∈ S, a * b = b * a"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_commutativity(self, structure)


class IdentityExistenceAxiom(Axiom):
    name = "Identity Existence"
    description = "∃ e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_identity_existence(self, structure)


class InverseExistenceAxiom(Axiom):
    name = "Inverse Existence"
    description = "∀ a ∈ S, ∃ b ∈ S s.t. a * b = b * a = e"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_inverse_existence(self, structure)


class MultiplicativeInversesAxiom(Axiom):
    name = "Multiplicative Inverses"
    description = "∀ a ∈ S - {0}, ∃ b ∈ S s.t. a * b = b * a = 1"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_multiplicative_inverses(self, structure)


class DistributivityAxiom(Axiom):
    name = "Distributivity"
    description = "∀ a,b,c ∈ S, a * (b + c) = (a * b) + (a * c) and (a + b) * c = (a * c) + (b * c)"

    def accept(self, validator: "Validator", structure: "AlgebraicStructure") -> bool:
        return validator.visit_distributivity(self, structure)
