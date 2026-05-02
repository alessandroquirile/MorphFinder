# MorphFinder

MorphFinder is a Python library designed for the study of finite algebraic structures. It provides a robust framework for verifying algebraic properties (associativity, commutativity, etc.) and automatically classifying structures into a formal mathematical hierarchy.

The project is built to support future work in finding and classifying morphisms (homomorphisms, isomorphisms, etc.) between finite algebraic structures.

## Features

- **Formal Hierarchy**: Implements a strict inheritance-based model:
  - `Magma` → `Semigroup` → `Monoid` → `Group` → `AbelianGroup`.
- **Automatic Classification**: A `classify()` factory function that analyzes a Cayley table and returns the most specific applicable subclass.
- **Property Verification**: Built-in logic for checking:
  - Closure and Completeness
  - Associativity (∀ a, b, c: (a*b)*c = a*(b*c))
  - Identity element (∃ e: e*a = a*e = a)
  - Inverses (∀ a, ∃ b: a*b = b*a = e)
  - Commutativity (∀ a, b: a*b = b*a)
- **Pre-computed Properties**: `Group` objects automatically pre-calculate inverse maps for efficient lookup.

## Usage

```python
from src.algebraic_structures import classify

# Define Z2 (integers modulo 2) under addition
elements = {0, 1}
cayley_table = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 0): 1,
    (1, 1): 0,
}

# Classify the structure
structure = classify(elements, cayley_table)

print(f"Type: {type(structure).__name__}")
# Output: Type: AbelianGroup

if hasattr(structure, 'identity'):
    print(f"Identity: {structure.identity}")
    # Output: Identity: 0

if hasattr(structure, 'inverse'):
    print(f"Inverse of 1: {structure.inverse(1)}")
    # Output: Inverse of 1: 1
```

## Installation

### Prerequisites
- Python 3.12+

### Running Tests
MorphFinder uses `pytest` for its test suite.
```bash
pip install pytest
pytest
```

## Project Structure

- `src/algebraic_structures.py`: Core logic and structure definitions.
- `tests/test_algebraic_structures.py`: Unit tests for various algebraic structures.
- `GEMINI.md`: Internal documentation and development conventions.

## Roadmap

- [ ] Implement Homomorphism finding algorithm between two `Magma` structures.
- [ ] Implement Isomorphism verification.
- [ ] Add support for multi-operation structures (Rings, Fields).
- [ ] Visualization of Cayley tables.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
