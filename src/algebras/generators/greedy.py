from typing import Set, Any

from src.algebras.generators.base import GeneratingSetStrategy
from src.algebras.generators.helpers import _get_closure


def _find_best_candidate(elements, operations, constants, generators, current_closure):
    best_candidate = None
    max_growth = -1
    candidates = elements - current_closure

    for x in candidates:
        test_set = set(generators) | {x}
        potential_closure = _get_closure(test_set, constants, operations)
        growth = len(potential_closure) - len(current_closure)

        if growth > max_growth:
            max_growth = growth
            best_candidate = x

    return best_candidate


def _prune_generators(structure, generators):
    elements = set(structure.elements)
    operations = structure.operations
    constants = set(structure.constants.values())

    minimal_generators = set(generators)
    for g in generators:
        test_set = minimal_generators - {g}
        test_closure = _get_closure(test_set, constants, operations)
        if len(test_closure) == len(elements):
            minimal_generators.remove(g)

    return minimal_generators


def _greedy_expansion(structure):
    elements = set(structure.elements)
    operations = structure.operations
    constants = set(structure.constants.values())

    generators = []
    current_closure = _get_closure(set(), constants, operations)

    while len(current_closure) < len(elements):
        best_candidate = _find_best_candidate(
            elements, operations, constants, generators, current_closure
        )

        if best_candidate is not None:
            generators.append(best_candidate)
            current_closure = _get_closure(set(generators), constants, operations)
        else:
            break

    return generators


class GreedyPruningStrategy(GeneratingSetStrategy):
    """
    Finds a minimal generating set G using a greedy expansion followed by pruning.

    Theoretical Approach:
    1. Expansion: Iteratively adds elements that maximize the growth of the closure <G>.
    2. Pruning: Removes redundant elements from the resulting set.

    Note: While it ensures that <G> = S and no proper subset of G generates S, 
    it does not guarantee a global minimum cardinality.
    """


    def find(self, structure) -> Set[Any]:
        generators = _greedy_expansion(structure)
        return _prune_generators(structure, generators)
