"""
Script to generaze maps of differing complexity

"""

from random import shuffle, randrange
import pygame

SIZE = 15


def make_maze(w=SIZE, h=SIZE):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+ "
            if yy == y: ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    out = []
    s = ""

    f = open(f"out_{SIZE}x{SIZE}.txt", "w+")
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
        out.append(a)
        out.append(b)
        f.write(''.join(a + ['\n'] + b + ['\n']))

    return out


class MazeReader:

    def __init__(self, filename):
        self.maze = self.read_maze(filename)

    def read_maze(self, filename):
        out = []
        for line in open(filename).readlines():
            out.append(list(line.strip("\n")))
        return out


make_maze()
