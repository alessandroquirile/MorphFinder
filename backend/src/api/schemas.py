from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class StructureSchema(BaseModel):
    name: str
    elements: List[Any]
    # Representing the operation as a Cayley table: {(a, b): result} -> mapping a,b to result
    # In JSON, keys must be strings, so we'll use "a,b" as keys.
    table: Optional[Dict[str, Any]] = None
    formula: Optional[str] = None
    constants: Dict[str, Any]

class HomomorphismSchema(BaseModel):
    mapping: Dict[str, Any]
    properties: List[str]
    image: List[Any]
    kernel: List[Any]

class MorphismRequest(BaseModel):
    source: StructureSchema
    target: StructureSchema

class MorphismResponse(BaseModel):
    homomorphisms: List[HomomorphismSchema]
    strategy: str
    time_elapsed: float
