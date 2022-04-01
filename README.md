# Pushpullpracticepython
a Python program that reads in a grammar from an input file and then uses that grammar to print leftmost derivations (if they exist) 
of sentences read from standard input. 
The grammar file contains the rules for the grammar in Backus-Naur Form (sometimes written as Backus 
Normal Form), or BNF. Each line of the file contains zero or more rules. Blank lines, which contain zero 
rules, are ignored. All the elements of the rule(s) are separated by whitespace to make parsing easy. 

The left-hand side of the rule must be a single nonterminal,the symbol -> separates the left-hand and right-hand sides of the rule, 
and the right-hand side is a nonempty sequence of terminals and nonterminals. The symbol | separates alternative rules. 
There is a shortcut notation that allows alternatives to be written on separate lines where subsequent 
lines after the first begin with the symbol |. In this case, the left-hand side is the same as the previous 
line(s). 
