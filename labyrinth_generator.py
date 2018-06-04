#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyleft © Manoel Vilela
#
#

WIDTH,HEIGHT = 2,3
from random import shuffle, randrange

def make_maze(w=WIDTH, h=HEIGHT):

    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    nowalls = []

    def walk(x, y):
        vis[x][y] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]

        shuffle(d)

        for (x_n, y_n) in d:
            if vis[x_n][y_n]:
                continue

            nowalls.append((x, y, x_n, y_n))
            walk(x_n, y_n)

    walk(randrange(h), randrange(w))
    return(nowalls)


def draw_maze(nowalls, w=WIDTH, h=HEIGHT):
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    for (x, y, x_n, y_n) in nowalls:
        if x_n == x:
            ver[x][max(y, y_n)] = "   "
        if y_n == y:
            hor[max(x, x_n)][y] = "+  "

    arrange = []
    for (a, b) in zip(hor, ver):
        l = ''.join(a + ['\n'] + b).split('\n')
        arrange.extend(l)

    return arrange


def random_replace(maze, block):
    from random import randint
    x, y = randint(1, len(maze) - 2), randint(0, len(maze[0]) - 1)
    if maze[x][y] == ' ':
        maze[x] = maze[x][:y] + block + maze[x][y + 1:]
    else:
        maze = random_replace(maze, block)

    return maze


def translate(maze):
    from re import sub
    return [sub(r'[\-\+\|]', 'W', x) for x in maze]


def draw(maze):
    for x, line in enumerate(maze):
        print('{:>2}'.format(x), line)


def generate(width,height,blocks='EP'):
    nw = make_maze(width,height)
    maze = draw_maze(nw,width,height)
    # nwabs = nowallsabs(nw)
    for block in blocks:
        maze = random_replace(maze, block)
    draw(maze)
    translated = translate(maze)
    return translated

if __name__ == '__main__':
    generate()
