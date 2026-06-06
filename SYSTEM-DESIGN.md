# System Design: MorphFinder Architecture

MorphFinder is designed according to Robert C. Martin's Clean Architecture principles. The primary goal is the Separation of Concerns, ensuring that the core algebraic domain logic is decoupled from external frameworks, UIs, and technical details.

![Clean Architecture](https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg)

## The Dependency Rule

The overriding rule that makes this architecture work is the Dependency Rule. This rule says that source code dependencies can only point inward. Nothing in an inner circle can know anything at all about something in an outer circle.

## The Four Layers

### 1. Entities (Domain Layer)
Path: `backend/src/domain/entities/`

This is the innermost layer. It contains the most general and high-level rules of the application - the Algebraic Domain.

- Algebras: Concrete definitions of `Group`, `Ring`, `Field`, etc. (located in `algebras/`).
- Axioms: Mathematical rules like Associativity or Commutativity.
- Value Objects: Pure data carriers like `CarrierSet`, `BinaryOperation`, and `Homomorphism`.
- Foundations: The base `AlgebraicStructure` and finite analysis tools.

### 2. Use Cases (Application Layer)
Path: `backend/src/application/`

This layer contains application-specific business rules. It orchestrates the flow of data to and from the entities.

- `FindHomomorphismsUseCase`: The primary use case that executes the discovery algorithm.
- `Generators`: Strategies for finding minimal generating sets (Brute Force, Greedy), which support the use cases.

### 3. Interface Adapters
Path: `backend/src/adapters/`

This layer consists of a set of adapters that convert data from the format most convenient for the use cases and entities, to the format most convenient for some external agency such as the Web or a Database.

- Controllers: `MorphismController` translates API requests into use case inputs and orchestrates the response.
- Gateways: `ConfigFileReader` provides an interface to external configuration files.
- Data Transfer Objects (DTOs): Pydantic schemas that define the API's contract.

### 4. Frameworks & Drivers (Infrastructure Layer)
Path: `backend/src/infrastructure/`

The outermost layer is generally composed of frameworks and tools such as the Database, the Web Framework, etc.

- FastAPI: The web framework used to expose the discovery engine as a REST API.
- Docker: Containerization and orchestration for the full-stack environment.
- Web UI: The React/TypeScript frontend (located in the `frontend/` directory).


## Benefits of this Design

1. Independent of Frameworks: The algebraic engine doesn't depend on FastAPI or any other library.
2. Testable: The domain logic can be tested without the UI, Database, or Web Server.
3. Independent of UI: The React frontend can be swapped for a CLI or a mobile app without changing the core logic.
4. Flexible Configuration: The way we load strategies (YAML, Env, Database) can change without affecting the application rules.

## Domain Modeling and Axiom Validation

### Algebra Hierarchy
The domain layer models finite algebraic structures using object-oriented inheritance to mirror mathematical categorization:

```mermaid
classDiagram
    AlgebraicStructure <|-- Magma
    Magma <|-- Semigroup
    Semigroup <|-- Monoid
    Monoid <|-- Group
    Group <|-- AbelianGroup
    
    AlgebraicStructure <|-- Ring
    Ring <|-- CommutativeRing
    Ring <|-- UnitalRing
    UnitalRing <|-- Field
    CommutativeRing <|-- Field

    class AlgebraicStructure {
        +CarrierSet carrier
        +Tuple[BinaryOperation] operations
        +List[Axiom] axioms
        +validate(Validator)
    }
    class Magma {
        +FiniteBinaryOperation operation
    }
    class Monoid {
        +Any identity
    }
    class Group {
        +Dict inverse_map
        +inverse(a) Any
    }
```

### Axiom Validation Design
When a concrete algebra (e.g., `Group`) is instantiated, it automatically appends its required axioms (e.g., `AssociativityAxiom`, `IdentityExistenceAxiom`, `InverseExistenceAxiom`) and validates them against the provided operations using the `FiniteAxiomValidator` (Domain Service). 

If any axiom check fails, a `ValueError` is raised, preventing the construction of mathematically invalid structures.

## Generating Set Discovery (Strategy Pattern)

