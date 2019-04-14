#!/usr/bin/python3
import argparse
import sys



def parse_file(f):
    grammar = {
        'N': [],
        'Sigma': [],
        'S': 'S',
        'P': [] 
    }
    for i in range(3):
        line = f.readline()
        line = line.rstrip()

        idx = line.find(' = ')
        s = line[:idx]
        elements = line[idx+3:].split(' ')
        grammar[s] = elements
        if s == 'S':
            grammar[s] = elements[0]
    for line in f:
        line = line.rstrip()

        idx = line.find(' -> ')
        left_hand_side = line[:idx]
        right_hand_side = line[idx+4:]
        grammar['P'].append((left_hand_side, right_hand_side))
    return grammar


# based on https://medium.com/100-days-of-algorithms/day-93-first-follow-cfe283998e3e
def compute_first_follow(grammar):
    first = {}
    follow = {}
    for terminal in grammar['Sigma']:
        first[terminal] = {terminal}
        follow[terminal] = set()

    for nonterminal in grammar['N']:
        first[nonterminal] = set()
        follow[nonterminal] = set()
        
    follow[grammar['S']].add('$')
    epsilon = set()
    for left, right in grammar['P']:
        if right == '$':
            epsilon.add(left)
    ok = True
    while ok == True:
        ok = False

        for left, right in grammar['P']:
            for symbol in right:
                ok |= union(first[left], first[symbol])
                if symbol not in epsilon:
                    break
                else:
                    ok |= union(epsilon, {left})

            new = follow[left]
            for symbol in reversed(right):
                ok |= union(follow[symbol], new)
                if symbol in epsilon:
                    new = new.union(first[symbol])
                else:
                    new = first[symbol]
    return first, follow, epsilon


def union(first, begins):
    n = len(first)
    first |= begins
    return len(first) != n


def make_csting(l):
   cstring = 'std::string(\"'
   for elem in l:
       cstring += elem
   cstring += '\")'
   return cstring
   

