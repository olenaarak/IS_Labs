import definitions as defs


def match(state1, state2, bindings=None):
    if len(state1.terms) != len(state2.terms) or state1.predicate != state2.predicate:
        return False
    if not bindings:
        bindings = defs.Assignments()
    return match_recursive(state1.terms, state2.terms, bindings)


def match_recursive(terms1, terms2, bindings):
    if len(terms1) == 0:
        return bindings
    if defs.Variable.is_variable(terms1[0]):
        if not bindings.test_and_bind(terms1[0], terms2[0]):
            return False
    elif defs.Variable.is_variable(terms2[0]):
        if not bindings.test_and_bind(terms2[0], terms1[0]):
            return False
    elif terms1[0] != terms2[0]:
        return False
    return match_recursive(terms1[1:], terms2[1:], bindings)


def instantiate(statement, bindings):
    def handle_term(term):
        if defs.Variable.is_variable(term):
            bound_value = bindings.is_assigned_to(term.term)
            return defs.Term(bound_value) if bound_value else term
        else:
            return term

    new_terms = [handle_term(t) for t in statement.terms]
    return defs.Predicate([statement.predicate] + new_terms)
