#!/usr/bin/env python3

import sys
import random
from copy import deepcopy

class WordsearchGenerator:
    EMPTY = ' '
    ALL_LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    matrix = None

    def __init__(self, w: int, h: int, words: list, **kwargs):
        self.w = w
        self.h = h
        self.words = words
        self.hop = kwargs['hop'] \
            if 'hop' in kwargs else 1
        self.forbidSameDirection = kwargs['forbidSameDirection'] \
            if 'forbidSameDirection' in kwargs else False
        self.nextDirectionAlgorithm = kwargs['nextDirectionAlgorithm'] \
            if 'nextDirectionAlgorithm' in kwargs else 'shuffle'
        if self.forbidSameDirection and self.nextDirectionAlgorithm == 'preferright':
            print('WARNING: "preferright" algorithm does not respect `forbidSameDirection` attribute.', file=sys.stderr)

    def dump(self):
        for row in zip(*self.matrix):
            print(''.join(row))

    def construct(self) -> list:
        UP, RIGHT, DOWN, LEFT = (0, -self.hop), (+self.hop, 0), (0, +self.hop), (-self.hop, 0)
        self.matrix = [x[:] for x in [[self.EMPTY] * self.h] * self.w]

        def get_random_direction(x: int, y: int, current_letter: str, invalid_direction = None) -> tuple:
            directions = list(filter(lambda d: d != invalid_direction, [RIGHT, LEFT, DOWN, UP]))
            if self.nextDirectionAlgorithm == 'shuffle':
                random.shuffle(directions)
            elif self.nextDirectionAlgorithm == 'forceright':
                pass
            elif self.nextDirectionAlgorithm == 'preferright':
                directions = []
                while not all([item in directions for item in [RIGHT, LEFT, DOWN, UP]]):
                    directions.append(random.choices([RIGHT, LEFT, DOWN, UP], weights=[2, 1, 1, 1], k=1)[0])
            for d in directions:
                letter = self.matrix[(x + d[0]) % self.w][(y + d[1]) % self.h]
                if letter is self.EMPTY or letter is current_letter:
                    return d
            return None, None

        def get_random_xy() -> tuple:
            max_iter = self.w * self.h # practical value
            i = 0
            while i < max_iter:
                x = random.randrange(self.w)
                y = random.randrange(self.h)
                if self.matrix[x][y] is self.EMPTY:
                    return x, y
                i += 1
            return None, None
        
        print('Emplaced words:\n')
        
        max_tries = self.w * self.h # practical value
        for word in self.words:
            i = 0
            while i < max_tries:
                old_matrix = deepcopy(self.matrix)
                x, y = get_random_xy()
                if x is None:
                    break
                last_direction = None
                for letter in word:
                    direction = get_random_direction(x, y, letter, last_direction)
                    dx, dy = direction
                    if dx is None or dy is None:
                        self.matrix = old_matrix
                        break
                    x = (x + dx) % self.w
                    y = (y + dy) % self.h
                    self.matrix[x][y] = letter
                    if self.forbidSameDirection is True:
                        last_direction = direction
                if dx is not None:
                    print(f'- {word}')
                    break
                i += 1
                self.matrix = old_matrix

        num_filled = 0
        for x in range(self.w):
            for y in range(self.h):
                if self.matrix[x][y] == self.EMPTY:
                    self.matrix[x][y] = random.choice(self.ALL_LETTERS)
                    num_filled += 1

        print(f'\nRandomly filled {num_filled} cell{"s" if num_filled != 1 else ""} ({100.0*num_filled/(self.w*self.h):.1f}%)')

    def writeSVG(self, filename):
        scale = 44
        stroke = 'black'
        stroke_width = 2
        fill = 'white'
        with open(filename, 'w+') as svg:
            svg.write(f'<svg version="1.1" viewBox="{-stroke_width} {-stroke_width} {scale*self.w+stroke_width*2} {scale*self.h+stroke_width*2}" width="{scale*self.w}" height="{scale*self.h}" xmlns="http://www.w3.org/2000/svg">\n')
            svg.write(f'  <g stroke="{stroke}" stroke-width="{stroke_width}">\n')
            # draw frame
            svg.write(f'    <rect x="{0}" y="{0}" width="{self.w*scale}" height="{self.h*scale}" rx="0" fill="{fill}" />\n')
            # draw horizontal lines
            for y in range(1, self.h):
                svg.write(f'    <line x1="{0}" y1="{y*scale}" x2="{self.w*scale}" y2="{y*scale}" />\n')
            # draw vertical lines
            for x in range(1, self.w):
                svg.write(f'    <line x1="{x*scale}" y1="{0}" x2="{x*scale}" y2="{self.h*scale}" />\n')
            # draw letters
            svg.write(f'''    <style>
        text {{
            font-family: "Courier New", Courier, monospace;
            font-size: {scale/1.618}px;
            text-anchor: middle;
            dominant-baseline: middle;
            color: {stroke};
        }}
        </style>\n''')
            for y in range(self.h):
                for x in range(self.w):
                    svg.write(f'    <text x="{scale/2+x*scale}" y="{scale/2+y*scale}">{self.matrix[x][y]}</text>\n')
            svg.write('  </g>\n')
            svg.write('</svg>')

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
    wsg = WordsearchGenerator(w, h, words, hop=hop, nextDirectionAlgorithm='shuffle')
    wsg.construct()
    print()
    wsg.dump()
    wsg.writeSVG('matrix.svg')

def usage():
    print('gen.py [width] [height] [hop] < wordlist.txt')

if __name__ == '__main__':
    main(*[int(x) for x in sys.argv[1:4]])
