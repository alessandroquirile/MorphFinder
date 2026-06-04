from typing import Set, Any

from src.algebras.generators.base import GeneratingSetStrategy


def find_minimal_generating_set(structure, strategy: GeneratingSetStrategy) -> Set[Any]:
    """
    Finds a minimal generating set using the provided strategy (Dependency Injection).
    """
    return strategy.find(structure)
