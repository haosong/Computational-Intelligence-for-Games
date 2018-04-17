from kalah import Kalah
from math import *
import random
import copy

nodeMap = {}


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.state = state
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.legal_moves()

    def uct_select_child(self, isMaxPlayer):
        #if isMaxPlayer:
        s = sorted(self.childNodes, key=lambda c: nodeMap[c].wins / nodeMap[c].visits + sqrt(2 * log(self.visits) / nodeMap[c].visits))[-1]
        #else:
        # s = sorted(self.childNodes, key=lambda c: nodeMap[c].wins / nodeMap[c].visits - sqrt(2 * log(self.visits) / nodeMap[c].visits))[0]
        node = nodeMap[s]
        node.parentNode = self
        return node

    def add_child(self, move, state, existed):
        n = nodeMap[state] if existed else Node(move=move, parent=self, state=state)
        if existed:
            n.move = move
            n.parentNode = self
        nodeMap[state] = n
        self.untriedMoves.remove(move)
        self.childNodes.append(state)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result


def uct(rootstate, itermax):

    if rootstate.is_initial:
        nodeMap.clear()

    isMaxPlayer = rootstate.next_player() == 0

    if rootstate in nodeMap:
        rootnode = nodeMap[rootstate]
        rootnode.parentNode = None
    else:
        rootnode = Node(state=rootstate)
        nodeMap[rootstate] = rootnode

    for i in range(itermax):
        node = rootnode

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.uct_select_child(isMaxPlayer)
            # state = node.state
        state = copy.deepcopy(node.state)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            move = random.choice(node.untriedMoves)
            state = state.result(move)
            node = node.add_child(move, state, state in nodeMap)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while not state.game_over():  # while state is non-terminal
            state = state.result(random.choice(state.legal_moves()))

        # Backpropagate
        curWinner = state.winner()
        while node is not None:
            # 41.5%
            win = curWinner * (node.state.next_player() - 0.5) * 2
            
            # 42.5%
            #win = 1
            #if curWinner == 0:
            #    win = 0.5
            #elif (curWinner == 1 and node.state.next_player() == 0) or (curWinner == -1 and node.state.next_player() == 1):
            #    win = 0
            node.update(win)
            node = node.parentNode

    #if isMaxPlayer:
    return nodeMap[sorted(rootnode.childNodes, key=lambda c: nodeMap[c].wins / nodeMap[c].visits)[-1]].move
    #else:
    #return nodeMap[sorted(rootnode.childNodes, key=lambda c: nodeMap[c].wins / nodeMap[c].visits)[0]].move


def mcts_strategy(n):
    def fxn(pos):
        move = uct(pos, n)
        return move

    return fxn

