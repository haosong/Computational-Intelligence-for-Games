from math import *
import random
import copy

nodeMap = {}


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.unvisited = state.legal_moves()
        self.parent = parent
        self.child = []
        self.wins = 0
        self.visits = 0

    def uct_select_child(self):
        s = sorted(self.child, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def add_child(self, m, s, existed):
        n = nodeMap.get(s) if existed else Node(move=m, parent=self, state=s)
        if not existed:
            nodeMap[s] = n
        self.child.append(n)
        self.unvisited.remove(m)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result


def uct(pos, n):

    root = Node(state=pos)

    for i in range(n):
        node = root
        state = copy.deepcopy(pos)

        # Selection
        while node.untriedMoves == [] and node.children != []:
            node = node.uct_select_child()
            state = state.result(node.move)

        # Expansion
        if node.untriedMoves:
            m = random.choice(node.untriedMoves)
            state = state.result(m)
            node = node.add_child(m, state, state in nodeMap)

        # Simulation
        while not state.game_over():
            state = state.result(random.choice(state.legal_moves()))

        # Backpropagation
        while node is not None:
            node.update(state.winner())
            node = node.parentNode

    return sorted(root.child, key=lambda c: c.visits)[-1].move


def mcts_strategy(n):
    def fxn(pos):
        move = uct(pos, n)
        return move

    return fxn
