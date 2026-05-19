from abc import ABC, abstractmethod
from typing import Any


class CarrierSet(ABC):
    """
    Abstract Base Class for the carrier set of an algebraic structure.
    """

    @property
    @abstractmethod
    def elements(self) -> set[Any]:
        """Returns the set of elements in the carrier set."""
        pass

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __contains__(self, item):
        return item in self.elements


class FiniteCarrierSet(CarrierSet):
    """
    Represents a finite carrier set, optionally linked to a CayleyTable.
    """

    def __init__(self, elements: set[Any], cayley_table: Any = None):
        self._elements = frozenset(elements)
        self.cayley_table = cayley_table

    @property
    def elements(self) -> set[Any]:
        return set(self._elements)
