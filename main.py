from src.algebras.structures.monoid import Monoid
from src.core.engine import MorphismFinder
from src.utils.reader import ConfigFileReader

if __name__ == "__main__":
    # (Z4, +, 0) and (Z3, +, 0)
    S = Monoid({0, 1, 2, 3}, lambda a, b: (a + b) % 4, identity=0)
    T = Monoid({0, 1, 2}, lambda a, b: (a + b) % 3, identity=0)

    # Strategy configuration for finding a generating set G of S
    strategy = ConfigFileReader.get_strategy_name()
    finder = MorphismFinder(strategy_name=strategy)

    # Finding homomorphisms
    homomorphisms = finder.find_homomorphisms(S, T)

    # Results
    print(f"Found {len(homomorphisms)} homomorphism(s)")
    for homomorphism in homomorphisms:
        print(f"{homomorphism.pretty()}")
