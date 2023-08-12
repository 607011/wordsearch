# Wordsearch

This repository contains two related projects to produce and verify searchword puzzles.

## Riddle Generator

The Python script [snakewordcreator.py](https://github.com/607011/wordsearch/blob/main/snakewordcreator.py) generates word search puzzles from a word list read from stdin. Use it like e.g.

```
python3 ./snakewordcreator.py \
  --width 15 \
  --height 14 \
  --hop 1 \
  wordlist.txt
```

to produce a matrix 15 columns wide and 14 rows high. The `1` tells the script to choose a direct neighbor of the current cell to place the next letter; `2` would choose the one after the next, and so on.

If the script produces a **`TypeError: 'type' object is not subscriptable`**, you’re probably running an outdated Python version. Please consider updating your Python installation, or if not possible e.g. if you’re using Windows 7, check out the branch „python3.8“ (`git checkout python3.8`) to get an edition of the script that can be executed with Python 3.8 (and possibly older versions).

### Basic Rules

- The words are read horizontally and vertically: up and down and left and right, but not diagonally.

- The direction can change within a word, even into the opposite direction.

- Words can cross each other, including themselves.

- And particularly nasty: you must think of the matrix as a torus, i.e. words can continue on the opposite edge.

- Ä = AE, Ö = OE, Ü = UE, ß = SS


The rule set can be changed by command-line parameters (see `snakewordcreator.py --help`)

## Word Checker

The Word Checker (see file [check.html](https://github.com/607011/wordsearch/blob/main/check.html)) is a single-page web application in which you can paste a matrix. You can then search the matrix for words.


## Copyright

_Copyright ©️ 2023 [Oliver Lau](mailto:ola@ct.de), [Heise](https://www.heise.de/) Medien GmbH & Co. KG_
