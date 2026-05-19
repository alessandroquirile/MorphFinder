from typing import Set, Any


def _get_closure(generators: Set[Any], constants: Set[Any], operations: Any) -> Set[Any]:
    """
    Computes the algebraic closure <G> of a set of generators G and constants.
    """
    closure = set(generators) | set(constants)
    new_elements = set(closure)

    while new_elements:
        next_generation = set()
        for op in operations:
            current_closure_list = list(closure)
            for x in new_elements:
                for y in current_closure_list:
                    results = {op(x, y), op(y, x)}
                    for res in results:
                        if res not in closure:
                            closure.add(res)
                            next_generation.add(res)

        new_elements = next_generation

    return closure
