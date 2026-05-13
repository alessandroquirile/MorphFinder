from abc import ABC, abstractmethod
from typing import Set, Any

class GeneratingSetStrategy(ABC):
    """
    Abstract Base Class for generating set discovery strategies.
    """

    @abstractmethod
    def find(self, structure) -> Set[Any]:
        """
        Finds a generating set for the given algebraic structure.
        """
        pass
