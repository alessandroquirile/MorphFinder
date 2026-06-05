from typing import Any

from src.domain.services.analysis.analyzer import RingAnalyzer
from src.domain.entities.algebras.ring import Ring


class FiniteRingAnalyzer(RingAnalyzer):
    """Implementation of ring analysis for finite rings."""

    def supports(self, structure: Any) -> bool:
        return isinstance(structure, Ring)

    def get_zero_divisors(self, ring: Ring) -> set[Any]:
        zero_divisors = set()
        zero = ring.zero
        for a in ring.carrier.elements:
            if a == zero:
                continue
            for b in ring.carrier.elements:
                if b == zero:
                    continue
                if ring.multiplication(a, b) == zero or ring.multiplication(b, a) == zero:
                    zero_divisors.add(a)
                    break
        return zero_divisors

    def get_unit(self, ring: Ring) -> set[Any]:
        return {a for a in ring.carrier.elements if self.is_invertible(ring, a)}

    def is_invertible(self, ring: Ring, a: Any) -> bool:
        unity = ring.unity
        if unity is None:
            return False
        for b in ring.carrier.elements:
            if ring.multiplication(a, b) == unity and ring.multiplication(b, a) == unity:
                return True
        return False
