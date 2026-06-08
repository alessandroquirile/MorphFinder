import time

from src.domain.entities.algebras.base import AlgebraicStructure
from src.domain.entities.binary_operation import FiniteBinaryOperation
from src.domain.entities.carrier_set import FiniteCarrierSet
from src.adapters.dtos.schemas import MorphismRequest, MorphismResponse, HomomorphismSchema, StructureSchema
from src.application.use_cases.find_homomorphisms import FindHomomorphisms
from src.adapters.gateways.config_reader import ConfigFileReader


class MorphismController:
    """
    Interface Adapter: Controller for handling morphism-related requests.
    Converts API DTOs to Domain models and orchestrates Use Cases.
    """

    @staticmethod
    def find_morphisms(request: MorphismRequest) -> MorphismResponse:
        """Handles the discovery of homomorphisms between two structures."""
        source_structure = MorphismController._build_structure(request.source)
        target_structure = MorphismController._build_structure(request.target)

        # Retrieve strategy from config (Gateway)
        strategy = ConfigFileReader.get_strategy_name()

        start_time = time.perf_counter()
        use_case = FindHomomorphisms(strategy_name=strategy)
        homs = use_case.execute(source_structure, target_structure)
        end_time = time.perf_counter()

        results = []
        for h in homs:
            results.append(HomomorphismSchema(
                mapping={str(k): v for k, v in h.mapping.items()},
                properties=list(h.properties),
                image=list(h.image),
                kernel=list(h.kernel)
            ))

        return MorphismResponse(
            homomorphisms=results,
            strategy=strategy,
            time_elapsed=end_time - start_time
        )

    @staticmethod
    def _build_structure(model: StructureSchema) -> AlgebraicStructure:
        """Helper to convert API model to internal AlgebraicStructure."""
        # Ensure elements are strings to maintain consistency
        str_elements = [str(e) for e in model.elements]
        carrier = FiniteCarrierSet(set(str_elements))

        if model.formula:
            # Evaluate formula for each pair of elements to build the internal operation
            allowed_names = {"__builtins__": {}, "abs": abs, "min": min, "max": max}
            n = len(str_elements)

            # Create a mapping from element value to index
            element_to_index = {val: i for i, val in enumerate(str_elements)}

            def op_func(a, b):
                # Map elements to their indices if possible for formula evaluation
                idx_a = element_to_index.get(str(a), a)
                idx_b = element_to_index.get(str(b), b)

                # Evaluate expression like "(a + b) % n"
                try:
                    result = eval(model.formula, allowed_names, {"a": idx_a, "b": idx_b, "n": n})
                    # Attempt to map the numeric result back to an element if applicable
                    return str(str_elements[result % n]) if isinstance(result, int) else str(result)
                except Exception:
                    return None
        else:
            def op_func(a, b):
                key = f"{a},{b}"
                return str(model.table.get(key))

        operation = FiniteBinaryOperation(carrier, op_func)

        # Simple wrapper for dynamic structure
        class DynamicStructure(AlgebraicStructure):
            def __init__(self, carrier, ops, constants):
                super().__init__(carrier, ops)
                self._constants = constants

            @property
            def constants(self):
                return self._constants

        return DynamicStructure(carrier, [operation], model.constants)
