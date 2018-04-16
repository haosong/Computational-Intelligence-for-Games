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
        if isMaxPlayer:
            s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        else:
            s = sorted(self.childNodes, key=lambda c: c.wins / c.visits - sqrt(2 * log(self.visits) / c.visits))[0]
        s.parentNode = self
        return s

    def add_child(self, move, state, existed):
        n = nodeMap[state] if existed else Node(move=move, parent=self, state=state)
        if existed:
            n.move = move
            n.parentNode = self
        nodeMap[state] = n
        self.untriedMoves.remove(move)
        self.childNodes.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result


def uct(rootstate, itermax):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""
    if rootstate.is_initial:
        nodeMap.clear()

    isMaxPlayer = rootstate.next_player() == 0

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = copy.deepcopy(rootstate)

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.uct_select_child(isMaxPlayer)
            state = node.state

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            move = random.choice(node.untriedMoves)
            state = state.result(move)
            node = node.add_child(move, state, state in nodeMap)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while not state.game_over():  # while state is non-terminal
            state = state.result(random.choice(state.legal_moves()))

        # if state.winner() == 0:
        #     win = 0.5
        # elif state.winner() == 1:  # Player 0 wins
        #     win = 1 if rootstate.next_player() == 1 else 0
        # else:  # Player 1 wins
        #     win = 1 if rootstate.next_player() == 0 else 0

        # win = (state.winner() + 1) * (rootstate.next_player() - 0.5)
        # win = (state.winner() + 1) * ((1 - rootstate.next_player()) - 0.5)
        win = (state.winner() + 1) / 2
        # win = (state.winner() + 1) / 2 if isMaxPlayer else 1- (state.winner() + 1) / 2
        # win = state.winner()
        # print(win)

        # Backpropagate
        while node is not None:
            node.update(win)
            node = node.parentNode

    if isMaxPlayer:
        return sorted(rootnode.childNodes, key=lambda c: c.wins / c.visits)[-1].move
    else:
        return sorted(rootnode.childNodes, key=lambda c: c.wins / c.visits)[0].move


def mcts_strategy(n):
    def fxn(pos):
        move = uct(pos, n)
        return move

    return fxn
