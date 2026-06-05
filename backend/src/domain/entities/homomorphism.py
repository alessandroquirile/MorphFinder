from typing import Dict, Any, List, Set

class Homomorphism:
    """
    Domain Entity/Value Object: Represents a validated homomorphism between two algebraic structures.
    This is a pure data carrier, agnostic of the services that classify or analyze it.
    """

    def __init__(
        self, 
        mapping: Dict[Any, Any], 
        source: Any, 
        target: Any,
        properties: List[str] = None,
        image: Set[Any] = None,
        kernel: Set[Any] = None
    ):
        self.mapping = mapping
        self.source = source
        self.target = target
        self.properties = properties or []
        self.image = image or set()
        self.kernel = kernel or set()

    def __repr__(self):
        props_str = f" | {', '.join(self.properties)}" if self.properties else ""
        return f"Homomorphism({self.mapping}{props_str})"

    def pretty(self) -> str:
        """Returns a detailed formatted algebraic representation of the homomorphism."""
        source_elements = "{" + ", ".join(map(str, sorted(list(self.source.elements)))) + "}"
        target_elements = "{" + ", ".join(map(str, sorted(list(self.target.elements)))) + "}"

        mapping_str = ", ".join([f"{src} ↦ {tgt}" for src, tgt in self.mapping.items()])
        props_str = f" | Properties: {', '.join(self.properties)}" if self.properties else ""

        image_str = f" | Im(f): {{{', '.join(map(str, sorted(list(self.image))))}}}"
        kernel_str = f" | Ker(f): {{{', '.join(map(str, sorted(list(self.kernel))))}}}"

        return f"f: {source_elements} → {target_elements} | {mapping_str}{props_str}{kernel_str}{image_str}"
