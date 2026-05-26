from typing import Any, Callable


class Pruner:
    """
    Handles heuristic-based pruning to reduce the search space for homomorphisms.
    Decoupled from algebraic structures to keep them focused on math.
    """

    @staticmethod
    def is_assignment_possible(source_val: Any, target_val: Any, source, target) -> bool:
        """
        Heuristic check if assigning source_val -> target_val is possible.
        
        Pruning Strategies (Constraint Satisfaction):
        Homomorphisms must preserve algebraic invariants. If f(g) = t violates
        an invariant (like order or idempotency), the assignment is pruned
        early to avoid exploring invalid branches of the backtracking tree.
        """
        # 1. Idempotency (Universal check)
        if not Pruner._check_idempotency(source_val, target_val, source, target):
            return False

        # 2. Group Order Pruning (Specific to groups or structures with identity/op)
        if (hasattr(source, "identity") and hasattr(source, "operation") and
            hasattr(target, "identity") and hasattr(target, "operation")):
            if not Pruner._check_group_order(source_val, target_val, source, target):
                return False

        return True

    @staticmethod
    def _check_idempotency(source_val, target_val, source, target) -> bool:
        num_ops = min(len(source.operations), len(target.operations))
        for op_idx in range(num_ops):
            source_op = source.operations[op_idx]
            target_op = target.operations[op_idx]
            if source_op(source_val, source_val) == source_val:
                if target_op(target_val, target_val) != target_val:
                    return False
        return True

    @staticmethod
    def _check_group_order(source_val, target_val, source, target) -> bool:
        """
        In group homomorphisms, the order of the image f(g) must divide 
        the order of the element g. This is a powerful invariant for pruning.
        """
        source_order = Pruner._get_order(source_val, source.identity, source.operation)
        try:
            target_order = Pruner._get_order(target_val, target.identity, target.operation)
            if source_order % target_order != 0:
                return False
        except Exception:
            # Fallback if target doesn't behave like a finite group
            pass
        return True

    @staticmethod
    def _get_order(element: Any, identity: Any, operation: Callable) -> int:
        if element == identity:
            return 1
        order = 1
        current = element
        # Safety limit for finite structures
        max_limit = 1000 
        while current != identity and order < max_limit:
            current = operation(current, element)
            order += 1
        return order
