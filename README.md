# Wordsearch

This repository contains two related projects to produce and verify searchword puzzles.

## Riddle Generator

The Python script [gen.py](https://github.com/607011/wordsearch/blob/main/gen.py) generates word search puzzles from a word list read from stdin. Use it like

```
python3 gen.py 15 14 1 < wordlist.txt
```

to produce a matrix 15 columns wide and 14 rows high. The `1` tells the script to choose a direct neighbor of the current cell to place the next letter; `2` would choose the one after the next, and so on.

### The Rules

- The words are read horizontally and vertically: up and down and left and right, but not diagonally.

- The direction can change within a word, even in the opposite direction.

- Words can cross each other, including themselves.

- And particularly nasty: you must think of the matrix as a torus, i.e. words can continue on the opposite edge.

- Ä = AE, Ö = OE, Ü = UE, ß = SS

## Word Checker

The Word Checker (see file [check.html](https://github.com/607011/wordsearch/blob/main/check.html)) is a single-page web application in which you can paste a matrix. You can then search the matrix for words.



### Copyright

_Copyright ©️ 2023 [Oliver Lau](mailto:ola@ct.de), [Heise](https://www.heise.de/) Medien GmbH & Co. KG_
