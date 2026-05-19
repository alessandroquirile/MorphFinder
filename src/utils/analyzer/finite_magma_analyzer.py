from typing import Any, Optional

from src.algebras.magma import Magma
from src.utils.analyzer.base import Analyzer


class FiniteMagmaAnalyzer(Analyzer):
    """Implementation of magma analysis for finite magmas."""

    def supports(self, structure: Any) -> bool:
        return isinstance(structure, Magma)

    def find_identity(self, structure: Magma) -> Optional[Any]:
        """Finds the identity element e ∈ S s.t. ∀ a ∈ S, e * a = a * e = a."""
        elements = structure.carrier.elements
        for e in elements:
            if all(structure.operation(e, a) == a and structure.operation(a, e) == a for a in elements):
                return e
        return None
