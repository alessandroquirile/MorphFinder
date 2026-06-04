# MorphFinder

MorphFinder is a computational tool for finding and classifying homomorphisms between finite algebraic structures (
magmas, semigroups, monoids, groups, rings, and fields) using an optimized CSP-based engine.

## Project Structure

The project is organized as a monorepo:

- `backend`: FastAPI service containing the algebraic engine and search logic.
- `frontend`: React + Vite application for interactive visualization of morphisms between magmas, semigroups, monoids,
  and groups. (Rings and fields are currently only supported via the backend API).

## Quick Start

### Docker

The easiest way to run MorphFinder is using Docker Compose. This will start both the backend API and the frontend
dashboard.

```bash
docker-compose up --build
```

- Frontend UI: http://localhost:5173
- Backend API: http://localhost:8000

## Usage (Web UI)

![Web UI](assets/webui.png)

> **Note:** The Web UI is currently limited to magmas, semigroups, monoids, and groups. To analyze rings and fields,
> please use the Python API.

The Web UI provides an interactive way to discover and visualize morphisms between algebraic structures:

1. Add Structures: Click "+ Add Source" or "+ Add Target" to open the Structure Builder.
2. Define Structure:
    - Enter the elements (e.g., `0, 1, 2, 3` or `a, b, c`).
    - Choose an operation method: either fill the Cayley's Table or specify the Formula (e.g., `(a + b) % n`)
3. Find Morphisms: Once both Source and Target are defined, click the Search icon to initiate the computation.
4. Visualize Results:
    - The Sidebar will display all discovered homomorphisms.
    - Click on a specific homomorphism in the sidebar to view its mapping, image, kernel, and algebraic properties in
      the central canvas.

## Usage (Python API)

You can use the core library directly within the `backend/` directory:

```shell
from src.algebras.structures.group import Group
from src.core.engine import MorphismFinder

# Define structures: (Z4, +) and (Z2, +)
Z4 = Group({0, 1, 2, 3}, lambda a, b: (a + b) % 4)
Z3 = Group({0, 1}, lambda a, b: (a + b) % 2)

# Find Hom(Z4, Z3)
finder = MorphismFinder()
homomorphisms = finder.find_homomorphisms(Z4, Z3)

# Found 1 homomorphism(s) between given structures:
# f: {0, 1, 2, 3} → {0, 1, 2} | 0 ↦ 0, 1 ↦ 0, 2 ↦ 0, 3 ↦ 0 
# Properties: Trivial | Ker(f): {0, 1, 2, 3} | Im(f): {0}
for hom in homomorphisms:
    print(hom.pretty())
```

<!--
## Manual Installation

If you prefer to run the components separately:

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

-->

## Running Tests

To run the backend test suite:

```bash
cd backend
pytest
```

## Theoretical Background

For an in-depth explanation of the mathematical foundations, the CSP search algorithm, and the classification of
homomorphisms, consult the [THEORY.md](THEORY.md) file.
