from abc import ABC, abstractmethod
from typing import Any


class Analyzer(ABC):
    """Base class for all algebraic structure analyzers."""

    @abstractmethod
    def supports(self, structure: 'AlgebraicStructure') -> bool:
        """Checks if the analyzer supports the given algebraic structure."""
        pass


class RingAnalyzer(Analyzer):
    """Interface for ring-specific analysis."""

    @abstractmethod
    def get_zero_divisors(self, structure: 'Ring') -> set[Any]:
        pass

    @abstractmethod
    def get_unit(self, structure: 'Ring') -> set[Any]:
        pass

    @abstractmethod
    def is_invertible(self, structure: 'Ring', element: Any) -> bool:
        pass
