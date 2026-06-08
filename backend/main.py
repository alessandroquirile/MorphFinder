from src.domain.entities.algebras.group import Group
from src.application.use_cases.find_homomorphisms import FindHomomorphisms

# Example Python API usage

if __name__ == "__main__":
    # (Z4, +) and (Z3, +)
    S = Group({0, 1, 2, 3}, lambda a, b: (a + b) % 4)
    T = Group({0, 1, 2}, lambda a, b: (a + b) % 3)

    # Find Hom(S,T)
    finder = FindHomomorphisms()
    homomorphisms = finder.execute(S, T)

    # Results
    print(f"Found {len(homomorphisms)} homomorphism(s) between given structures:")
    for homomorphism in homomorphisms:
        print(f"{homomorphism.pretty()}")
