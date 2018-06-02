from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

    def path(self):
        actions = []
        actions.append(self.action)
        parent = self.parent
        while(parent != None):
            actions.append(parent.action)
            parent = parent.parent
        actions = actions[::-1]
        return actions[1:]


def bfs(problem):
    queue = deque()
    queue.append(Node(problem.initial))
    while queue:
        t = queue.popleft()
        if problem.goal_test(t.state):
            return t
        for action in problem.actions(t):
            u = problem.result(t, action)
            queue.append(Node(u,t, action))

    return None