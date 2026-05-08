from src.algebras.magma import Magma


class Semigroup(Magma):
    """An associative Magma."""

    def validate(self) -> None:
        """Validates associativity."""
        super().validate()
        if not self.is_associative():
            raise ValueError("Associativity violated: Structure is not a Semigroup.")

    def is_associative(self) -> bool:
        """Checks ∀ a, b, c ∈ S, (a * b) * c = a * (b * c)."""
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.op(self.op(a, b), c) != self.op(a, self.op(b, c)):
                        return False
        return True
