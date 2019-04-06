#!/usr/bin/python3
import argparse
import sys



def parse_file(f):
    grammar = {
        'N': [],
        'Sigma': [],
        'S': 'S',
        'P': {} 
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
        if left_hand_side in grammar['P']:
            grammar['P'][left_hand_side].append(right_hand_side)
        else:
            grammar['P'][left_hand_side] = [right_hand_side]
    return grammar
    

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
    print(grammar)


if __name__ == '__main__':
    sys.exit(main());
