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


if __name__ == '__main__':
    sys.exit(main());
