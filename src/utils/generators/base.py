from abc import ABC, abstractmethod
from typing import Set, Any

from src.algebras.algebraic_structure import AlgebraicStructure


class GeneratingSetStrategy(ABC):
    """
    Abstract Base Class for generating set discovery strategies.
    """

    @abstractmethod
    def find(self, structure: AlgebraicStructure) -> Set[Any]:
        """
        Finds a generating set for the given algebraic structure.
        """
        pass
