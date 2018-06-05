from collections import deque
import heapq
import itertools

class Node:
    '''
    Used to store information for the search algorithms
    such as the sate, parent node, action to the node,
    the path cost from node to node, the problem it is used in
    and the depth of the current node
    '''
    def __init__(self, state, parent=None, action=None, pathCost=0, problem=None):
        '''
        Used to initialise the node class. A lot of search algorithms need particular
        properties of a node. This class is used for all of them
        '''
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        self.problem = problem
        self.depth=0
        if parent:
            self.depth = parent.depth +1

    def __lt__(self, other):
        '''
        Used since heapq needs to be able to use the "<" symbol
        between two nodes.
        '''
        if(self.problem==None):
            raise Exception
        currentNumber = self.problem.f(self)
        otherNumber = self.problem.f(other)
        if(currentNumber<otherNumber):
            return True
        return False

    def path(self):
        '''
        Used to get the path from the initial node to the current node
        '''
        actions = []
        actions.append(self.action)
        parent = self.parent
        while(parent != None):
            actions.append(parent.action)
            parent = parent.parent
        actions = actions[::-1]
        return actions[1:]

#-----------------------------------------------------------------------------------------------#
#                          The rest of the code are search algorithms                           #

def breadthFirstTreeSearch(problem):
    queue = deque()
    queue.append(Node(problem.initial))
    while queue:
        node = queue.popleft()
        if problem.goal_test(node.state):
            return node
        for action in problem.actions(node):
            newNode = problem.result(node, action)
            queue.append(Node(newNode,node, action))
    return None

def breadthFirstGraphSearch(problem):
    explored = set()
    queue = deque()
    queue.append(Node(problem.initial))
    while queue:
        node = queue.popleft()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state[0:2])
        for action in problem.actions(node):
            newState = problem.result(node, action)
            if(newState[0:2] not in explored):
                queue.append(Node(newState,node, action))
    return None

def depthFirstTreeSearch(problem):
    queue = deque()
    queue.append(Node(problem.initial))
    while queue:
        node = queue.pop()
        if problem.goal_test(node.state):
            return node
        for action in problem.actions(node):
            newNode = problem.result(node, action)
            queue.append(Node(newNode,node, action))
    return None

def depthFirstGraphSearch(problem):
    explored = set()
    queue = deque()
    queue.append(Node(problem.initial))
    while queue:
        node = queue.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state[0:2])
        for action in problem.actions(node):
            newState = problem.result(node, action)
            if(newState[0:2] not in explored):
                queue.append(Node(newState,node, action))
    return None

def greedyTreeSearch(problem):
    initialNode = Node(problem.initial, problem=problem)
    queue = []
    heapq.heappush(queue, (problem.h(initialNode), initialNode))
    while queue:
        node = heapq.heappop(queue)[1]
        if problem.goal_test(node.state):
            return node
        for action in problem.actions(node):
            newState = problem.result(node, action)
            newNode = Node(newState,node, action,problem=problem)
            heapq.heappush(queue, (problem.h(newNode), newNode))
    return None

def greedyGraphSearch(problem):
    initialNode = Node(problem.initial, problem=problem)
    explored = set()    
    queue = []
    heapq.heappush(queue, (problem.h(initialNode), initialNode))
    while queue:
        node = heapq.heappop(queue)[1]
        if problem.goal_test(node.state):
            return node
        explored.add(node.state[0:2])
        for action in problem.actions(node):
            newState = problem.result(node, action)
            newNode = Node(newState,node, action,problem=problem)
            if(newState[0:2] not in explored):
                heapq.heappush(queue, (problem.h(newNode), newNode))
    return None

def astarTreeSearch(problem):
    initialNode = Node(problem.initial, problem=problem)
    queue = []
    heapq.heappush(queue, (problem.f(initialNode), initialNode))
    while queue:
        node = heapq.heappop(queue)[1]
        if problem.goal_test(node.state):
            return node
        for action in problem.actions(node):
            newState = problem.result(node, action)
            newNode = Node(newState,node, action,pathCost = 1,problem=problem)
            heapq.heappush(queue, (problem.f(newNode), newNode))
    return None

def astarGraphSearch(problem):
    initialNode = Node(problem.initial, problem=problem)
    explored = set()    
    queue = []
    heapq.heappush(queue, (problem.f(initialNode), initialNode))
    while queue:
        node = heapq.heappop(queue)[1]
        if problem.goal_test(node.state):
            return node
        explored.add(node.state[0:2])
        for action in problem.actions(node):
            newState = problem.result(node, action)
            newNode = Node(newState,node, action,pathCost = 1,problem=problem)
            if(newState[0:2] not in explored):
                heapq.heappush(queue, (problem.f(newNode), newNode))
    return None

def uniformCostSearch(problem):
    initialNode = Node(problem.initial, problem=problem)
    explored = set()    
    queue = []
    heapq.heappush(queue, (problem.f(initialNode), initialNode))
    while queue:
        node = heapq.heappop(queue)[1]
        if problem.goal_test(node.state):
            return node
        explored.add(node.state[0:2])
        for action in problem.actions(node):
            newState = problem.result(node, action)
            newNode = Node(newState,node, action,pathCost = 1,problem=problem)
            if(newState[0:2] not in explored):
                heapq.heappush(queue, (newNode.pathCost, newNode))
    return None

def depthLimitedSearch(problem, limit=50):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for action in problem.actions(node):
                newState = problem.result(node, action)
                newNode = Node(newState,node, action)
                result = recursive_dls(newNode, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            if cutoff_occurred:
                return 'cutoff'
            else:
                return None
    return recursive_dls(Node(problem.initial), problem, limit)

def iterativeDeepeningSearch(problem):
    for depth in itertools.count():
        result = depthLimitedSearch(problem, depth)
        if result != 'cutoff':
            return result
    