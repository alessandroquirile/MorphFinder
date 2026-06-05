from abc import ABC, abstractmethod
from typing import Any

class Analyzer(ABC):
    """Abstract base class for algebraic structure analyzers."""
    
    @abstractmethod
    def supports(self, structure: Any) -> bool:
        """Returns True if the analyzer supports the given structure."""
        pass

class RingAnalyzer(Analyzer):
    """Base class for ring analyzers."""
    pass
