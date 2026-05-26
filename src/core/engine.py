from typing import List, Dict, Any, Set

from src.algebras.structures.base import AlgebraicStructure
from src.core.genealogy import Genealogy
from src.core.pruning import Pruner
from src.algebras.generators.factory import StrategyFactory
from src.algebras.structures.unital_ring import UnitalRing


class Homomorphism:
    """Represents a validated homomorphism between two algebraic structures."""
    def __init__(self, mapping: Dict[Any, Any], source, target):
        self.mapping = mapping
        self.source = source
        self.target = target

    def __repr__(self):
        return f"Homomorphism({self.mapping})"


class MorphismFinder:
    """Core engine for finding homomorphisms using CSP backtracking and genealogy propagation."""

    def __init__(self, strategy_name: str):
        self.factory = StrategyFactory()
        self.strategy = self.factory.get_strategy(strategy_name)

    def find_homomorphisms(self, source: AlgebraicStructure, target: AlgebraicStructure) -> List[Homomorphism]:
        """Finds all homomorphisms f: source -> target"""

        if len(source.operations) != len(target.operations):
            return []

        # Find generators using specified strategy (e.g., brute force, greedy...)
        generators = list(self.strategy.find(source))
        genealogy = Genealogy(source, set(generators))
        
        homomorphisms = []
        
        # Pre-map constants using the constants dictionary
        base_mapping = self._get_constants_mapping(source, target)
        
        # Identify "free" constants: those in source.constants values but NOT in base_mapping.
        # This handles cases where a structure has a constant that doesn't have a 
        # mandatory target in the other structure (e.g., unity in a non-unital ring).
        source_constants_values = set(source.constants.values())
        free_constants = [c for c in source_constants_values if c not in base_mapping]
        all_to_map = generators + free_constants
        
        self._backtrack(
            0, all_to_map, base_mapping, source, target, genealogy, homomorphisms
        )
        
        return homomorphisms

    def _get_constants_mapping(self, source, target) -> Dict[Any, Any]:
        """Maps constants that share the same key in both structures."""
        mapping = {}
        source_constants = source.constants
        target_constants = target.constants
        
        for key, source_val in source_constants.items():
            if key in target_constants:
                # Special case: 'unity' is only mandatory if both are Unital Rings
                # or if we are strictly looking for unital homomorphisms.
                # For general Rings, mapping unity to 0 (the zero homomorphism) is valid.
                if key == "unity":
                    if not (isinstance(source, UnitalRing) and isinstance(target, UnitalRing)):
                        continue
                
                mapping[source_val] = target_constants[key]
            
        return mapping

    def _backtrack(self, generator_index, generators, current_mapping, source, target, genealogy, results):
        """Backtracking algorithm."""
        if generator_index == len(generators):
            # All generators mapped, propagate to all elements
            try:
                full_mapping = genealogy.propagate(current_mapping, target)
                if self._is_valid_homomorphism(full_mapping, source, target):
                    results.append(Homomorphism(full_mapping, source, target))
            except Exception:
                pass
            return

        gen = generators[generator_index]
        if gen in current_mapping:
            # Generator is already mapped (likely it's a mandatory constant)
            self._backtrack(generator_index + 1, generators, current_mapping, source, target, genealogy, results)
            return

        for target_val in target.elements:
            # Pruning using Pruner class
            if not Pruner.is_assignment_possible(gen, target_val, source, target):
                continue

            new_mapping = current_mapping.copy()
            new_mapping[gen] = target_val
            self._backtrack(generator_index + 1, generators, new_mapping, source, target, genealogy, results)

    def _is_valid_homomorphism(self, mapping, source, target) -> bool:
        """Final verification of the homomorphism property."""
        # 1. Check all elements are mapped
        if len(mapping) != len(source.elements):
            return False

        # 2. Check operation preservation: f(a * b) = f(a) * f(b)
        for op_index, source_op in enumerate(source.operations):
            target_op = target.operations[op_index]
            for a in source.elements:
                for b in source.elements:
                    res_ab = source_op(a, b)
                    if mapping[res_ab] != target_op(mapping[a], mapping[b]):
                        return False
        
        # 3. Check constants preservation
        source_constants = source.constants
        target_constants = target.constants
        for key, source_val in source_constants.items():
            if key in target_constants:
                # Unity is only mandatory for Unital Rings
                if key == "unity":
                    if not (isinstance(source, UnitalRing) and isinstance(target, UnitalRing)):
                        continue
                if mapping.get(source_val) != target_constants[key]:
                    return False

        return True