To optimize backtracking, the search space is restricted from $O(|T|^{|S|})$ to $O(|T|^{|G|})$ by discovering a generating set $G$ of the source structure. MorphFinder employs the Strategy Pattern to decouple the discovery method from the main usecase:

```mermaid
classDiagram
    class GeneratingSetStrategy {
        <<abstract>>
        +find(AlgebraicStructure) Set
    }
    GeneratingSetStrategy <|-- BruteForceStrategy
    GeneratingSetStrategy <|-- GreedyPruningStrategy
    
    class BruteForceStrategy {
        +find(AlgebraicStructure) Set
    }
    class GreedyPruningStrategy {
        +find(AlgebraicStructure) Set
    }
    
    class StrategyFactory {
        +get_strategy(name) GeneratingSetStrategy
    }
```

* BruteForceStrategy: Finds the globally minimal generating set by checking all subsets in increasing size.
* GreedyPruningStrategy: Greedily accumulates elements to maximize closure size, then prunes redundant elements. Faster for larger structures but doesn't guarantee global minimality.

## Sequence Diagrams

### Web UI
This flow shows how the system handles HTTP requests from the frontend, involving data conversion and DTOs.

```mermaid
sequenceDiagram
    actor User
    participant Controller as MorphismController
    participant Config as ConfigFileReader
    participant UseCase as FindHomomorphismsUseCase
    participant Factory as StrategyFactory
    participant Gen as Genealogy
    participant Pruner
    participant Classifier

    User->>Controller: HTTP Request (MorphismRequest)
    Controller->>Controller: _build_structure(source)
    Controller->>Controller: _build_structure(target)
    Controller->>Config: get_strategy_name()
    Config-->>Controller: strategy_name
    Controller->>UseCase: FindHomomorphismsUseCase(strategy_name)
    UseCase->>Factory: get_strategy(strategy_name)
    Factory-->>UseCase: strategy
    Controller->>UseCase: execute(source, target)
    
    activate UseCase
    UseCase->>UseCase: Find generators using strategy
    UseCase->>Gen: Genealogy(source, generators)
    UseCase->>UseCase: _backtrack(0, all_to_map, base_mapping)
    
    activate UseCase
    loop Recursion / Pruning
        UseCase->>Pruner: is_assignment_possible(gen, target_val)
        Pruner-->>UseCase: boolean
    end
    deactivate UseCase

    opt On Leaf of Search Tree (all generators mapped)
        UseCase->>Gen: propagate(current_mapping, target)
        Gen-->>UseCase: full_mapping
        UseCase->>UseCase: _is_valid_homomorphism(full_mapping)
        opt If valid
            UseCase->>Classifier: classify(temp_hom)
            Classifier-->>UseCase: properties
            UseCase->>Classifier: get_image(full_mapping)
            Classifier-->>UseCase: image
            UseCase->>Classifier: get_kernel(full_mapping, target)
            Classifier-->>UseCase: kernel
        end
    end

    UseCase-->>Controller: List[Homomorphism]
    deactivate UseCase
    Controller-->>User: HTTP Response (MorphismResponse)
```

### Python API
This flow demonstrates how the application can be used directly, bypassing the Controller and DTO layers for programmatic access.

```mermaid
sequenceDiagram
    actor Script as main.py
    participant UseCase as FindHomomorphismsUseCase
    participant Gen as Genealogy
    participant Pruner
    participant Classifier

    Script->>UseCase: FindHomomorphismsUseCase()
    Script->>UseCase: execute(S, T)
    activate UseCase
    UseCase->>UseCase: Find generators
    UseCase->>Gen: Genealogy(S, generators)
    UseCase->>UseCase: _backtrack()
    loop Backtracking
        UseCase->>Pruner: is_assignment_possible()
        Pruner-->>UseCase: boolean
        opt All mapped
            UseCase->>Gen: propagate()
            Gen-->>UseCase: full_mapping
            UseCase->>Classifier: classify / get_image / get_kernel
            Classifier-->>UseCase: metadata
        end
    end
    UseCase-->>Script: List[Homomorphism]
    deactivate UseCase
    Script->>Script: print results
```

