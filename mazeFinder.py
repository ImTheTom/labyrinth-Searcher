import labyrinth_explorer
import pygame
import search
import random

BLOCKSIZE = 16

def findSolution(method,filterActionsValue,player, end_rect, walls):
    '''
    Used to call the correct problem and search method deteremined by the GUI
    Returns the path from a node
    '''
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
    '''
    Problem class is an object that is used in search algorithms
    it is used to determine if a state is a goal state and all
    possible actions and results for states
    '''

    def __init__(self, initial, goal=None):
        '''
        Used to initialse an inital state and a goal state
        '''
        self.initial = initial; self.goal = goal

    def actions(self, state):
        '''
        Used to get all posible actions for a state. List is shuffled
        so that a depth first search doesn't just loop one action that
        can't be performed for a given state.
        '''
        actionList = ["Move Up", "Move Down", "Move Right", "Move Left"]
        random.shuffle(actionList)
        return actionList

    def result(self, node, action):
        '''
        Used to get the state after an action is used on a node
        returns the new state of the node
        '''
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
        '''
        Used to determine if the current state of a node is the goal state.
        '''
        return(state[0] == self.goal[0] and state[1]==self.goal[1])

    def h(self, node):
        '''
        Used to determine the h value. The h value
        is the distance from the state to the goal.
        Distance is the manhattan distance.
        '''
        state = node.state
        xDifference = abs(state[0] - self.goal[0])
        yDifference = abs(state[1] - self.goal[1])
        return xDifference+yDifference

    def f(self, node):
        '''
        Used to determine the f value or
        the h value + the path cost to the node.
        Used in A star searches.
        '''
        hValue = self.h(node)
        pathCost = node.pathCost
        return hValue+pathCost

class ProblemFilter(Problem):
    '''
    ProblemFilter is a class based from the problem class
    The difference is that the actions method only returns
    actions that can be done for a given state. Actions that
    are filtered out are actions that result in a collision
    with any wall
    '''

    def actions(self, node):
        '''
        Used to get the list of actions that can occur for a given state.
        Actions that can't be done aren't added to the action list.
        returns a list of actions.
        '''
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
        '''
        Determines the result from the given action. 
        Since actions are filtered no need to check
        if the action can be done.
        Returns the state after the action is completed
        '''
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