from src.algebras.magma import Magma
from src.algebras.analyzer import StructureAnalyzer


class Semigroup(Magma):
    """An associative Magma."""

    def validate(self) -> None:
        """Validates associativity."""
        super().validate()
        if not StructureAnalyzer.is_associative(self.op):
            raise ValueError("Associativity violated: Structure is not a Semigroup.")
