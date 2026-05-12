from src.algebras.magma import Magma


class Semigroup(Magma):
    """An associative Magma."""

    def validate(self) -> None:
        """Validates associativity."""
        super().validate()
        if not self.op.is_associative:
            raise ValueError("Associativity violated: Structure is not a Semigroup.")
