from typing import Set, Any, Dict, Tuple, List


class Genealogy:
    """
    Tracks how each element of an algebraic structure is generated from a 
    minimal set of generators and constants.
    """

    def __init__(self, structure, generators: Set[Any]):
        self.structure = structure
        self.generators = set(generators)
        self.constants_dict = structure.constants
        self.constants_values = set(self.constants_dict.values())
        self.base_elements = self.generators | self.constants_values
        # derivation: element -> (op_idx, arg1, arg2)
        self.recipes: Dict[Any, Tuple[int, Any, Any]] = {}
        # order in which elements were discovered to ensure dependencies are met
        self.generation_order: List[Any] = []
        self._build()

    def _build(self):
        """Builds the recipes for all elements in the structure."""
        closure = set(self.base_elements)
        new_elements = set(self.base_elements)
        
        while new_elements:
            next_generation = set()
            for op_idx, op in enumerate(self.structure.operations):
                current_closure = list(closure)
                # Try all pairs from current closure
                for x in current_closure:
                    for y in current_closure:
                        res = op(x, y)
                        if res not in closure:
                            closure.add(res)
                            next_generation.add(res)
                            self.recipes[res] = (op_idx, x, y)
                            self.generation_order.append(res)
            
            if not next_generation:
                break
            new_elements = next_generation

    def propagate(self, mapping: Dict[Any, Any], target_structure) -> Dict[Any, Any]:
        """
        Given a mapping for base elements, computes images for the rest 
        of the structure.
        """
        full_mapping = mapping.copy()
        for element in self.generation_order:
            op_idx, arg1, arg2 = self.recipes[element]
            target_op = target_structure.operations[op_idx]
            full_mapping[element] = target_op(full_mapping[arg1], full_mapping[arg2])
        return full_mapping
