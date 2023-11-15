from definitions import *


def parse_input():
    facts, rules = parse_facts(), parse_rules()
    output = []
    for f in facts:
        output.append(f)
    for r in rules:
        output.append(r)
    return output


def parse_facts():
    with open('data/facts.txt', 'r') as file:
        return [parse_fact(line) for line in file]


def parse_fact(fact):
    return Fact(fact.rstrip().strip().split())


def parse_rules():
    with open('data/rules.txt', 'r') as file:
        lines = [line.rstrip() for line in file]
        rules = []
        for line in lines:
            r = line.split('->')
            rhs = r[1].rstrip().strip().split()
            lhs = r[0].split('&')
            lhs = map(lambda x: x.rstrip().strip().split(), lhs)
            rules.append(Rule([lhs, rhs]))
        return rules
