# MorphFinder

MorphFinder is a Python-based library for working with finite algebraic structures. Its primary goal is to provide tools for verifying algebraic properties, classifying structures into a formal hierarchy, and ultimately finding and classifying morphisms between them.

## Project Overview

- **Core Logic**: Located in `src/algebraic_structures.py`. It uses a Cayley table-based representation for finite magmas.
- **Architecture**: A strict inheritance hierarchy representing mathematical axioms:
    - `AlgebraicStructure` (Base)
    - `Magma` (Set + Operation)
    - `Semigroup` (Associative Magma)
    - `Monoid` (Semigroup + Identity)
    - `Group` (Monoid + Inverses)
    - `AbelianGroup` (Commutative Group)
- **Factory Pattern**: The `classify()` function automatically identifies the most specific subclass for a given set and Cayley table.

## Building and Running

### Prerequisites
- Python 3.12+
- `pytest` for running tests.

### Key Commands
- **Run Tests**: `pytest` or `python3 -m pytest tests/test_algebraic_structures.py`
- **Install Dependencies**: (Currently only `pytest` is required) `pip install pytest`

## Development Conventions

### Coding Style
- **Naming**: Use `cayley_table` for internal operation storage and `op(a, b)` for the public operation interface.
- **Types**: Use Python type hints (`typing` module) for all method signatures.
- **Quantifiers**: Use Unicode symbols `∀` (for all) and `∃` (there exists) in docstrings to define mathematical axioms formally.

### Testing Practices
- **Framework**: Use `pytest` for test execution.
- **Coverage**: Every new algebraic property or classification logic must be accompanied by tests using known finite structures (e.g., $Z_n$ under addition, power sets under union/intersection).

### Morphism Finding (Planned)
- Future development will focus on implementing logic to find all homomorphisms $f: G \to H$ satisfying $f(a * b) = f(a) * f(b)$.
