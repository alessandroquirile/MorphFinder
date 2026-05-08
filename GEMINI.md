# 🌀 MorphFinder: Project Blueprint

> **Status:** Implementation Phase (Algebras Complete)  
> **Concept:** Automated Algebraic Morphism Discovery & Categorical Visualization

---

## 📌 1. Project Vision

**MorphFinder** is a computational algebra tool designed to explore the relationships between finite algebraic
structures. It uses optimized backtracking algorithms to find, classify, and visualize homomorphisms, treating algebras
as objects and mappings as morphisms within a categorical framework.

## 🏗 2. System Architecture (`src/` layout)

The project is structured to separate mathematical logic from search optimization and visualization.

```text
src/
├── core/                   # The CSP-based backtracking engine
│   ├── backtracking.py     # Main recursive search logic
│   ├── pruning.py          # Algebraic invariant filters (Order, Idempotency)
│   └── classification.py   # Labeling (Mono/Epi/Iso/Auto)
│
├── algebras/               # Structural definitions (Modular & Readable)
│   ├── base.py             # BinaryOperation & CayleyTable abstractions
│   ├── magma.py            # Basic closure logic
│   ├── semigroup.py        # Associative structures
│   ├── monoid.py           # Identity element & orders
│   ├── group.py            # Inverses & group properties
│   ├── abelian_group.py    # Commutative groups
│   ├── ring.py             # Base Ring class & Zero/Unity logic
│   ├── commutative_ring.py # Commutative multiplicative structures
│   ├── unity_rings.py      # Rings with Multiplicative Identity
│   └── field.py            # Commutative Unity Rings with all non-zero invertible
│
├── graph/                  # Categorical visualization
│   ├── builder.py          # Maps structures to Nodes and morphisms to Edges
│   └── exporters.py        # Export to JSON, DOT, or Cytoscape.js
│
├── utils/                  # Support modules
│   ├── generators.py       # Minimum generating set discovery
│   └── sympy_bridge.py     # Conversion between SymPy objects
│
└── api.py                  # Main entry point for the MorphFinder class
```

## 🧠 3. Core Algorithm: Optimized Backtracking

To find all homomorphisms $f: A \to B$ where $f(a * b) = f(a) * f(b)$, MorphFinder treats the problem as a **Constraint
Satisfaction Problem (CSP)**.

### Key Strategies:

1. **Minimum Generating Set ($G_{min}$):** Instead of mapping all elements of $A$, we only map a minimum set of
   generators. This reduces search space from $|B|^{|A|}$ to $|B|^{|G_{min}|}$.
2. **Pruning Heuristics:**
    * **Groups:** The order of $f(g)$ in $B$ must divide the order of $g$ in $A$.
    * **Rings:** $f(1_A) = 1_B$ must hold for unital rings.
    * **Fields:** Characteristics must match ($char(A) = char(B)$).
    * **Semigroups:** Idempotent elements ($x^2=x$) must map to idempotent elements.
3. **Consistency Checking:** As each generator is mapped, the engine checks for violations of structural relations
   before proceeding deeper into the recursion.

## 📈 4. Development Roadmap

Development follows a path from maximum structural rigidity to maximum entropy.

1. **Phase 1: Foundation (COMPLETED):** Modular implementation of Magmas, Semigroups, Monoids, Groups, and Rings with
   structural invariants (generating sets, orders, centers).
2. **Phase 2: CSP Engine:** Implementation of the optimized backtracking search and pruning heuristics.
3. **Phase 4: Fields & Galois Theory (COMPLETED):** Implementation of $\mathbb{F}_{p^n}$ and field homomorphisms.
4. **Phase 5: Lattices:** Mapping order-preserving relations ($\le$) and Join/Meet operations.

## 🏷 5. Categorical Classification

Every discovered morphism is automatically classified based on its properties:

* **Monomorphism:** Injective mapping.
* **Epimorphism:** Surjective mapping.
* **Isomorphism:** Bijective mapping (Structural identity).
* **Endomorphism:** Mapping of a structure to itself ($A \to A$).
* **Automorphism:** A bijective endomorphism.

## 🛠 6. Tech Stack

* **Language:** Python 3.10+
* **Math Engine:** **SymPy** (for structure generation and symbolic pre-processing).
* **Storage:** **Dictionary-based Cayley Tables** (optimized for readability and mathematical clarity).
* **Visualization:** Graphviz / Cytoscape.js.

