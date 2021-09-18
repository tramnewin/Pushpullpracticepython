import os
import re
import sys


def isnonterminal(x):
    return isinstance(x, str) and re.match(r'^<.*>$', x) is not None


def isterminal(x):
    return isinstance(x, str) and not isnonterminal(x)


def read_grammar(filepath):
    grammar = []
    current_lhs = None

    def make_rule(lhs, rhs):
        if not isnonterminal(lhs):
            raise Exception(f'LHS {lhs} is not a nonterminal')
        if not rhs:
            raise Exception('Empty RHS')
        return (lhs, rhs)

    def parse_rhs(lexemes):
        rules = []
        rhs = []
        for lex in lexemes:
            if lex == '|':
                rules.append(make_rule(current_lhs, rhs))
                rhs = []
            else:
                rhs.append(lex)
        rules.append(make_rule(current_lhs, rhs))
        return rules

    with open(filepath) as fp:
        for line in fp:
            lexemes = line.split()
            if not lexemes:
                pass
            elif len(lexemes) == 1:
                raise Exception(f'Illegal rule {line}')
            elif isnonterminal(lexemes[0]) and lexemes[1] == '->':
                current_lhs = lexemes[0]
                grammar.extend(parse_rhs(lexemes[2:]))
            elif lexemes[0] == '|':
                grammar.extend(parse_rhs(lexemes[1:]))
            else:
                raise Exception(f'Illegal rule {line}')

    return grammar


def print_grammar(grammar):
    for rule in grammar:
        print(f'{rule[0]} -> {" ".join(rule[1])}')


def applicable_rules(grammar, nonterminal): #returns a list of grammar rules for nonterminal
    return list(filter(lambda rule: rule[0] == nonterminal, grammar))


def match_form(form, sentence):  # return int of the length of prefix ['begin', 'A', '='] =len(3)
    for i, lex in enumerate(form):  # i is index and lex is the value within the element of that index, enumerate makes that happen
        if i == len(sentence):
            return -1
        if isnonterminal(lex):
            return i
        if lex != sentence[i]:
            return -1
    return len(sentence) if len(sentence) == len(form) else -1


def subst(rule, form, match):
    return form[:match] + rule[1] + form[match + 1:]

A_fo=[]
def leftmost_derivation(grammar, sentence, form, finalform=[]):  # my last parameter is incorrect (might be depth
    # code here
    match = match_form(form, sentence)
    if match == -1:
        return None
    if match == len(sentence):
        return finalform
    for rule in applicable_rules(grammar, form[match]):
        if rule not in form and rule[1][0] not in form:
            form += subst(rule, form, match)
            finalform += form
            if len(finalform) > 3:
                if finalform[max(index for index, item in enumerate(finalform) if item == 'begin'):] == sentence and finalform[max(index for index, item in enumerate(finalform) if item == 'begin'):] != finalform[:3]:

                    print(match, "  ", len(finalform), "   ", finalform)
                    return finalform
            leftmost_derivation(grammar, sentence, form[max(index for index, item in enumerate(form) if item == 'begin'):])
    return None




def print_derivation(derivation):
    for things in derivation:
        print(f'{things[0]} -> {" ".join(things[1])}')


def main():
    #filepath = sys.argv[1]
    filepath = input("Name of the file: ")
    if not os.path.isfile(filepath):
        raise Exception(f'File path {filepath} does not exist.')

    print(f'Reading grammar from {filepath}')
    grammar = read_grammar(filepath)
    print(grammar)
    print_grammar(grammar)
    # Read sentences from standard input until end of file and print
    # their leftmost derivations.
    while True:
        print('---')
        try:
            sentence_string = input('Enter a sentence:\n')
        except EOFError:
            sys.exit()
        sentence = sentence_string.split()
        print(sentence)
        #print(sentence)  # added on to check for correct input
        start = grammar[0][1]

        derivation = leftmost_derivation(grammar, sentence, start)
        print(derivation)
        print(' '.join(sentence))
        print('Derivation:')
        print_derivation(derivation)
        print('\nDone')


if __name__ == '__main__':
    A_Form = []
    main()
