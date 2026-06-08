from src.domain.entities.algebras.group import Group
from src.domain.entities.algebras.ring import Ring
from src.application.use_cases.find_homomorphisms import FindHomomorphisms


def test_isomorphism_z3():
    """Test Z3 -> Z3 isomorphism."""
    elements = {0, 1, 2}
    add_op = lambda a, b: (a + b) % 3

    z3 = Group(elements, add_op)
    finder = FindHomomorphisms(strategy_name="brute_force")

    homs = finder.execute(z3, z3)

    # We expect 2 homomorphisms: the trivial one (all to 0) and the identity.
    # Actually, for Z3 as a group, there's also f(1)=2 which is an automorphism.
    # Let's check for the identity mapping specifically.
    identity_hom = next(h for h in homs if h.mapping == {0: 0, 1: 1, 2: 2})

    assert "Isomorphism" in identity_hom.properties
    assert "Automorphism" in identity_hom.properties
    assert "Endomorphism" in identity_hom.properties
    assert identity_hom.image == {0, 1, 2}
    assert identity_hom.kernel == {0}


def test_trivial_homomorphism_z3():
    """Test Z3 -> Z3 trivial homomorphism (zero mapping)."""
    elements = {0, 1, 2}
    add_op = lambda a, b: (a + b) % 3

    z3 = Group(elements, add_op)
    finder = FindHomomorphisms(strategy_name="brute_force")

    homs = finder.execute(z3, z3)
    trivial_hom = next(h for h in homs if h.mapping == {0: 0, 1: 0, 2: 0})

    assert "Monomorphism" not in trivial_hom.properties
    assert "Epimorphism" not in trivial_hom.properties
    assert "Endomorphism" in trivial_hom.properties
    assert trivial_hom.image == {0}
    assert trivial_hom.kernel == {0, 1, 2}


def test_non_injective_ring_homomorphism():
    """Test Z6 -> Z3 (mod 3) ring homomorphism."""
    z6_elements = set(range(6))
    z6_add = lambda a, b: (a + b) % 6
    z6_mul = lambda a, b: (a * b) % 6
    z6 = Ring(z6_elements, z6_add, z6_mul)

    z3_elements = set(range(3))
    z3_add = lambda a, b: (a + b) % 3
    z3_mul = lambda a, b: (a * b) % 3
    z3 = Ring(z3_elements, z3_add, z3_mul)

    finder = FindHomomorphisms(strategy_name="brute_force")
    homs = finder.execute(z6, z3)

    # f(x) = x % 3 is a valid ring homomorphism
    mod3_mapping = {i: i % 3 for i in range(6)}
    mod3_hom = next(h for h in homs if h.mapping == mod3_mapping)

    assert "Epimorphism" in mod3_hom.properties
    assert "Monomorphism" not in mod3_hom.properties
    assert mod3_hom.image == {0, 1, 2}
    assert mod3_hom.kernel == {0, 3}
