# MorphFinder

MorphFinder is a library for finding and classifying homomorphisms between finite algebraic structures, including: magmas, semigroups, monoids, groups, abelian groups, rings, commutative rings, unital rings, and fields.

## Theoretical Background

For an in-depth explanation of the mathematical foundations, the CSP search algorithm, and the classification of homomorphisms, consult the [THEORY.md](THEORY.md) file.

## Installation

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

The strategy for finding a system of generators for a given algebraic structure can be specified in the `config.yaml` file:

```yaml
strategy: greedy # or brute_force
```

## Usage Example

You can run the example provided in the `main.py` file to see MorphFinder in action:

```bash
python main.py
```

This script defines two simple monoids ($\mathbb{Z}_4, +, \bar{0}$) and ($\mathbb{Z}_3, +, \bar{0}$) and searches for homomorphisms between them. The expected output will be:

```text
Found 1 homomorphism(s) between given structures:
f: {0, 1, 2, 3} → {0, 1, 2} | 0 ↦ 0, 1 ↦ 0, 2 ↦ 0, 3 ↦ 0 | Properties: Trivial | Ker(f): {0, 1, 2, 3} | Im(f): {0}
```

## Running Tests

You can run the test suite using `pytest`.
