from typing import Any, Optional

from src.domain.services.analysis.analyzer import Analyzer
from src.domain.entities.algebras.magma import Magma


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
