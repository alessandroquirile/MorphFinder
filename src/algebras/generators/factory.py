from src.algebras.generators.base import GeneratingSetStrategy
from src.algebras.generators.brute_force import BruteForceStrategy
from src.algebras.generators.greedy import GreedyPruningStrategy
from src.utils.reader import ConfigFileReader


class StrategyFactory:
    """
    Factory Method Pattern to instantiate the correct strategy.
    """

    @staticmethod
    def get_strategy(name: str = "") -> GeneratingSetStrategy:
        if not name:
            try:
                name = ConfigFileReader.get_strategy_name()
            except (FileNotFoundError, KeyError):
                name = "greedy"

        strategies = {
            "greedy": GreedyPruningStrategy,
            "brute_force": BruteForceStrategy
        }
        strategy_class = strategies.get(name.lower(), GreedyPruningStrategy)
        return strategy_class()
