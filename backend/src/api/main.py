from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.api.schemas import MorphismRequest, MorphismResponse, HomomorphismSchema, StructureSchema
from src.algebras.structures.base import AlgebraicStructure
from src.algebras.structures.carrier_set import FiniteCarrierSet
from src.algebras.structures.binary_operation import FiniteBinaryOperation
from src.core.engine import MorphismFinder
from typing import Any, Dict
from src.utils.reader import ConfigFileReader
import uvicorn
import time

app = FastAPI(title="MorphFinder API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def build_structure(model: StructureSchema) -> AlgebraicStructure:
    """Helper to convert API model to internal AlgebraicStructure."""
    # Ensure elements are strings to maintain consistency
    str_elements = [str(e) for e in model.elements]
    carrier = FiniteCarrierSet(set(str_elements))
    
    if model.formula:
        # Evaluate formula for each pair of elements to build the internal operation
        # We use a restricted scope for security
        allowed_names = {"__builtins__": {}, "abs": abs, "min": min, "max": max}
        n = len(str_elements)
        
        # Create a mapping from element value to index
        element_to_index = {val: i for i, val in enumerate(str_elements)}
        
        def op_func(a, b):
            # Map elements to their indices if possible for formula evaluation
            idx_a = element_to_index.get(str(a), a)
            idx_b = element_to_index.get(str(b), b)
            
            # Evaluate expression like "(a + b) % n"
            # Using indices as 'a' and 'b' in the formula context
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

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
# ... (rest of imports)

# ... (within find_morphisms function)
@app.post("/v1/morphisms/find", response_model=MorphismResponse)
async def find_morphisms(request: MorphismRequest):
    try:
        source_structure = build_structure(request.source)
        target_structure = build_structure(request.target)

        start_time = time.perf_counter()
        finder = MorphismFinder()
        homs = finder.find_homomorphisms(source_structure, target_structure)
        end_time = time.perf_counter()

        strategy = ConfigFileReader.get_strategy_name()

        results = []
        for h in homs:
            results.append(HomomorphismSchema(
                mapping={str(k): v for k, v in h.mapping.items()},
                properties=list(h.properties),
                image=list(h.image),
                kernel=list(h.kernel)
            ))

        return MorphismResponse(homomorphisms=results, strategy=strategy, time_elapsed=end_time - start_time)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
