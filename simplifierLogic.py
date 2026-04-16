from nodes import Var, Const, Not, And, Or

def collect_or_terms(node):
    if isinstance(node, Or):
        return collect_or_terms(node.left) + collect_or_terms(node.right)
    return [node]

def collect_and_terms(node):
    if isinstance(node, And):
        return collect_and_terms(node.left) + collect_and_terms(node.right)
    return [node]

def build_or_tree(terms):
    result = terms[0]
    for t in terms[1:]:
        result = Or(result, t)
    return result

def build_and_tree(terms):
    result = terms[0]
    for t in terms[1:]:
        result = And(result, t)
    return result

def is_negation(a, b):
    return (isinstance(a, Not) and a.child == b) or \
           (isinstance(b, Not) and b.child == a)

# -------------------
# RULES
# -------------------

def rule_double_negation(node):
    if isinstance(node, Not) and isinstance(node.child, Not):
        return node.child.child
    return node

def rule_de_morgan(node):
    if isinstance(node, Not) and isinstance(node.child, And):
        return Or(Not(node.child.left), Not(node.child.right))

    if isinstance(node, Not) and isinstance(node.child, Or):
        return And(Not(node.child.left), Not(node.child.right))

    return node

def rule_idempotent(node):
    if isinstance(node, Or):
        terms = collect_or_terms(node)
        unique = []
        for t in terms:
            if t not in unique:
                unique.append(t)

        if len(unique) == 1:
            return unique[0]

        new_node = build_or_tree(unique)
        if new_node != node:
            return new_node

    if isinstance(node, And):
        terms = collect_and_terms(node)
        unique = []
        for t in terms:
            if t not in unique:
                unique.append(t)

        if len(unique) == 1:
            return unique[0]

        new_node = build_and_tree(unique)
        if new_node != node:
            return new_node

    return node

def rule_complement(node):
    if isinstance(node, Or):
        terms = collect_or_terms(node)
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                if is_negation(terms[i], terms[j]):
                    return Const(1)

    if isinstance(node, And):
        terms = collect_and_terms(node)
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                if is_negation(terms[i], terms[j]):
                    return Const(0)

    return node

def rule_identity_domination(node):
    if isinstance(node, Or):
        terms = collect_or_terms(node)

        if any(isinstance(t, Const) and t.value == 1 for t in terms):
            return Const(1)

        terms = [t for t in terms if not (isinstance(t, Const) and t.value == 0)]

        if len(terms) == 0:
            return Const(0)
        if len(terms) == 1:
            return terms[0]

        new_node = build_or_tree(terms)
        if new_node != node:
            return new_node

    if isinstance(node, And):
        terms = collect_and_terms(node)

        if any(isinstance(t, Const) and t.value == 0 for t in terms):
            return Const(0)

        terms = [t for t in terms if not (isinstance(t, Const) and t.value == 1)]

        if len(terms) == 0:
            return Const(1)
        if len(terms) == 1:
            return terms[0]

        new_node = build_and_tree(terms)
        if new_node != node:
            return new_node

    return node

# -------------------
# SIMPLIFIER
# -------------------

def simplify_once(node):
    if isinstance(node, (Var, Const)):
        current = node

    elif isinstance(node, Not):
        current = Not(simplify_once(node.child))

    elif isinstance(node, And):
        current = And(simplify_once(node.left), simplify_once(node.right))

    elif isinstance(node, Or):
        current = Or(simplify_once(node.left), simplify_once(node.right))

    else:
        raise ValueError("Unknown node")

    for rule in [
        rule_double_negation,
        rule_de_morgan,
        rule_idempotent,
        rule_complement,
        rule_identity_domination
    ]:
        new_node = rule(current)
        if new_node != current:
            return new_node

    return current

def simplify_full(node):
    while True:
        new_node = simplify_once(node)
        if new_node == node:
            return node
        node = new_node

# -------------------
# AST BACK TO STRING
# -------------------

def to_string(node):
    if isinstance(node, Var):
        return node.name

    if isinstance(node, Const):
        return str(node.value)

    if isinstance(node, Not):
        child = node.child
        s = to_string(child)
        if isinstance(child, (And, Or)):
            return f"!({s})"
        return f"!{s}"

    if isinstance(node, And):
        l = to_string(node.left)
        r = to_string(node.right)

        if isinstance(node.left, Or):
            l = f"({l})"
        if isinstance(node.right, Or):
            r = f"({r})"

        return f"{l}*{r}"

    if isinstance(node, Or):
        return f"{to_string(node.left)}+{to_string(node.right)}"
