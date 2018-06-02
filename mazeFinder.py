import labyrinth_explorer
import pygame
import search

import itertools

BLOCKSIZE = 16

def findSolution(player, end_rect, walls):
    pos = player.position
    prob = Problem((pos[0],pos[1],walls), (end_rect.x, end_rect.y))
    a = search.bfs(prob)
    print(a.path())
    return a.path()

class Problem(object):

    def __init__(self, initial, goal=None):
        self.initial = initial; self.goal = goal

    def actions(self, state):
        return["Move Up", "Move Down", "Move Right", "Move Left"]

    def result(self, node, action):
        state = node.state
        x = state[0]
        y = state[1]
        walls = state[2]
        if(action == "Move Up"):
            y -=BLOCKSIZE
        elif(action == "Move Down"):
            y +=BLOCKSIZE
        elif(action == "Move Right"):
            x += BLOCKSIZE
        elif(action == "Move Left"):
            x -= BLOCKSIZE
        block = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        for wall in walls:
            if block.colliderect(wall.rect):
                return state
        return x,y,walls

    def goal_test(self, state):
        return(state[0] == self.goal[0] and state[1]==self.goal[1])