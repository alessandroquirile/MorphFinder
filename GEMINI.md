# 🌀 MorphFinder: Project Blueprint

> **Status:** Implementation Phase (CSP Engine & Classification Complete)  
> **Concept:** Automated Algebraic Morphism Discovery & Categorical Visualization

---

## 📌 1. Project Overview

**MorphFinder** is a computational algebra tool designed to explore relationships between finite algebraic structures.
It treats algebras as objects and mappings as morphisms within a categorical framework, using optimized backtracking
algorithms to find and classify homomorphisms.

### Key Technologies:

- **Language:** Python 3.10+
- **Testing:** Pytest
- **Logic:** CSP (Constraint Satisfaction Problem) with Pruning Heuristics
- **Math Foundations:** Group Theory, Ring Theory, Category Theory, First Isomorphism Theorem.

---

## 🏗 2. System Architecture (`src/` layout)

The project separates mathematical definitions from search optimization and classification logic.

```text
src/
├── core/                   # The CSP-based backtracking engine
│   ├── engine.py           # Main MorphismFinder & Homomorphism classes
│   ├── genealogy.py        # Propagation 'recipes' (Phase 1)
│   ├── pruning.py          # Algebraic invariant filters (Order, Idempotency)
│   └── classification.py   # Labeling (Mono/Epi/Iso/Endo/Auto) using Isomorphism Theorems
│
├── algebras/               # Structural definitions (Modular & Readable)
│   ├── base.py             # BinaryOperation & CarrierSet abstractions
│   ├── structures/         # Concrete types (Magma, Group, Ring, Field, etc.)
│   ├── axioms/             # Axiomatic definitions (Associativity, Identity, etc.)
│   ├── analysis/           # Tools for identity discovery and magma analysis
│   ├── generators/         # Generating set discovery (BruteForce, Greedy)
│   └── validation/         # Axiom verification logic
│
└── utils/                  # Support modules
    └── reader.py           # Configuration and file utilities
```

---

## 🧠 3. Core Algorithm: Optimized Backtracking (CSP)

MorphFinder solves for $f: S \to T$ such that $f(a * b) = f(a) \square f(b)$ using a three-phase CSP approach:

1. **Phase 1: Genealogy:** Build a recipe $h(x)$ for all elements $x \in S \setminus G$, where $G$ is a minimal
   generating set.
2. **Phase 2: Backtracking:** Systematically assign values from $T$ to the generators $G$. Propagate assignments to the
   rest of $S$ using the genealogy recipe.
3. **Phase 3: Validation:** Verify preservation of operations and distinguished constants (Zero, Unity).

### Pruning Strategies:

- **Idempotency:** $x^2 = x \implies f(x)^2 = f(x)$.
- **Group Order:** The order of $f(g)$ in $T$ must divide the order of $g$ in $S$.

---

## 🏷 4. Categorical Classification

Morphisms are classified based on the **First Isomorphism Theorem** and **Congruence Classes**:

- **Monomorphism ($f: S \hookrightarrow T$):** Injective. Checked via $|S| = |Im(f)|$.
- **Epimorphism ($f: S \twoheadrightarrow T$):** Surjective. Checked via $|Im(f)| = |T|$.
- **Isomorphism ($f: S \cong T$):** Bijective.
- **Endomorphism ($f: S \to S$):** $S = T$.
- **Automorphism ($f: S \cong S$):** Bijective endomorphism.

---

## 🛠 5. Building and Running

### Setup

Create a virtual environment, activate it, and install dependencies:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The default generator strategy can be set in `config.yaml`:

```yaml
strategy: greedy # or brute_force
```

### Testing

Run the suite using `pytest`:

```bash
pytest
```

---

## 📝 6. Development Conventions

- **Mathematical Integrity:** New structures must inherit from `AlgebraicStructure` and register their axioms.
- **Surgical Updates:** When modifying the engine, ensure pruning heuristics remain decoupled in `Pruner`.
- **Documentation:** Maintain alignment between `README.md` examples and implementation logic.
- **Type Safety:** Use Type Hints for all mathematical mappings and structures.
