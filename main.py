"""Word-Ladder Solver.

blah blah blah
and blah
"""


import sys
import enum
import argparse
import itertools
from collections import deque


class Mode(enum.Enum):
    SWAP = 'swap-only'
    ADD_REM_SWAP = 'add-remove-swap'


class Node:
    """Node of a Tree"""
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent

    def __iter__(self):
        if self.parent is not None:
            yield from self.parent
        yield self.value

    def __reversed__(self):
        node = self
        while node is not None:
            yield node.value
            node = node.parent


def command_line_parser():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('word', nargs='+')
    parser.add_argument('final_word')
    parser.add_argument(
            '-m', '--mode', type=Mode,
            choices=[m.value for m in Mode], default=Mode.SWAP,
            help='mode of operation to use')
    parser.add_argument(
            '-d', '--dictionnary', '--words-file',
            metavar='PATH', default='/usr/share/dict/words',
            help='path to the list of words to search from')
    return parser

def take_inputs():
  modes = [Mode.SWAP, Mode.ADD_REM_SWAP]
  words = input("Enter list of words, seperated by spaces: ").split()
  mode = input("Enter 1 for swap-only mode, or 2 for swap-add-rem mode: ")
  while not(mode.isdigit()) or not(1 <= int(mode) <= 2):
    print("invalid input")
    mode = input("Enter 1 for swap-only mode, or 2 for swap-add-rem mode: ")
  return words, modes[int(mode)-1]

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    yield from zip(a, b)


def hamming(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def read_words(filename):
    with open(filename) as f:
        return set(map(str.lower, filter(str.isalpha, map(str.strip, f))))


def find_word_ladder(source, target, words, distance):
    checked = set()
    candidates = deque([Node(source)])

    while candidates:
        node = candidates.popleft()
        candidate = node.value
        if candidate == target:
            return node

        if candidate not in checked:
            checked.add(candidate)
            candidates.extend(
                    Node(word, node)
                    for word in words
                    if distance(word, candidate) == 1)


def main(targets, words, mode):
    if mode is Mode.SWAP:
        distance = hamming
    elif mode is Mode.ADD_REM_SWAP:
        distance = levenshtein
    else:
        return

    for source, target in pairwise(targets):
        if source not in words:
            sys.exit('unknown word in dictionnary: {}'.format(source))
        if target not in words:
            sys.exit('unknown word in dictionnary: {}'.format(target))
        chain = find_word_ladder(source, target, words, distance)
        print(list(chain))


if __name__ == '__main__':
    #parser = command_line_parser()
    targets, mode = take_inputs()

    try:
        words = read_words("words")
    except OSError as e:
        print("Unable to read word file {}".format(e))

    if mode is Mode.SWAP:
        length = len(targets[-1])
        words = {w for w in words if len(w) == length}

    
    main(targets, words, mode)