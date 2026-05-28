# MorphFinder

MorphFinder is a library for finding and classifying homomorphisms between finite algebraic structures, including:
magmas, semigroups, monoids, groups, abelian groups, rings, commutative rings, unital rings, and fields.

## Installation

Clone this repository, create and activate a Python virtual environment and install all dependencies:

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

You can run the example provided in the `main.py` file to see MorphFinder in action: instantiate any algebraic structure and run `find_homomorphisms` method to find homomorphisms between the given structures. Simple as that.

```python
from src.algebras.structures.group import Group
from src.core.engine import MorphismFinder

# (Z4, +) and (Z3, +)
S = Group({0, 1, 2, 3}, lambda a, b: (a + b) % 4)
T = Group({0, 1, 2}, lambda a, b: (a + b) % 3)

# Find Hom(S,T)
finder = MorphismFinder()
homomorphisms = finder.find_homomorphisms(S, T)

# Results
print(f"Found {len(homomorphisms)} homomorphism(s) between given structures:")
for homomorphism in homomorphisms:
    print(f"{homomorphism.pretty()}")
```

The expected output is:

```text
Found 1 homomorphism(s) between given structures:
f: {0, 1, 2, 3} → {0, 1, 2} | 0 ↦ 0, 1 ↦ 0, 2 ↦ 0, 3 ↦ 0 | Properties: Trivial | Ker(f): {0, 1, 2, 3} | Im(f): {0}
```

## Configuration

The strategy for finding a system of generators for a given algebraic structure can be specified in the `config.yaml`
file:

```yaml
strategy: greedy # or brute_force
```

## Running tests

You can run the test suite using `pytest`.


## Theoretical Background

For an in-depth explanation of the mathematical foundations, the CSP search algorithm, and the classification of
homomorphisms, consult the [THEORY.md](THEORY.md) file.