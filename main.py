from src.algebras.structures.group import Group
from src.core.engine import MorphismFinder

if __name__ == "__main__":
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
