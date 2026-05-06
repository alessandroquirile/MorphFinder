# MorphFinder

MorphFinder is a Python library designed for the study and exploration of finite algebraic structures. It provides a modular, readable framework for verifying algebraic axioms and finding relationships (morphisms) between structures using optimized backtracking.

## Features

- **Modular Formal Hierarchy**: Implements a strict inheritance-based model across dedicated modules:
    - `Magma` → `Semigroup` → `Monoid` → `Group` → `AbelianGroup`.
- **Multi-Operation Structures**: Support for `Ring` structures using composition-based logic (Additive Abelian Group + Multiplicative Semigroup).
- **Search Optimization (CSP)**: Built-in invariants to facilitate high-speed morphism discovery:
    - **Generating Sets**: Find minimal subsets that generate the entire structure.
    - **Element Orders**: Pre-computed orders for pruning search spaces.
    - **Idempotents & Centers**: Structural invariants for mapping constraints.
- **Readable Abstractions**:
    - `CayleyTable`: Efficient and readable data storage.
    - `BinaryOperation`: Textbook-like notation (`self.op(a, b)`) for mathematical clarity.

## Usage

```python
from src.algebras.abelian_group import AbelianGroup
from src.algebras.ring import Ring

# Define Z2 (integers modulo 2) under addition
elements = {0, 1}
add_op = lambda a, b: (a + b) % 2

# Instantiate an Abelian Group
z2_add = AbelianGroup(elements, add_op)

print(f"Structure: {type(z2_add).__name__}")
print(f"Identity: {z2_add.identity}")
print(f"Generating Set: {z2_add.find_generating_set()}")

# Define Z2 as a Ring
mul_op = lambda a, b: (a * b) % 2
z2_ring = Ring(elements, add_op, mul_op)

print(f"Ring Addition (1+1): {z2_ring.add(1, 1)}")
print(f"Ring Multiplication (1*1): {z2_ring.mul(1, 1)}")
```

## Installation

### Prerequisites

- Python 3.10+

### Running Tests

MorphFinder uses `pytest` for its test suite.

```bash
pytest tests/test_algebras_modular.py
```

## Project Structure

- `src/algebras/`: Core algebraic logic.
    - `base.py`: Operation and table abstractions.
    - `magma.py` to `abelian_group.py`: Single-operation hierarchy.
    - `ring.py`: Multi-operation structures.
- `src/core/`: CSP-based backtracking and morphism discovery (In Progress).
- `tests/`: Comprehensive validation suite.

## Roadmap

- [ ] Implement Optimized Backtracking Engine for Homomorphisms.
- [ ] Implement Isomorphism/Automorphism classification.
- [ ] Add support for Fields and Galois Theory.
- [ ] Add support for Lattices and Order Relations.
- [ ] Visualization of Categorical Morphisms (Graphviz/Cytoscape).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
