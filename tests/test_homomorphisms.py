import unittest
from src.core.engine import MorphismFinder
from src.algebras.structures.magma import Magma
from src.algebras.structures.semigroup import Semigroup
from src.algebras.structures.monoid import Monoid
from src.algebras.structures.group import Group
from src.algebras.structures.abelian_group import AbelianGroup
from src.algebras.structures.ring import Ring
from src.algebras.structures.unital_ring import UnitalRing
from src.algebras.structures.commutative_ring import CommutativeRing
from src.algebras.structures.field import Field


class TestHomomorphisms(unittest.TestCase):
    def setUp(self):
        self.finder = MorphismFinder(strategy_name="greedy")

    def test_magmas(self):
        # Magma M1: {0, 1} with a*b = 0
        m1 = Magma({0, 1}, lambda a, b: 0)
        # Magma M2: {0, 1} with a*b = b
        m2 = Magma({0, 1}, lambda a, b: b)
        
        homs = self.finder.find_homomorphisms(m1, m2)
        # f(a*b) = f(0). f(a)*f(b) = f(a)*f(b).
        # In M2, f(a)*f(b) = f(b). So f(0) = f(b) for all b.
        # This means f must be a constant function.
        # f(x)=0 or f(x)=1.
        self.assertEqual(len(homs), 2)
        mappings = [h.mapping for h in homs]
        self.assertIn({0: 0, 1: 0}, mappings)
        self.assertIn({0: 1, 1: 1}, mappings)

    def test_semigroups(self):
        # S1: {0, 1} mod 2 multiplication (associative)
        s1 = Semigroup({0, 1}, lambda a, b: (a * b) % 2)
        # S2: {0} multiplication
        s2 = Semigroup({0}, lambda a, b: 0)
        homs = self.finder.find_homomorphisms(s1, s2)
        self.assertEqual(len(homs), 1)
        self.assertEqual(homs[0].mapping, {0: 0, 1: 0})

    def test_z4_to_z3_monoids(self):
        # Esempio esatto del README
        # Z4 (somma mod 4) -> Z3 (somma mod 3)
        # Identità è 0. Omomorfismo deve preservare 0 (f(0)=0).
        z4 = Monoid({0, 1, 2, 3}, lambda a, b: (a + b) % 4)
        z3 = Monoid({0, 1, 2}, lambda a, b: (a + b) % 3)
        
        homs = self.finder.find_homomorphisms(z4, z3)
        
        # Solo l'omomorfismo banale f(x)=0 deve esistere.
        self.assertEqual(len(homs), 1)
        self.assertEqual(homs[0].mapping, {0: 0, 1: 0, 2: 0, 3: 0})

    def test_abelian_groups(self):
        # Z2 -> Z4
        z2 = AbelianGroup({0, 1}, lambda a, b: (a + b) % 2)
        z4 = AbelianGroup({0, 1, 2, 3}, lambda a, b: (a + b) % 4)
        homs = self.finder.find_homomorphisms(z2, z4)
        self.assertEqual(len(homs), 2)

    def test_non_abelian_groups(self):
        # S3 (Symmetric group on 3 elements)
        # Represented as permutations: (0,1,2), (0,2,1), (1,0,2), (1,2,0), (2,0,1), (2,1,0)
        elements = {
            (0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)
        }
        def s3_op(p1, p2):
            return tuple(p1[p2[i]] for i in range(3))
        
        s3 = Group(elements, s3_op)
        z2 = Group({0, 1}, lambda a, b: (a + b) % 2)
        
        homs = self.finder.find_homomorphisms(s3, z2)
        # Homomorphisms from S3 to Z2:
        # 1. Trivial: f(x) = 0
        # 2. Sign homomorphism: f(even) = 0, f(odd) = 1
        self.assertEqual(len(homs), 2)

    def test_rings(self):
        # Z4 -> Z2
        z4 = Ring({0, 1, 2, 3}, lambda a, b: (a+b)%4, lambda a, b: (a*b)%4)
        z2 = Ring({0, 1}, lambda a, b: (a+b)%2, lambda a, b: (a*b)%2)
        homs = self.finder.find_homomorphisms(z4, z2)
        self.assertEqual(len(homs), 2) # f(x)=0 and f(x)=x%2

    def test_unital_rings(self):
        # Z2 -> Z2 (unital)
        z2_a = UnitalRing({0, 1}, lambda a, b: (a+b)%2, lambda a, b: (a*b)%2)
        z2_b = UnitalRing({0, 1}, lambda a, b: (a+b)%2, lambda a, b: (a*b)%2)
        homs = self.finder.find_homomorphisms(z2_a, z2_b)
        # f(1) = 1 is mandatory for UnitalRing
        # f(0) = 0 is mandatory
        # So only f(x) = x.
        self.assertEqual(len(homs), 1)
        self.assertEqual(homs[0].mapping, {0: 0, 1: 1})

    def test_commutative_rings(self):
        # Z4 (commutative) -> Z2 (commutative)
        z4 = CommutativeRing({0, 1, 2, 3}, lambda a, b: (a+b)%4, lambda a, b: (a*b)%4)
        z2 = CommutativeRing({0, 1}, lambda a, b: (a+b)%2, lambda a, b: (a*b)%2)
        homs = self.finder.find_homomorphisms(z4, z2)
        # Since it's also a Ring (not necessarily Unital Ring in its __init__ logic unless inherited),
        # but let's check what our implementation does.
        # CommutativeRing inherits from Ring.
        self.assertEqual(len(homs), 2)

    def test_fields(self):
        # F3 -> F3
        f3_a = Field({0, 1, 2}, lambda a, b: (a+b)%3, lambda a, b: (a*b)%3)
        f3_b = Field({0, 1, 2}, lambda a, b: (a+b)%3, lambda a, b: (a*b)%3)
        homs = self.finder.find_homomorphisms(f3_a, f3_b)
        # Field inherits from UnitalRing, so f(1)=1 is mandatory.
        # This excludes f(x)=0.
        # Only identity f(x)=x exists for F3.
        self.assertEqual(len(homs), 1)
        self.assertEqual(homs[0].mapping, {0: 0, 1: 1, 2: 2})

if __name__ == '__main__':
    unittest.main()
