import unittest

from src.algebras.abelian_group import AbelianGroup
from src.algebras.group import Group
from src.algebras.magma import Magma
from src.algebras.monoid import Monoid
from src.algebras.ring import Ring
from src.algebras.commutative_ring import CommutativeRing
from src.algebras.semigroup import Semigroup


class TestAlgebrasModular(unittest.TestCase):
    def test_z2_abelian_group(self):
        # Z2 under addition
        elements = {0, 1}
        g = AbelianGroup(elements, lambda a, b: (a + b) % 2)
        self.assertEqual(g.identity, 0)
        self.assertEqual(g.inverse(1), 1)
        self.assertEqual(g.op(1, 1), 0)

    def test_z3_abelian_group(self):
        # Z3 under addition
        elements = {0, 1, 2}
        g = AbelianGroup(elements, lambda a, b: (a + b) % 3)
        self.assertEqual(g.identity, 0)
        self.assertEqual(g.inverse(1), 2)
        self.assertEqual(g.op(1, 2), 0)

    def test_monoid_not_group(self):
        # {0, 1, 2} mod 3 under multiplication is a Monoid but not a Group
        elements = {0, 1, 2}
        m = Monoid(elements, lambda a, b: (a * b) % 3)
        self.assertEqual(m.identity, 1)
        with self.assertRaisesRegex(ValueError, "Inverse elements not found"):
            Group(elements, lambda a, b: (a * b) % 3)

    def test_semigroup_not_monoid(self):
        # Even numbers under multiplication (no identity in finite set like {2, 4, 6})
        # Actually, let's use a simpler one: {0, 2} mod 4 under multiplication is associative but has no identity (1 is not in set)
        elements = {0, 2}
        s = Semigroup(elements, lambda a, b: (a * b) % 4)
        self.assertTrue(s.is_associative())
        with self.assertRaisesRegex(ValueError, "Identity element not found"):
            Monoid(elements, lambda a, b: (a * b) % 4)

    def test_magma_not_semigroup(self):
        # Subtraction mod 3 is not associative
        elements = {0, 1, 2}
        m = Magma(elements, lambda a, b: (a - b) % 3)
        with self.assertRaisesRegex(ValueError, "Associativity violated"):
            Semigroup(elements, lambda a, b: (a - b) % 3)

    def test_z2_ring(self):
        # Z2 as a ring
        elements = {0, 1}
        add_op = lambda a, b: (a + b) % 2
        mul_op = lambda a, b: (a * b) % 2
        r = Ring(elements, add_op, mul_op)
        self.assertEqual(r.zero, 0)
        self.assertEqual(r.additive_abelian_group.op(1, 1), 0)
        self.assertEqual(r.multiplicative_semigroup.op(1, 1), 1)

    def test_zero_divisors_z6(self):
        # Z6 under addition and multiplication
        elements = set(range(6))
        add_op = lambda a, b: (a + b) % 6
        mul_op = lambda a, b: (a * b) % 6
        r = CommutativeRing(elements, add_op, mul_op)
        
        zero_divisors = r.find_zero_divisors()
        # 2*3=0, 3*2=0, 3*4=0, 4*3=0
        self.assertEqual(zero_divisors, {2, 3, 4})

    def test_ring_propositions_z6(self):
        # Z6 under addition and multiplication
        elements = set(range(6))
        add_op = lambda a, b: (a + b) % 6
        mul_op = lambda a, b: (a * b) % 6
        r = CommutativeRing(elements, add_op, mul_op)
        
        # 1. Unity exists and is 1
        self.assertEqual(r.unity, 1)
        
        # 2. Zero divisors in Z6 are {2, 3, 4}
        zero_divisors = r.find_zero_divisors()
        self.assertEqual(zero_divisors, {2, 3, 4})
        
        # 3. Cancellable elements in Z6 are {1, 5}
        cancellable = r.find_cancellable_elements()
        self.assertEqual(cancellable, {1, 5})
        
        # 4. Invertible elements (units) in Z6 are {1, 5} (elements coprime to 6)
        units = r.find_invertible_elements()
        self.assertEqual(units, {1, 5})
        
        # 5. Proposition: Each non-zero element is either a zero divisor XOR cancellable
        non_zero_elements = elements - {r.zero}
        for a in non_zero_elements:
            is_zd = a in zero_divisors
            is_can = a in cancellable
            # XOR logic: (A or B) and not (A and B)
            self.assertTrue((is_zd or is_can) and not (is_zd and is_can), f"Element {a} failed XOR proposition")

        # 6. Unity is cancellable
        self.assertTrue(r.is_cancellable(r.unity))
        
        # 7. Units are a subset of cancellable elements
        self.assertTrue(units.issubset(cancellable))

    def test_commutative_ring_validation(self):
        # Z2 is commutative
        elements = {0, 1}
        add_op = lambda a, b: (a + b) % 2
        mul_op = lambda a, b: (a * b) % 2
        r = Ring(elements, add_op, mul_op)
        self.assertTrue(r.is_commutative())
        
        # Test that CommutativeRing accepts it
        CommutativeRing(elements, add_op, mul_op)

    def test_distributivity_violation(self):
        # A structure that is not a ring (e.g., changing multiplicative_semigroup to always return 1)
        elements = {0, 1}
        add_op = lambda a, b: (a + b) % 2
        mul_op = lambda a, b: 1
        # This will fail multiplication validation if we strictly use Semigroup for multiplicative_semigroup
        # because (0, 1) -> 1, (1, 1) -> 1, (0, 0) -> 1, (1, 0) -> 1 is associative.
        # But 1*(0+0) = 1*0 = 1 vs 1*0 + 1*0 = 1+1 = 0.
        with self.assertRaisesRegex(ValueError, "Distributivity violated"):
            Ring(elements, add_op, mul_op)

    def test_invariants_z4_group(self):
        # Z4 under addition
        elements = {0, 1, 2, 3}
        g = AbelianGroup(elements, lambda a, b: (a + b) % 4)
        
        # Generating set: {1} or {3} are minimal
        gen_set = g.find_generating_set()
        self.assertEqual(len(gen_set), 1)
        self.assertTrue(1 in gen_set or 3 in gen_set)
        
        # Idempotents: only 0 is idempotent (0+0=0)
        self.assertEqual(g.idempotents(), {0})
        
        # Center: entire group since it's Abelian
        self.assertEqual(g.center(), elements)
        
        # Orders: 0:1, 1:4, 2:2, 3:4
        orders = g.element_orders()
        self.assertEqual(orders[0], 1)
        self.assertEqual(orders[1], 4)
        self.assertEqual(orders[2], 2)
        self.assertEqual(orders[3], 4)

    def test_invariants_s2_monoid(self):
        # {0, 1} under multiplication (S2 monoid)
        elements = {0, 1}
        m = Monoid(elements, lambda a, b: (a * b) % 2)
        
        # Generating set: {0, 1} is needed? No, {0} generates {0}, {1} generates {1}.
        # Wait, closure of {0} is {0}, closure of {1} is {1}. 
        # To get {0, 1}, we need both.
        gen_set = m.find_generating_set()
        self.assertEqual(gen_set, {0, 1})
        
        # Idempotents: both 0 and 1 are idempotent
        self.assertEqual(m.idempotents(), {0, 1})
        
        # Orders: 1 is identity (order 1), 0 (0^n is never 1)
        orders = m.element_orders()
        self.assertEqual(orders[1], 1)
        self.assertIsNone(orders[0])

    def test_invalid_arity(self):
        # Magma requires a binary operation, but we provide a unary one
        elements = {0, 1}
        with self.assertRaisesRegex(TypeError, "must be binary"):
            Magma(elements, lambda x: x)

    def test_closure_violation(self):
        # Operation a + b on {0, 1} is not closed (1 + 1 = 2)
        elements = {0, 1}
        with self.assertRaisesRegex(ValueError, "not closed"):
            Magma(elements, lambda a, b: a + b)


if __name__ == '__main__':
    unittest.main()
