import labyrinth_explorer
import pygame
import search
import random

BLOCKSIZE = 16

def findSolution(method,filterActionsValue,player, end_rect, walls):
    pos = player.position
    problem = None
    if(filterActionsValue==1):
        problem = ProblemFilter((pos[0],pos[1],walls), (end_rect.x, end_rect.y))
    else:
        problem = Problem((pos[0],pos[1],walls), (end_rect.x, end_rect.y))
    solution = None
    if(method==0):
        solution = search.breadthFirstTreeSearch(problem)
    elif(method==1):
        solution = search.breadthFirstGraphSearch(problem)
    elif(method==2):
        solution = search.depthFirstTreeSearch(problem)
    elif(method==3):
        solution = search.depthFirstGraphSearch(problem)
    elif(method==4):
        solution = search.uniformCostSearch(problem)
    elif(method==5):
        solution = search.iterativeDeepeningSearch(problem)
    elif(method==6):
        solution = search.greedyTreeSearch(problem)
    elif(method==7):
        solution = search.greedyGraphSearch(problem)
    elif(method==8):
        solution = search.astarTreeSearch(problem)
    elif(method==9):
        solution = search.astarGraphSearch(problem)
    if(solution==None):
        raise Exception
    print(solution.path())
    return solution.path()

class Problem(object):

    def __init__(self, initial, goal=None):
        self.initial = initial; self.goal = goal

    def actions(self, state):
        actionList = ["Move Up", "Move Down", "Move Right", "Move Left"]
        random.shuffle(actionList)
        return actionList

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

    def h(self, node):
        state = node.state
        xDifference = abs(state[0] - self.goal[0])
        yDifference = abs(state[1] - self.goal[1])
        return xDifference+yDifference

    def f(self, node):
        hValue = self.h(node)
        pathCost = node.pathCost
        return hValue+pathCost

class ProblemFilter(Problem):

    def actions(self, node):
        state = node.state
        walls = state[2]
        actionList = ["Move Up", "Move Down", "Move Right", "Move Left"]
        block = pygame.Rect(state[0], state[1]-1, BLOCKSIZE, BLOCKSIZE)
        for wall in walls:
            if block.colliderect(wall.rect):
                del actionList[actionList.index("Move Up")]
                break
        block.y =state[1]+1
        for wall in walls:
            if block.colliderect(wall.rect):
                del actionList[actionList.index("Move Down")]
                break
        block.y = state[1]
        block.x = state[0]+1
        for wall in walls:
            if block.colliderect(wall.rect):
                del actionList[actionList.index("Move Right")]
                break
        block.x = state[0]-1
        for wall in walls:
            if block.colliderect(wall.rect):
                del actionList[actionList.index("Move Left")]
                break
        return actionList

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
        return x,y,walls