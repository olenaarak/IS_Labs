class Fact:
    def __init__(self, predicate, backed_by=None):
        super(Fact, self).__init__()
        if backed_by is None:
            backed_by = []
        self.predicate = predicate if isinstance(predicate, Predicate) else Predicate(predicate)
        self.asserted = not backed_by
        self.backed_by = []
        self.backs_facts = []
        self.backs_rules = []
        for pair in backed_by:
            self.backed_by.append(pair)

    def __eq__(self, other):
        return isinstance(other, Fact) and self.predicate == other.predicate


class Rule:
    def __init__(self, rule, backed_by=None):
        super(Rule, self).__init__()
        if backed_by is None:
            backed_by = []
        self.lhs = [p if isinstance(p, Predicate) else Predicate(p) for p in rule[0]]
        self.rhs = rule[1] if isinstance(rule[1], Predicate) else Predicate(rule[1])
        self.asserted = not backed_by
        self.backed_by = []
        self.backs_facts = []
        self.backs_rules = []
        for pair in backed_by:
            self.backed_by.append(pair)


class Predicate:
    def __init__(self, predicates_list=None):
        if predicates_list is None:
            predicates_list = []
        self.terms = []
        self.predicate = ""

        if predicates_list:
            self.predicate = predicates_list[0]
            self.terms = [t if isinstance(t, Term) else Term(t) for t in predicates_list[1:]]

    def __eq__(self, other):
        if self.predicate != other.predicate:
            return False

        for self_term, other_term in zip(self.terms, other.terms):
            if self_term != other_term:
                return False

        return True


class Term:
    def __init__(self, term):
        super(Term, self).__init__()
        is_var_or_value = isinstance(term, Variable) or isinstance(term, Value)
        self.term = term if is_var_or_value else (Variable(term) if Variable.is_variable(term) else Value(term))

    def __eq__(self, other):
        return (self is other
                or isinstance(other, Term) and self.term.element == other.term.element
                or ((isinstance(other, Variable) or isinstance(other, Value))
                    and self.term.element == other.element))


class Variable:
    def __init__(self, element):
        self.term = None
        self.element = element

    def __eq__(self, other):
        return (self is other
                or isinstance(other, Term) and self.term.element == other.term.element
                or ((isinstance(other, Variable) or isinstance(other, Value))
                    and self.term.element == other.element))

    @staticmethod
    def is_variable(var):
        if type(var) == str:
            return var[0] == '?'
        if isinstance(var, Term):
            return isinstance(var.term, Variable)

        return isinstance(var, Variable)


class Value:
    def __init__(self, element):
        self.term = None
        self.element = element

    def __eq__(self, other):
        return (self is other
                or isinstance(other, Term) and self.term.element == other.term.element
                or ((isinstance(other, Variable) or isinstance(other, Value))
                    and self.term.element == other.element))


class Assignment:
    def __init__(self, variable, value):
        super(Assignment, self).__init__()
        self.variable = variable
        self.value = value

    def __str__(self):
        return self.variable.element + " : " + self.value.element


class Assignments:
    def __init__(self):
        self.assignments = []
        self.mapping = {}

    def __str__(self):
        if not self.assignments:
            return ''
        return ", ".join((str(binding) for binding in self.assignments))

    def __getitem__(self, key):
        return self.mapping[key] if (self.mapping and key in self.mapping) else None

    def assign(self, variable, value):
        self.mapping[variable.element] = value.element
        self.assignments.append(Assignment(variable, value))

    def is_assigned_to(self, variable):
        if variable.element in self.mapping.keys():
            value = self.mapping[variable.element]
            if value:
                return Variable(value) if Variable.is_variable(value) else Value(value)
        return False

    def test_and_bind(self, variable_term, value_term):
        bound = self.is_assigned_to(variable_term.term)
        if bound:
            return value_term.term == bound

        self.assign(variable_term.term, value_term.term)
        return True
