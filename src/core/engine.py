from typing import List, Dict, Any

from src.algebras.generators.factory import StrategyFactory
from src.algebras.structures.base import AlgebraicStructure
from src.algebras.structures.unital_ring import UnitalRing
from src.core.classification import Classifier
from src.core.genealogy import Genealogy
from src.core.pruning import Pruner


class Homomorphism:
    """Represents a validated homomorphism between two algebraic structures."""

    def __init__(self, mapping: Dict[Any, Any], source, target):
        self.mapping = mapping
        self.source = source
        self.target = target
        self.properties = Classifier.classify(self)
        self.image = Classifier.get_image(self.mapping)
        self.kernel = Classifier.get_kernel(self.mapping, self.target)

    def __repr__(self):
        props_str = f" | {', '.join(self.properties)}" if self.properties else ""
        return f"Homomorphism({self.mapping}{props_str})"

    def pretty(self) -> str:
        """Returns a detailed formatted algebraic representation of the homomorphism."""
        source_elements = "{" + ", ".join(map(str, sorted(list(self.source.elements)))) + "}"
        target_elements = "{" + ", ".join(map(str, sorted(list(self.target.elements)))) + "}"

        mapping_str = ", ".join([f"{src} ↦ {tgt}" for src, tgt in self.mapping.items()])
        props_str = f" | Properties: {', '.join(self.properties)}" if self.properties else ""

        image_str = f" | Im(f): {{{', '.join(map(str, sorted(list(self.image))))}}}"
        kernel_str = f" | Ker(f): {{{', '.join(map(str, sorted(list(self.kernel))))}}}"

        return f"f: {source_elements} → {target_elements} | {mapping_str}{props_str}{kernel_str}{image_str}"


class MorphismFinder:
    """Core engine for finding homomorphisms using CSP backtracking and genealogy propagation."""

    def __init__(self, strategy_name: str):
        self.factory = StrategyFactory()
        self.strategy = self.factory.get_strategy(strategy_name)

    def find_homomorphisms(self, source: AlgebraicStructure, target: AlgebraicStructure) -> List[Homomorphism]:
        """
        Finds all homomorphisms f: source -> target.
        
        Complexity Optimization:
        Instead of exploring the full map space O(|T|^|S|), we exploit the fact that
        a homomorphism is uniquely determined by its values on a generating set G.
        This reduces the search space to O(|T|^|G|), where |G| << |S|.
        """

        if len(source.operations) != len(target.operations):
            return []

        # Find generators using specified strategy (e.g., brute force, greedy...)
        # Note: G is typically NOT closed under the operations. This non-closure
        # allows us to model the problem as a Constraint Satisfaction Problem (CSP)
        # and propagate constraints through the structure's genealogy.
        generators = list(self.strategy.find(source))

        # Phase 1: Genealogy Function
        # Build the genealogy mapping homomorphism: S \ G -> S x S to track how elements
        # are generated, enabling deterministic constraint propagation.
        genealogy = Genealogy(source, set(generators))

        homomorphisms = []

        # Pre-map constants using the constants dictionary
        base_mapping = self._get_constants_mapping(source, target)

        # Identify "free" constants
        source_constants_values = set(source.constants.values())
        free_constants = [c for c in source_constants_values if c not in base_mapping]
        all_to_map = generators + free_constants

        # Phase 2: Backtracking and Constraint Propagation
        # Assign values to generators and propagate images using the genealogy 'recipe'.
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
        """
        PHASE 3: Final Validation
        Verify that the constructed mapping satisfies the homomorphism property:
        f(a * b) = f(a) □ f(b) and preserves intrinsic structural properties.
        """
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
        # According to the theory, valid homomorphisms must preserve distinguished
        # elements like zero and unity (intrinsic properties of the structures).
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
