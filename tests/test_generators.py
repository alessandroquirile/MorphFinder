import unittest
from src.algebras.abelian_group import AbelianGroup
from src.algebras.group import Group
from src.algebras.ring import Ring
from src.algebras.magma import Magma
from src.utils.generators.discovery import find_minimal_generating_set

class TestGenerators(unittest.TestCase):
    def test_minimal_gen_set_z4(self):
        # Z4 under addition: Minimal generating set should be {1} or {3}
        elements = {0, 1, 2, 3}
        op = lambda a, b: (a + b) % 4
        g = AbelianGroup(elements, op)
        
        gen_set = find_minimal_generating_set(g)
        self.assertEqual(len(gen_set), 1)
        self.assertTrue(1 in gen_set or 3 in gen_set)

    def test_minimal_gen_set_klein4(self):
        # Klein Four-Group: {e, a, b, c} where x*x = e, a*b = c
        # Any two non-identity elements generate the group.
        elements = {'e', 'a', 'b', 'c'}
        table = {
            ('e', 'e'): 'e', ('e', 'a'): 'a', ('e', 'b'): 'b', ('e', 'c'): 'c',
            ('a', 'e'): 'a', ('a', 'a'): 'e', ('a', 'b'): 'c', ('a', 'c'): 'b',
            ('b', 'e'): 'b', ('b', 'a'): 'c', ('b', 'b'): 'e', ('b', 'c'): 'a',
            ('c', 'e'): 'c', ('c', 'a'): 'b', ('c', 'b'): 'a', ('c', 'c'): 'e',
        }
        g = Group(elements, lambda x, y: table[(x, y)], identity='e')
        
        gen_set = find_minimal_generating_set(g)
        # Should be size 2, and should not contain the identity 'e'
        self.assertEqual(len(gen_set), 2)
        self.assertNotIn('e', gen_set)

    def test_minimal_gen_set_z6_ring(self):
        # Z6 Ring: (Z6, +, *). 
        # The constants include zero (0) and unity (1).
        # Since 1 generates the additive group (Z6, +), the minimal generating set should be empty.
        elements = set(range(6))
        add_op = lambda a, b: (a + b) % 6
        mul_op = lambda a, b: (a * b) % 6
        r = Ring(elements, add_op, mul_op)
        
        gen_set = find_minimal_generating_set(r)
        self.assertEqual(len(gen_set), 0)

    def test_magma_non_associative(self):
        # Subtraction mod 3: (a - b) % 3
        # In this structure, 1 generates {0, 1, 2} (1-1=0, 0-1=2)
        elements = {0, 1, 2}
        op = lambda a, b: (a - b) % 3
        m = Magma(elements, op)
        
        gen_set = find_minimal_generating_set(m)
        self.assertEqual(len(gen_set), 1)
        self.assertIn(gen_set, [{1}, {2}])

if __name__ == '__main__':
    unittest.main()
