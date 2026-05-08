# MorphFinder

MorphFinder is a Python library designed for the study and exploration of finite algebraic structures. It provides a
modular, readable framework for verifying algebraic axioms and finding relationships (morphisms) between structures
using optimized backtracking.

## Features

- **Modular Formal Hierarchy**: Implements a strict inheritance-based model across dedicated modules:
    - `Magma` → `Semigroup` → `Monoid` → `Group` → `AbelianGroup`.
- **Multi-Operation Structures**: Support for `Ring`, `CommutativeRing`, `UnityRing`, and `Field` structures using composition-based logic.
- **Algebraic Discovery**: Built-in logic to identify:
    - **Zero Divisors**: Discovery of left, right, and two-sided zero divisors.
    - **Cancellation**: Verification of left/right cancellation properties.
    - **Units & Inverses**: Identification of invertible elements and unity.
- **Search Optimization (CSP)**: Built-in invariants to facilitate high-speed morphism discovery:
    - **Generating Sets**: Find minimal subsets that generate the entire structure.
    - **Element Orders**: Pre-computed orders for pruning search spaces.
    - **Idempotents & Centers**: Structural invariants for mapping constraints.
- **Readable Abstractions**:
    - `CayleyTable`: Efficient and readable data storage.
    - `BinaryOperation`: Textbook-like notation (`self.op(a, b)`) for mathematical clarity.

## Usage

```python
from src.algebras.field import Field

# Define Z5 (integers modulo 5) as a Field
elements = set(range(5))
add_op = lambda a, b: (a + b) % 5
mul_op = lambda a, b: (a * b) % 5

z5 = Field(elements, add_op, mul_op)

print(f"Structure: {type(z5).__name__}")
print(f"Zero: {z5.zero}")
print(f"Unity: {z5.unity}")
print(f"Zero Divisors: {z5.find_zero_divisors()}") # Empty set for a field
print(f"Invertible Elements: {z5.find_invertible_elements()}") # {1, 2, 3, 4}
```

## Installation

### Prerequisites

- Python 3.10+

### Running Tests

MorphFinder uses `pytest` for its test suite.

```bash
.venv/bin/pytest tests/test_algebras_modular.py
```

## Project Structure

- `src/algebras/`: Core algebraic logic.
    - `base.py`: Operation and table abstractions.
    - `magma.py` to `abelian_group.py`: Single-operation hierarchy.
    - `ring.py` to `field.py`: Dual-operation structures.
- `src/core/`: CSP-based backtracking and morphism discovery (In Progress).
- `tests/`: Comprehensive validation suite.

## Roadmap

- [ ] Implement Optimized Backtracking Engine for Homomorphisms.
- [ ] Implement Isomorphism/Automorphism classification.
- [x] Add support for Fields and Galois Theory.
- [ ] Add support for Lattices and Order Relations.
- [ ] Visualization of Categorical Morphisms (Graphviz/Cytoscape).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
