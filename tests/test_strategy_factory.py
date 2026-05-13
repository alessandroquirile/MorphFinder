import unittest
from unittest.mock import patch
from src.algebras.group import Group
from src.utils.generators.discovery import find_minimal_generating_set
from src.utils.generators.factory import StrategyFactory
from src.utils.generators.greedy import GreedyPruningStrategy
from src.utils.generators.brute_force import BruteForceStrategy

class TestStrategyFactory(unittest.TestCase):
    
    def setUp(self):
        # Klein Four-Group: {e, a, b, c} where x*x = e, a*b = c
        self.elements = {'e', 'a', 'b', 'c'}
        self.table = {
            ('e', 'e'): 'e', ('e', 'a'): 'a', ('e', 'b'): 'b', ('e', 'c'): 'c',
            ('a', 'e'): 'a', ('a', 'a'): 'e', ('a', 'b'): 'c', ('a', 'c'): 'b',
            ('b', 'e'): 'b', ('b', 'a'): 'c', ('b', 'b'): 'e', ('b', 'c'): 'a',
            ('c', 'e'): 'c', ('c', 'a'): 'b', ('c', 'b'): 'a', ('c', 'c'): 'e',
        }
        self.group = Group(self.elements, lambda x, y: self.table[(x, y)], identity='e')

    def test_factory_creation(self):
        """Verify that StrategyFactory returns the correct classes."""
        greedy = StrategyFactory.get_strategy("greedy")
        self.assertIsInstance(greedy, GreedyPruningStrategy)
        
        brute = StrategyFactory.get_strategy("brute_force")
        self.assertIsInstance(brute, BruteForceStrategy)
        
        # Default case
        default = StrategyFactory.get_strategy("unknown")
        self.assertIsInstance(default, GreedyPruningStrategy)

    @patch('src.utils.config.reader.ConfigFileReader.get_strategy_name')
    def test_find_minimal_generating_set_with_greedy(self, mock_get_name):
        """Verify find_minimal_generating_set uses Greedy strategy when configured."""
        mock_get_name.return_value = "greedy"
        gen_set = find_minimal_generating_set(self.group)
        self.assertEqual(len(gen_set), 2)
        self.assertNotIn('e', gen_set)

    @patch('src.utils.config.reader.ConfigFileReader.get_strategy_name')
    def test_find_minimal_generating_set_with_brute_force(self, mock_get_name):
        """Verify find_minimal_generating_set uses BruteForce strategy when configured."""
        mock_get_name.return_value = "brute_force"
        gen_set = find_minimal_generating_set(self.group)
        self.assertEqual(len(gen_set), 2)
        self.assertNotIn('e', gen_set)

    def test_brute_force_strategy_directly(self):
        """Explicitly test BruteForceStrategy."""
        strategy = BruteForceStrategy()
        gen_set = strategy.find(self.group)
        self.assertEqual(len(gen_set), 2)
        self.assertNotIn('e', gen_set)

if __name__ == '__main__':
    unittest.main()
