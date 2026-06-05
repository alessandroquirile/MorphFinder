from src.application.generators.base import GeneratingSetStrategy
from src.application.generators.brute_force import BruteForceStrategy
from src.application.generators.greedy import GreedyPruningStrategy


class StrategyFactory:
    """
    Factory Method Pattern to instantiate the correct strategy.
    """

    @staticmethod
    def get_strategy(name: str = "greedy") -> GeneratingSetStrategy:
        strategies = {
            "greedy": GreedyPruningStrategy,
            "brute_force": BruteForceStrategy
        }
        strategy_class = strategies.get(name.lower(), GreedyPruningStrategy)
        return strategy_class()
