from src.utils.generators.base import GeneratingSetStrategy
from src.utils.generators.greedy import GreedyPruningStrategy
from src.utils.generators.brute_force import BruteForceStrategy

class StrategyFactory:
    """
    Factory Method Pattern to instantiate the correct strategy.
    """

    @staticmethod
    def get_strategy(name: str) -> GeneratingSetStrategy:
        strategies = {
            "greedy": GreedyPruningStrategy,
            "brute_force": BruteForceStrategy
        }
        strategy_class = strategies.get(name.lower(), GreedyPruningStrategy)
        return strategy_class()
