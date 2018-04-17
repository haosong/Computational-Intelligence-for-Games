from kalah import Kalah
from math import *
import random
import copy

nodeMap = {}

class Node:
    def __init__(self, move=None, parent=None, player=None, state=None):
        self.state = state
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.player = player
        self.untriedMoves = state.legal_moves()

    def uct_select_child(self):
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(1.5 * log(self.visits) / c.visits))[-1]
        s.parentNode = self
        return s

    def add_child(self, move, state):
        player = state.next_player()
        if (player, state) in nodeMap:
            n = nodeMap[(player, state)]
            n.move = move
            n.parentNode = self
        else:
            n = Node(move=move, parent=self, player=player, state=state)
        nodeMap[(player, state)] = n
        self.untriedMoves.remove(move)
        self.childNodes.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return '%r %r %r' % (self.wins, self.visits, self.state)

def uct(rootstate, itermax):
    if rootstate.is_initial():
        nodeMap.clear()
    
    if (rootstate.next_player(), rootstate) in nodeMap:
        rootnode = nodeMap[(rootstate.next_player(), rootstate)]
        rootnode.childNodes = []
        rootnode.untriedMoves = rootstate.legal_moves()
        rootnode.parentNode = None
    else:
        rootnode = Node(state=rootstate)
        #nodeMap[(rootstate.next_player(), rootstate)] = rootnode
    '''
    # Non-sharing among iterations
    nodeMap.clear()
    rootnode = Node(state=rootstate)
    '''

    for i in range(itermax):
        node = rootnode
        
        # Select
        while node.untriedMoves == [] and node.childNodes != []: 
            node = node.uct_select_child()
        
        # Expand
        if node.untriedMoves != []: 
            move = random.choice(node.untriedMoves)
            state = node.state.result(move)
            node = node.add_child(move, state)
                
        '''
        # Simulate - Using deep copy
        state = copy.deepcopy(node.state)
        while not state.game_over():
            state = state.result(random.choice(state.legal_moves()))
        '''
        # Simulate
        if not node.state.game_over():
            oriState = node.state.result(random.choice(node.state.legal_moves()))
            state = oriState
            while not state.game_over():
                state = state.result(random.choice(state.legal_moves()))
        else:
            state = node.state
                
        # Back-propagate
        curWinner = state.winner()
        while node is not None:
            #win = curWinner * (node.state.next_player() - 0.5) * 2
            win = 1
            if curWinner == 0:
                win = 0.4
            elif (curWinner == 1 and node.player == 0) or (curWinner == -1 and node.player == 1):
                win = -0.2
            node.update(win)
            node = node.parentNode
    return sorted(rootnode.childNodes, key=lambda c: c.wins / c.visits)[-1].move


def mcts_strategy(n):
    def fxn(pos):
        move = uct(pos, n)
        return move

    return fxn


if __name__ == '__main__':
    b = Kalah(6)
    pos = Kalah.Position(b, [6, 4, 2, 0, 0, 2, 9, 0, 0, 2, 2, 6, 6, 9], 0)
    print(mcts_strategy(1000)(pos))

    pos = Kalah.Position(b, [0, 0, 2, 2, 6, 6, 9, 6, 4, 2, 0, 0, 2, 9], 1)
    print(mcts_strategy(1000)(pos))

