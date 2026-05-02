import unittest
from src.algebraic_structures import Magma, Semigroup, Monoid, Group, AbelianGroup, classify


class TestMagmaHierarchy(unittest.TestCase):
    def test_z2_group(self):
        # Z2 under addition is an Abelian Group
        elements = {0, 1}
        table = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0,
        }
        m = classify(elements, table)
        self.assertIsInstance(m, AbelianGroup)
        self.assertEqual(m.identity, 0)
        self.assertEqual(m.inverse(1), 1)

    def test_n_plus_finite(self):
        # Finite subset of N under addition: Z3 (Abelian Group)
        elements = {0, 1, 2}
        table = { (a, b): (a + b) % 3 for a in elements for b in elements }
        m = classify(elements, table)
        self.assertIsInstance(m, AbelianGroup)

    def test_n_mul_finite(self):
        # {0, 1, 2} mod 3 under multiplication is a Commutative Monoid
        # (0*x = 0, 1*x = x, 2*0=0, 2*1=2, 2*2=1)
        # Wait, mod 3 is a field, but {0, 1, 2} has 0 which has no inverse.
        elements = {0, 1, 2}
        table = { (a, b): (a * b) % 3 for a in elements for b in elements }
        m = classify(elements, table)
        self.assertIsInstance(m, Monoid)
        self.assertNotIsInstance(m, Group)
        self.assertEqual(m.identity, 1)

    def test_z_minus_not_semigroup(self):
        # Subtraction mod 3 is not associative
        elements = {0, 1, 2}
        table = { (a, b): (a - b) % 3 for a in elements for b in elements }
        m = classify(elements, table)
        self.assertIsInstance(m, Magma)
        self.assertNotIsInstance(m, Semigroup)

    def test_powerset_union(self):
        # P({1}) under union: { {}, {1} } (Commutative Monoid)
        elements = [frozenset(), frozenset({1})]
        table = { (a, b): a | b for a in elements for b in elements }
        m = classify(elements, table)
        self.assertIsInstance(m, Monoid)
        self.assertNotIsInstance(m, Group) # {1} has no inverse under union

    def test_validation_incomplete(self):
        elements = {0, 1}
        table = { (0, 0): 0, (0, 1): 1, (1, 0): 1 }
        with self.assertRaisesRegex(ValueError, "incomplete"):
            classify(elements, table)

if __name__ == '__main__':
    unittest.main()
