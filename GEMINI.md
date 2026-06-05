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

## 🏗 2. System Architecture (Clean Architecture)

The project follows Robert Martin's Clean Architecture principles to ensure decoupling of domain logic from external frameworks.

### Backend (Python/FastAPI)
Located in `backend/src/`, organized into four layers:
- **Domain:**
    - **Entities:** Algebraic structures (`algebras/`), axioms (`axioms/`), and core value objects (`carrier_set`, `homomorphism`).
    - **Services:** Specialized logic for categorical `classification`, structural `analysis`, `validators`, and `generating_set` management.
- **Application:** Orchestrates business rules via **Use Cases** (e.g., `FindHomomorphismsUseCase`) and manages strategy discovery via **Generators**.
- **Adapters:** Translates data between internal models and external formats using **Controllers**, **Gateways** (Config), and **DTOs**.
- **Infrastructure:** Framework-specific entry points like the **FastAPI** application and server configuration.

### Frontend (React/TypeScript)
Located in `frontend/src/`, organized similarly:
- **Domain:** Pure models and type definitions.
- **Application:** Custom Hooks encapsulating business and orchestration logic.
- **Adapters:** Specialized API Clients for HTTP communication.
- **UI:** Visual React components.

---

```text
MorphFinder/
├── backend/
│   ├── src/
│   │   ├── domain/
│   │   │   ├── entities/    # Algebras, Axioms, Value Objects
│   │   │   └── services/    # Analysis, Validators, Classification
│   │   ├── application/     # Use Cases and Generators
│   │   ├── adapters/        # Controllers, Gateways (Config), DTOs
│   │   └── infrastructure/  # FastAPI Entry Point
│   └── main.py              # CLI usage example
├── frontend/
│   ├── src/
│   │   ├── domain/          # Core models/types
│   │   ├── application/     # Hooks for business logic
│   │   ├── adapters/        # API clients
│   │   └── components/      # React UI
└── docker-compose.yaml
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

### Running with Docker (Recommended)

The easiest way to run the full stack is using Docker Compose:

```bash
docker-compose up --build
```

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Local Setup (Manual)

If you prefer to run services locally:

#### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.infrastructure.api.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Testing

Run the backend test suite:

```bash
cd backend
pytest
```

---

## 📝 6. Development Conventions

- **Mathematical Integrity:** New structures must inherit from `AlgebraicStructure` and register their axioms.
- **Surgical Updates:** When modifying the engine, ensure pruning heuristics remain decoupled in `Pruner`.
- **Documentation:** Maintain alignment between `README.md` examples and implementation logic.
- **Type Safety:** Use Type Hints for all mathematical mappings and structures.