def main():
    parser = argparse.ArgumentParser(description='Tool for generating a recursive descent parser.')
    parser.add_argument('input', type=str, help='Path to input file (where the grammar in described)')
    parser.add_argument('output', type=str, help='Output file name.')

    args = parser.parse_args()
    inputFile = args.input
    outputFile = args.output

    f = open(inputFile, 'r')
    grammar = parse_file(f)
    f.close()
    first, follow, epsilon = compute_first_follow(grammar)
    print(first)
    print(follow)
    print(epsilon)

    o = open(outputFile, 'w')
    # include libraries
    o.write('#include <iostream>\n')
    o.write('#include <string>\n')
    o.write('\n')

    # global variables
    o.write('std::string s;\n')
    o.write('int i = -1;\n')
    o.write('char token;\n')
    o.write('\n')

    for nonterminal in grammar['N']:
        o.write('void ' + nonterminal + '();\n')
    o.write('void check(std::string alpha);\n')
    o.write('void parse_nonterminal(std::string alpha);\n')
    o.write('\n')

    # first functions
    o.write('std::string first(char c) {\n')
    o.write('  switch(c) {\n')
    for terminal in grammar['Sigma']:
        o.write('    case \'' + terminal + '\': return ' + make_csting(first[terminal]) + '; break;\n')
    for nonterminal in grammar['N']:
        o.write('    case \'' + nonterminal + '\': return ' + make_csting(first[nonterminal]) + '; break;\n')
    o.write('  }\n')
    o.write('}\n')
    o.write('\n')

    # follow functions
    o.write('std::string follow(char c) {\n')
    o.write('  switch(c) {\n')
    for terminal in grammar['Sigma']:
        o.write('    case \'' + terminal + '\': return ' + make_csting(follow[terminal]) + '; break;\n')
    for nonterminal in grammar['N']:
        o.write('    case \'' + nonterminal + '\': return ' + make_csting(follow[nonterminal]) + '; break;\n')
    o.write('  }\n')
    o.write('}\n')
    o.write('\n')

    # scan function which returns next token
    o.write('char scan() {\n')
    o.write('  ++i;\n')
    o.write('  if (i < s.size()) {\n')
    o.write('    return s[i];\n')
    o.write('  }\n')
    o.write('  return EOF;\n')
    o.write('}\n')
    o.write('\n')

    # check function
    o.write('void check_terminal(std::string alpha) {\n')
    o.write('  if (alpha[0] == token) {\n')
    o.write('    token = scan();\n')
    o.write('  }\n')
    o.write('  else {\n')
    o.write('    std::cout << alpha[0] + \" expected\\n\";\n')
    o.write('  }\n')
    o.write('  if (alpha.size() >= 2) {\n')
    o.write('    check(alpha.substr(1));\n')
    o.write('  }\n')
    o.write('}\n')
    o.write('\n')

    o.write('void check_nonterminal(std::string alpha) {\n')
    o.write('  parse_nonterminal(alpha);\n')
    o.write('}\n')
    o.write('\n')

    o.write('void check(std::string alpha) {\n')
    o.write('  switch(alpha[0]) {\n')
    for terminal in grammar['Sigma']:
        o.write('    case \'' + terminal + '\': check_terminal(alpha); break;\n')
    for nonterminal in grammar['N']:
        o.write('    case \'' + nonterminal + '\': check_nonterminal(alpha); break;\n')
    o.write('  }\n')
    o.write('}\n')
    o.write('\n')

    # parse function for terminals and nonterminals
    o.write('void parse_terminal(std::string alpha) {\n')
    o.write('  if (alpha[0] != \'l\') {\n')
    o.write('    token = scan();\n')
    o.write('  }\n')
    o.write('  if (alpha.size() >= 2) {\n')
    o.write('    check(alpha.substr(1));\n')
    o.write('  }\n')
    o.write('}\n')
    o.write('\n')
    o.write('void parse_nonterminal(std::string alpha) {\n')
    o.write('  switch(alpha[0]) {\n')
    for nonterminal in grammar['N']:
        o.write('    case \'' + nonterminal + '\':' + nonterminal + '(); break;\n')
    o.write('  }\n')
    o.write('  if (alpha.size() >= 2) {\n')
    o.write('    check(alpha.substr(1));\n')
    o.write('  }\n')
    o.write('}\n')
    o.write('\n')

    # function for every nonterminal A from N
    for nonterminal in grammar['N']:
        o.write('void ' + nonterminal + '() {\n')
        for left, right in grammar['P']:
            if left == nonterminal:
                if right[0] != 'l':
                    o.write('  if (first(\'' + right[0] + '\').find(token) != std::string::npos) {\n')
                    o.write('    std::cout << \"' + nonterminal + ' -> ' + right + '\\n\";\n')
                    if right[0] in grammar['N']:
                        o.write('    parse_nonterminal(\"' + right + '\");\n')
                    else:
                        o.write('    parse_terminal(\"' + right + '\");\n')
                    o.write('    return;\n')
                    o.write('  }\n')
                else:
                    o.write('  if (follow(\'' + left + '\').find(token) != std::string::npos) {\n')
                    o.write('    std::cout << \"' + nonterminal + ' -> ' + right + '\\n\";\n')
                    if right[0] in grammar['N']:
                        o.write('    parse_nonterminal(\"' + right + '\");\n')
                    else:
                        o.write('    parse_terminal(\"' + right + '\");\n')
                    o.write('    return;\n')
                    o.write('  }\n')

        o.write('  std::cout << \"Se asteapta un token diferit\\n\";\n')
        o.write('}\n')
        o.write('\n')

    o.write('int main() {\n')
    o.write('  std::cin >> s;\n')
    o.write('  token = scan();\n')
    o.write('  ' + grammar['S'] + '();\n')
    o.write('  if (token != EOF) {\n')
    o.write("      std::cout << \"ERROR: EOF expectd\\n\";\n")
    o.write('  }\n')
    o.write('  return 0;\n')
    o.write('}\n')

if __name__ == '__main__':
    sys.exit(main());
