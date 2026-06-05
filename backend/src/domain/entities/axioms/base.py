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
