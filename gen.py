#!/usr/bin/env python3

import sys
import random
from copy import deepcopy

def dump(matrix):
    for row in matrix:
        print(''.join(row))


def construct(w: int, h: int, hop: int, words: list) -> list:
    EMPTY = ' '
    UP, RIGHT, DOWN, LEFT = (0, -hop), (+hop, 0), (0, +hop), (-hop, 0)
    ALL_LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    m = [x[:] for x in [[EMPTY] * h] * w]

    def get_random_direction(x: int, y: int, current_letter: str, invalid_direction: str = '') -> tuple:
        directions = list(filter(lambda d: d != invalid_direction, [UP, RIGHT, DOWN, LEFT]))
        random.shuffle(directions)
        for d in directions:
            letter = m[(x + d[0]) % w][(y + d[1]) % h]
            if letter is EMPTY or letter is current_letter:
                return d
        return None, None

    def get_random_xy() -> tuple:
        max_iter = w * h
        i = 0
        while i < max_iter:
            x = random.randrange(w)
            y = random.randrange(h)
            if m[x][y] is EMPTY:
                return x, y
            i += 1
        return None, None
    
    max_tries = 100
    for word in words:
        i = 0
        while i < max_tries:
            old_matrix = deepcopy(m)
            x, y = get_random_xy()
            if x is None:
                break
            last_direction = None
            for letter in word:
                direction = get_random_direction(x, y, letter, last_direction)
                dx, dy = direction
                if dx is None or dy is None:
                    m = old_matrix
                    break
                x = (x + dx) % w
                y = (y + dy) % h
                m[x][y] = letter
                last_direction = direction
            if dx is not None:
                print(word)
                break
            i += 1
            m = old_matrix

    num_filled = 0
    for x in range(w):
        for y in range(h):
            if m[x][y] == EMPTY:
                m[x][y] = random.choice(ALL_LETTERS)
                num_filled += 1
    print(f'Randomly filled: {num_filled}')
    return zip(*m)

def main(w: int = 7, h: int = 7, hop: int = 1):
    words = []
    for word in sys.stdin:
        word = word.rstrip().upper()\
            .replace('Ä', 'AE')\
            .replace('Ö', 'OE')\
            .replace('Ü', 'UE')\
            .replace('ß', 'SS')
        words.append(word.rstrip())
    words = sorted(words, key=len, reverse=True)
    matrix = construct(w, h, hop, words)
    print()
    dump(matrix)

def usage():
    print('gen.py [width] [height] [hop] < wordlist.txt')

if __name__ == '__main__':
    main(*[int(x) for x in sys.argv[1:4]])
