from typing import Set, Any
from src.utils.config.reader import ConfigFileReader
from src.utils.generators.factory import StrategyFactory

def find_minimal_generating_set(structure) -> Set[Any]:
    """
    Main entry point that delegates to the configured strategy.
    """
    strategy_name = ConfigFileReader.get_strategy_name()
    strategy = StrategyFactory.get_strategy(strategy_name)
    return strategy.find(structure)
