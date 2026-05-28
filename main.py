from src.algebras.structures.group import Group
from src.core.engine import MorphismFinder
from src.utils.reader import ConfigFileReader

if __name__ == "__main__":
    # (Z4, +) and (Z3, +)
    S = Group({0, 1, 2, 3}, lambda a, b: (a + b) % 4)
    T = Group({0, 1, 2}, lambda a, b: (a + b) % 3)

    # Strategy configuration for finding a generating set G of S
    strategy = ConfigFileReader.get_strategy_name()
    finder = MorphismFinder(strategy_name=strategy)

    # Finding homomorphisms
    homomorphisms = finder.find_homomorphisms(S, T)

    # Results
    print(f"Found {len(homomorphisms)} homomorphism(s) between given structure:")
    for homomorphism in homomorphisms:
        print(f"{homomorphism.pretty()}")
