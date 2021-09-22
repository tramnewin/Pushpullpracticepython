"""
Name: Tram Nguyen
CSCI 3415 001
Assignment 1: Python
The program read in a grammar from an input file. T
he grammar file contains the rules in Backus-Naur form
Each line from the file contains zero or more rules.
If the line has zero rule, it is considered as a blank line
and is ignored. All elements of the rule are separated by whitespaces to parse easily.
Once the program finishes reading the rules of the grammar,
the program prints out the parsed grammar and then
read in the user’s sentence and print out the leftmost derivation (if existed) on the terminal.
"""
import os
import re
import sys


def isnonterminal(nonterm):
    """return boolean datatype"""
    return isinstance(nonterm, str) and re.match(r'^<.*>$', nonterm) is not None


def isterminal(term):
    """return boolean datatype"""
    return isinstance(term, str) and not isnonterminal(term)


def read_grammar(filepath):
    """reads in the input text file, parse the input into rules
    and stores list of rules in grammar"""
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

    with open(filepath, 'r', encoding='utf-8') as file_path:
        for line in file_path:
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
    """print out the grammar rules generated from reading the input file"""
    for rule in grammar:
        print(f'{rule[0]} -> {" ".join(rule[1])}')


def applicable_rules(grammar, nonterminal):
    """returns a list of grammar rules for nonterminal"""
    return list(filter(lambda rule: rule[0] == nonterminal, grammar))


def match_form(form, sentence):
    """return the length of prefix to track how many terminals has been discovered"""
    for i, lex in enumerate(form):
        if i == len(sentence):
            return -1
        if isnonterminal(lex):
            return i
        if lex != sentence[i]:
            return -1
    return len(sentence) if len(sentence) == len(form) else -1


def subst(rule, form, match):
    """return a new form that has the matching form
    with the list of already found sentential form"""
    return form[:match] + rule[1] + form[match + 1:]


def leftmost_derivation(grammar, sentence, form):  # my last parameter is incorrect (might be depth
    """find the derivation of the sentence by using this recursive function.
    The function first find the prefix of the form.
    if the functions matches the whole length of the sentence,
    the derivation is finished and return the list of forms
    if the prefix is -1, none is returned indicating no prefix found.
    the it goes through a loop going over the list of rules in
    the grammar. the new form is created by calling subst.
    if the length of this form is less than or equal to
    the length of the sentence, this functions is recursively called
    and store the return result in derivation. If derivation is not
    empty, we append it into the new created form"""
    match = match_form(form, sentence)
    if match == -1:
        return None
    if match == len(sentence):
        return []
    for rule in applicable_rules(grammar, form[match]):
        new_form = subst(rule, form, match)
        if len(new_form) <= len(sentence):
            derivation = leftmost_derivation(grammar, sentence, new_form)
            if derivation is not None:
                return [new_form] + derivation
    return None


def print_derivation(grammar, derivation):
    """ Prints the derivation for a given grammar in a readable format. """
    start = grammar[0][0]
    blank = ' ' * len(start)
    if derivation is None:
        print('No derivation found')
    else:
        for i, form in enumerate(derivation, 1):
            print(f'{i:4d}: {start if i == 1 else blank} -> {" ".join(form)}')


def main():
    """main program that would calls the above functions in order to
     reads the grammar file, parse it into list of grammar rules,
     reads in the user's sentence, split it into a list, then
     calls the leftmost_derivation function to find setential forms
     and print out the result onto the terminal"""
    # filepath = sys.argv[1]
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
        # print(sentence)  # added on to check for correct input
        start = grammar[0][1]

        derivation = leftmost_derivation(grammar, sentence, start)
        print(derivation)
        print(' '.join(sentence))
        print('Derivation:')
        print_derivation(grammar, derivation)


if __name__ == '__main__':
    A_Form = []
    main()
