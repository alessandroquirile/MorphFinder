import unittest

from src.algebraic_structures import AlgebraicStructure, Magma, Semigroup, Monoid, Group, AbelianGroup, classify


class TestMagmaHierarchy(unittest.TestCase):
    def test_z2_group_callable(self):
        # Z2 under addition is an Abelian Group
        elements = {0, 1}
        # Model: (S, op1)
        m = classify(elements, lambda a, b: (a + b) % 2)
        self.assertIsInstance(m, AbelianGroup)
        self.assertEqual(m.identity, 0)
        self.assertEqual(m.inverse(1), 1)
        # Verify operation access via op()
        self.assertEqual(m.op(1, 1), 0)

    def test_z3_group_callable(self):
        # Z3 under addition using a callable
        elements = {0, 1, 2}
        m = classify(elements, lambda a, b: (a + b) % 3)
        self.assertIsInstance(m, AbelianGroup)
        self.assertEqual(m.identity, 0)
        self.assertEqual(m.op(1, 2), 0)

    def test_n_mul_finite_callable(self):
        # {0, 1, 2} mod 3 under multiplication is a Commutative Monoid
        elements = {0, 1, 2}
        m = classify(elements, lambda a, b: (a * b) % 3)
        self.assertIsInstance(m, Monoid)
        self.assertNotIsInstance(m, Group)
        self.assertEqual(m.identity, 1)

    def test_z_minus_not_semigroup_callable(self):
        # Subtraction mod 3 is not associative
        elements = {0, 1, 2}
        m = classify(elements, lambda a, b: (a - b) % 3)
        self.assertIsInstance(m, Magma)
        self.assertNotIsInstance(m, Semigroup)

    def test_powerset_union_callable(self):
        # P({1}) under union: { {}, {1} } (Commutative Monoid)
        elements = [frozenset(), frozenset({1})]
        m = classify(elements, lambda a, b: a | b)
        self.assertIsInstance(m, Monoid)
        self.assertNotIsInstance(m, Group)

    def test_closure_violation_callable(self):
        # Operation a + b on {0, 1} is not closed (1 + 1 = 2 not in {0, 1})
        elements = {0, 1}
        with self.assertRaisesRegex(ValueError, "not closed"):
            classify(elements, lambda a, b: a + b)

    def test_multi_op_structure(self):
        # Model: (S, op1, op2) where op1 is binary, op2 is unary
        S = {0, 1, 2}
        op1 = lambda a, b: (a + b) % 3
        op2 = lambda n: n ** 2 % 3

        struct = AlgebraicStructure(S, op1, op2)

        self.assertEqual(len(struct.operations), 2)
        self.assertEqual(struct.operations[0], op1)
        self.assertEqual(struct.operations[1], op2)

        # Verify internal tables
        self.assertEqual(len(struct._cayley_tables), 2)
        self.assertIsNotNone(struct._cayley_tables[0])
        self.assertIsNone(struct._cayley_tables[1])  # Unary ops have no Cayley table

    def test_magma_invalid_arity(self):
        # Magma requires arity 2, but lambda n: n**2 has arity 1
        elements = {0, 1, 2}
        with self.assertRaisesRegex(TypeError, "requires a binary operation"):
            Magma(elements, lambda n: n ** 2 % 3)


if __name__ == '__main__':
    unittest.main()
