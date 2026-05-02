# MorphFinder

MorphFinder is a Python-based library for working with finite algebraic structures. Its primary goal is to provide tools for verifying algebraic properties, classifying structures into a formal hierarchy, and ultimately finding and classifying morphisms between them.

## Project Overview

- **Core Logic**: Located in `src/algebraic_structures.py`. It uses a Cayley table-based representation for finite magmas.
- **Definitions**:
    - **Algebraic Structure**: A set of elements together with one or more operations defined on it.
    - **Magma**: An algebraic structure with a single binary operation.
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
- **Naming**: Use `self.operations` (a list of Cayley tables) in the base class. Single-operation structures (like `Magma`) should provide a `@property` named `cayley_table` pointing to `self.operations[0]`.
- **Types**: Use Python type hints (`typing` module) for all method signatures.
- **Quantifiers**: Use Unicode symbols `∀` (for all) and `∃` (there exists) in docstrings to define mathematical axioms formally.

### Multi-Operation Structures
- For structures with multiple operations (like Rings and Fields), follow the convention:
    - `index 0`: Addition
    - `index 1`: Multiplication
- Provide descriptive `@property` aliases (e.g., `addition_table`, `multiplication_table`) for clarity.

### Testing Practices
- **Framework**: Use `pytest` for test execution.
- **Coverage**: Every new algebraic property or classification logic must be accompanied by tests using known finite structures (e.g., $Z_n$ under addition, power sets under union/intersection).

### Morphism Finding (Planned)
- Future development will focus on implementing logic to find all homomorphisms $f: G \to H$ satisfying $f(a * b) = f(a) * f(b)$.
