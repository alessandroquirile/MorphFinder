from collections import defaultdict
from typing import Any, Dict, Set, List

from src.algebras.structures.group import Group
from src.algebras.structures.monoid import Monoid
from src.algebras.structures.ring import Ring


class Classifier:
    """
    Classifies homomorphisms based on categorical properties.
    Implements First Isomorphism Theorem logic and congruence analysis.
    """

    @staticmethod
    def get_image(mapping: Dict[Any, Any]) -> Set[Any]:
        """Returns the set of elements in the image of the homomorphism."""
        return set(mapping.values())

    @staticmethod
    def get_kernel(mapping: Dict[Any, Any], target: Any) -> Set[Any]:
        """
        Identifies the kernel for Groups and Rings.
        Returns elements of the source that map to the identity/zero of the target.
        
        Note: Based on the First Isomorphism Theorem, the kernel characterizes 
        the quotient structure S/Ker(f) which is isomorphic to the image.
        """
        zero_element = None

        # Determine the "zero" element of the target structure
        if isinstance(target, Ring):
            zero_element = target.zero
        elif isinstance(target, (Group, Monoid)):
            zero_element = target.identity

        if zero_element is not None:
            return {src for src, tgt in mapping.items() if tgt == zero_element}

        return set()

    @staticmethod
    def get_congruence_classes(mapping: Dict[Any, Any]) -> List[Set[Any]]:
        """
        Computes equivalence classes for general structures.
        a ~ b iff f(a) = f(b).
        """
        classes = defaultdict(set)
        for src, tgt in mapping.items():
            classes[tgt].add(src)
        return list(classes.values())

    @staticmethod
    def classify(homomorphism: Any) -> List[str]:
        """
        Returns a list of categorical labels for the given homomorphism.
        
        Categories:
        - Monomorphism (f: S ↪ T): An injective homomorphism.
        - Epimorphism (f: S ↠ T): A surjective homomorphism.
        - Isomorphism (f: S ≅ T): A bijective homomorphism.
        - Endomorphism (f: S → S): A homomorphism where the source and target are the same.
        - Automorphism (f: S ≅ S): A bijective endomorphism.
        """
        mapping = homomorphism.mapping
        source = homomorphism.source
        target = homomorphism.target

        image = Classifier.get_image(mapping)

        # Check if trivial (image is just the zero/identity element of the target)
        is_trivial = False
        if isinstance(target, (Ring, Group, Monoid)):
            zero_or_identity = getattr(target, 'zero', None) or getattr(target, 'identity', None)
            if zero_or_identity is not None and image == {zero_or_identity}:
                is_trivial = True

        # Computational shortcut: According to the First Isomorphism Theorem
        # (and its generalization for general structures via congruence classes),
        # f is injective iff |S| = |Im(f)|.
        is_injective = len(mapping) == len(image)
        is_surjective = len(image) == len(target.elements)
        is_endomorphism = source == target

        labels = []

        if is_trivial:
            labels.append("Trivial")
        if is_injective:
            labels.append("Monomorphism")
        if is_surjective:
            labels.append("Epimorphism")
        if is_injective and is_surjective:
            labels.append("Isomorphism")

        if is_endomorphism:
            labels.append("Endomorphism")
            if is_injective and is_surjective:
                labels.append("Automorphism")

        return labels
