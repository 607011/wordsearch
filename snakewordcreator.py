#!/usr/bin/env python3

import sys
import random
from copy import deepcopy


class SnakeWordPuzzleGenerator:
    EMPTY = " "
    ALL_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    matrix = None

    def __init__(self, words: list[str], args):
        self.words = words
        self.w = args.width
        self.h = args.height
        self.forbid_wrap = args.forbid_wrap
        self.hop = args.hop
        self.weights = [args.right_weight, 1, 1, 1]
        self.forbid_same_direction = args.forbid_same_direction
        self.max_tries = args.max_tries
        self.next_direction_algorithm = args.next_direction
        if (
            self.forbid_same_direction
            and self.next_direction_algorithm == "preferright"
        ):
            print(
                'WARNING: "preferright" algorithm does not respect `forbid_same_direction` attribute.',
                file=sys.stderr,
            )
        if args.sort == "ascending":
            self.words = sorted(self.words, key=len, reverse=False)
        elif args.sort == "descending":
            self.words = sorted(self.words, key=len, reverse=True)

    def dump(self):
        for row in zip(*self.matrix):
            print("".join(row))

    def construct(self) -> None:
        UP, RIGHT, DOWN, LEFT = (
            (0, -self.hop),
            (+self.hop, 0),
            (0, +self.hop),
            (-self.hop, 0),
        )
        self.matrix = [x[:] for x in [[self.EMPTY] * self.h] * self.w]
        self.emplaced_words = []

        def get_random_direction(
            x: int, y: int, current_letter: str, invalid_direction=None
        ) -> tuple[int, int]:
            if self.next_direction_algorithm == "shuffle":
                directions = [RIGHT, LEFT, DOWN, UP]
                if invalid_direction is not None:
                    directions.remove(invalid_direction)
                random.shuffle(directions)
            elif self.next_direction_algorithm == "preferright":
                directions = []
                while not all(d in directions for d in [RIGHT, LEFT, DOWN, UP]):
                    choice = random.choices(
                        [RIGHT, LEFT, DOWN, UP],
                        weights=self.weights,
                        k=1,
                    )[0]
                    if choice not in directions:
                        directions.append(choice)
            for direction in directions:
                dx, dy = direction
                if self.forbid_wrap and (
                    ((x + dx) >= self.w)
                    or ((y + dy) >= self.h)
                    or ((x + dx) < 0)
                    or ((y + dy) < 0)
                ):
                    continue
                letter = self.matrix[(x + dx) % self.w][(y + dy) % self.h]
                if letter is self.EMPTY or letter is current_letter:
                    return direction
            return None, None

        def get_random_xy() -> tuple[int, int]:
            max_iter = self.w * self.h  # practical value
            i = 0
            while i < max_iter:
                x = random.randrange(self.w)
                y = random.randrange(self.h)
                if self.matrix[x][y] is self.EMPTY:
                    return x, y
                i += 1
            return None, None


        for word in self.words:
            try_counter = 0
            while try_counter < self.max_tries:
                old_matrix = deepcopy(self.matrix)
                pos = get_random_xy()
                if None in pos:
                    break
                x, y = pos
                last_direction = None
                for letter in word:
                    direction = get_random_direction(
                        x,
                        y,
                        letter,
                        invalid_direction=last_direction,
                    )
                    dx, dy = direction
                    if None in direction:
                        self.matrix = old_matrix
                        break
                    x = (x + dx) % self.w
                    y = (y + dy) % self.h
                    self.matrix[x][y] = letter
                    if self.forbid_same_direction is True:
                        last_direction = direction
                if dx is not None:
                    self.emplaced_words.append(word)
                    break
                try_counter += 1
                self.matrix = old_matrix

        self.num_randomly_filled = 0
        for x in range(self.w):
            for y in range(self.h):
                if self.matrix[x][y] == self.EMPTY:
                    self.matrix[x][y] = random.choice(self.ALL_LETTERS)
                    self.num_randomly_filled += 1


    def write_svg(self, filename):
        scale = 44
        stroke = "black"
        stroke_width = 2
        fill = "white"
        with open(filename, "w+") as svg:
            svg.write(
                f'<svg version="1.1" viewBox="{-stroke_width} {-stroke_width} {scale*self.w+stroke_width*2} {scale*self.h+stroke_width*2}" width="{scale*self.w}" height="{scale*self.h}" xmlns="http://www.w3.org/2000/svg">\n'
            )
            svg.write(f'  <g stroke="{stroke}" stroke-width="{stroke_width}">\n')
            # draw frame
            svg.write(
                f'    <rect x="{0}" y="{0}" width="{self.w*scale}" height="{self.h*scale}" rx="0" fill="{fill}" />\n'
            )
            # draw horizontal lines
            for y in range(1, self.h):
                svg.write(
                    f'    <line x1="{0}" y1="{y*scale}" x2="{self.w*scale}" y2="{y*scale}" />\n'
                )
            # draw vertical lines
            for x in range(1, self.w):
                svg.write(
                    f'    <line x1="{x*scale}" y1="{0}" x2="{x*scale}" y2="{self.h*scale}" />\n'
                )
            # draw letters
            svg.write(
                f"""    <style>
        text {{
            font-family: "Courier New", Courier, monospace;
            font-size: {scale/1.618}px;
            text-anchor: middle;
            dominant-baseline: middle;
            color: {stroke};
        }}
        </style>\n"""
            )
            for y in range(self.h):
                for x in range(self.w):
                    svg.write(
                        f'    <text x="{scale/2+x*scale}" y="{scale/2+y*scale}">{self.matrix[x][y]}</text>\n'
                    )
            svg.write("  </g>\n")
            svg.write("</svg>")


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Snake word puzzle generator.", add_help=False)
    parser.add_argument(
        "-?", "--help", action="help", help="Show this help message and exit."
    )
    parser.add_argument(
        "wordfile", type=str, help="Name of word list file."
    )
    parser.add_argument(
        "-w", "--width", type=int, default=10, metavar="W", help="Width of matrix."
    )
    parser.add_argument(
        "-h", "--height", type=int, default=10, metavar="H", help="Height of matrix."
    )
    parser.add_argument(
        "--svg", type=str, metavar="FILENAME", help="Write matrix to SVG file."
    )
    parser.add_argument(
        "--hop", type=int, default=1, help="Hop so many cells to place next letter."
    )
    parser.add_argument(
        "--max-tries",
        type=int,
        help="Maximum number of tries to place a word. Default is 10 * W * H.",
    )
    parser.add_argument(
        "--sort",
        type=str,
        choices=["ascending", "descending"],
        help="Sort word list in `ascending` or `descending` order.",
    )
    parser.add_argument(
        "-d",
        "--next-direction",
        type=str,
        default="shuffle",
        choices=["shuffle", "preferright"],
        help="Algorithm to determine next direction.",
    )
    parser.add_argument(
        "--right-weight",
        type=int,
        default=1,
        help="Prefer right direction n times as much as other directions.",
    )
    parser.add_argument(
        "--allow-umlauts",
        action="store_true",
        help="Don't replace German umlauts and sharp S with AE, OE, UE, SS.",
    )
    parser.add_argument(
        "--forbid-wrap", action="store_true", help="Do not continue words across edges."
    )
    parser.add_argument(
        "--forbid-same-direction",
        action="store_true",
        help="Don't go into same direction twice in a row.",
    )
    args = parser.parse_args()
    words = []
    for word in open(args.wordfile):
        word = word.rstrip().upper()
        if not args.allow_umlauts:
            word = (
                word.replace("Ä", "AE")
                .replace("Ö", "OE")
                .replace("Ü", "UE")
                .replace("ß", "SS")
            )
        words.append(word)
    if args.max_tries is None:
        args.max_tries = 10 * args.width * args.height
    gen = SnakeWordPuzzleGenerator(words, args)
    gen.construct()
    print("Emplaced words:\n")
    for word in gen.emplaced_words:
        print(f"- {word}")
    print(
        f'\nRandomly filled {gen.num_randomly_filled} cell{"s" if gen.num_randomly_filled != 1 else ""} ({100.0*gen.num_randomly_filled/(gen.w*gen.h):.1f}%)\n'
    )
    gen.dump()
    if args.svg is not None:
        gen.write_svg(args.svg)


if __name__ == "__main__":
    main()