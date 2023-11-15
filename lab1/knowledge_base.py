from definitions import *
from utils import *


class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def add(self, item):
        if isinstance(item, Fact):
            self.add_fact(item)
        elif isinstance(item, Rule):
            self.add_rule(item)

    def add_fact(self, fact):
        if fact not in self.facts:
            self.facts.append(fact)
            for rule in self.rules:
                self.derive(fact, rule)
        else:
            if fact.backed_by:
                ind = self.facts.index(fact)
                for f in fact.backed_by:
                    self.facts[ind].backed_by.append(f)
            else:
                ind = self.facts.index(fact)
                self.facts[ind].asserted = True

    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)
            for fact in self.facts:
                self.derive(fact, rule)
        else:
            if rule.backed_by:
                ind = self.rules.index(rule)
                for f in rule.backed_by:
                    self.rules[ind].backed_by.append(f)
            else:
                ind = self.rules.index(rule)
                self.rules[ind].asserted = True

    def query(self, fact):
        if isinstance(fact, Fact):
            f = Fact(fact.predicate)
            bindings_lst = []
            for fact in self.facts:
                binding = match(f.predicate, fact.predicate)
                if binding:
                    bindings_lst.append(binding)

            return bindings_lst

        else:
            print("Invalid question:", fact.predicate)
            return []

    def derive(self, fact, rule):
        bindings = match(rule.lhs[0], fact.predicate)
        if not bindings:
            return None

        if len(rule.lhs) == 1:
            new_fact = Fact(instantiate(rule.rhs, bindings), [[rule, fact]])
            rule.backs_facts.append(new_fact)
            fact.backs_facts.append(new_fact)
            self.add(new_fact)
        else:
            local_lhs = []
            local_rule = []
            for i in range(1, len(rule.lhs)):
                local_lhs.append(instantiate(rule.lhs[i], bindings))
            local_rule.append(local_lhs)
            local_rule.append(instantiate(rule.rhs, bindings))
            new_rule = Rule(local_rule, [[rule, fact]])
            rule.backs_rules.append(new_rule)
            fact.backs_rules.append(new_rule)
            self.add(new_rule)
