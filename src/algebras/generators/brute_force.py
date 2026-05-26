from itertools import combinations
from typing import Set, Any

from src.algebras.generators.base import GeneratingSetStrategy
from src.algebras.generators.helpers import _get_closure


class BruteForceStrategy(GeneratingSetStrategy):
    """
    Finds the absolute minimum generating set G for a structure S.
    
    Theoretical Approach:
    Enumerates all subsets of S in order of increasing cardinality. 
    Returns the first subset G whose closure <G> equals S. 
    This guarantees finding a generating set of global minimum cardinality.
    """

    def find(self, structure) -> Set[Any]:
        elements = list(structure.elements)
        operations = structure.operations
        constants = set(structure.constants.values())
        target_size = len(elements)

        # First check if constants alone generate the structure
        if len(_get_closure(set(), constants, operations)) == target_size:
            return set()

        # Iterate through possible generating set sizes starting from 1
        for size in range(1, target_size + 1):
            for combo in combinations(elements, size):
                if len(_get_closure(set(combo), constants, operations)) == target_size:
                    return set(combo)

        return set(elements)
