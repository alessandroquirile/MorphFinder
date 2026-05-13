from itertools import combinations
from typing import Set, Any
from src.utils.generators.base import GeneratingSetStrategy
from src.utils.generators.helpers import _get_closure

class BruteForceStrategy(GeneratingSetStrategy):
    """
    Finds the absolute minimum generating set by checking all subsets 
    of increasing size. Guaranteed to find the smallest set.
    """

    def find(self, structure) -> Set[Any]:
        elements = list(structure.elements)
        operations = structure.operations
        constants = structure.constants
        target_size = len(elements)

        # Iterate through possible generating set sizes starting from 1
        for size in range(1, target_size + 1):
            for combo in combinations(elements, size):
                if len(_get_closure(set(combo), constants, operations)) == target_size:
                    return set(combo)
        
        return set(elements)
