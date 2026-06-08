from typing import List, Dict, Any

from src.application.generators.factory import StrategyFactory
from src.domain.entities.algebras.base import AlgebraicStructure
from src.domain.entities.algebras.unital_ring import UnitalRing
from src.domain.services.generating_set.genealogy import Genealogy
from src.domain.services.generating_set.pruning import Pruner
from src.domain.services.classification import Classifier
from src.domain.entities.homomorphism import Homomorphism


class FindHomomorphisms:
    """Application use case for finding homomorphisms using CSP backtracking and genealogy propagation."""

    def __init__(self, strategy_name: str = ""):
        self.factory = StrategyFactory()
        self.strategy = self.factory.get_strategy(strategy_name)

    def execute(self, source: AlgebraicStructure, target: AlgebraicStructure) -> List[Homomorphism]:
        """
        Executes the use case: Finds all homomorphisms f: source -> target.
        """

        # Homomorphisms must preserve all operations
        if len(source.operations) != len(target.operations):
            return []

        # Find generators of S using specified strategy
        generators = list(self.strategy.find(source))

        # Phase 1: Genealogy Function
        genealogy = Genealogy(source, set(generators))

        homomorphisms = []

        # Pre-map mandatory structural constants
        base_mapping = self._get_constants_mapping(source, target)

        # Identify constants not fixed by the mandatory mapping
        source_constants_values = set(source.constants.values())
        free_constants = [c for c in source_constants_values if c not in base_mapping]
        all_to_map = generators + free_constants

        # Phase 2: Backtracking and Constraint Propagation
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
                    # Use Classifier service (Application layer using Service) 
                    # to calculate properties before creating the Entity.
                    temp_hom = Homomorphism(full_mapping, source, target)
                    properties = Classifier.classify(temp_hom)
                    image = Classifier.get_image(full_mapping)
                    kernel = Classifier.get_kernel(full_mapping, target)

                    results.append(Homomorphism(
                        mapping=full_mapping,
                        source=source,
                        target=target,
                        properties=properties,
                        image=image,
                        kernel=kernel
                    ))
            except Exception:
                pass
            return

        gen = generators[generator_index]
        if gen in current_mapping:
            # Generator is already mapped
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
        """
        PHASE 3: Final Validation
        Verify that the constructed mapping satisfies the homomorphism property.
        """
        # 1. Check all elements are mapped
        if len(mapping) != len(source.elements):
            return False

        # 2. Check operation preservation: f(a * b) = f(a) □ f(b)
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
                if key == "unity":
                    if not (isinstance(source, UnitalRing) and isinstance(target, UnitalRing)):
                        continue
                if mapping.get(source_val) != target_constants[key]:
                    return False

        return True
