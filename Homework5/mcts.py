from kalah import Kalah
from random import choice
from math import sqrt, log

node = {}  # {<player, position>, [wins, plays]}
nextPos = {}  # {<position>, [all next possible positions]}


def get_next_pos(pos):
    if pos not in nextPos:
        all_next_pos = [pos.result(move) for move in pos.legal_moves()]
        nextPos[pos] = all_next_pos
    return nextPos[pos]

def mcts(pos):
    path = set()
    player = pos.next_player()
    expand = True

    while True:
        all_next_pos = [pos.result(move) for move in pos.legal_moves()]
        # all_next_pos = get_next_pos(pos)
        # Select
        if all(node.get((player, pos)) for pos in all_next_pos):
            Tn = 1.5 * log(sum(node[(player, pos)][1] for pos in all_next_pos))
            def ucb(pos):
                wi = node[(player, pos)][0]
                vi = node[(player, pos)][1]
                return wi / vi + sqrt(Tn / vi)
            next_pos = max(all_next_pos, key=ucb)
        # Simulate
        else:
            next_pos = choice(all_next_pos)
        # Expand
        if expand:
            path.add((player, next_pos))
        if expand and (player, next_pos) not in node:
            expand = False
            node[(player, next_pos)] = [0, 0]
        # Update Player
        pos = next_pos
        player = pos.next_player()
        winner = next_pos.winner()
        if winner is not None:
            break

    # Back-propagate
    for player, pos in path:
        if (player, pos) in node:
            node[(player, pos)][1] += 1
            win = -0.2
            if winner == 0:
                win = 0.4
            elif (player == 0 and winner == 1) or (player == 1 and winner == -1):
                win = 1
            node[(player, pos)][0] += win


def mcts_strategy(n):
    def fxn(pos):
        if not pos.legal_moves():
            return None
        if pos.is_initial():
            nextPos.clear()
            node.clear()
        for i in range(n):
            mcts(pos)
        player = pos.next_player()
        moves_res = [(move, pos.result(move)) for move in pos.legal_moves()]
        _, best_move = max((node.get((player, pos), [0, 0])[0] / node.get((player, pos), [1, 1])[1], move) for move, pos in moves_res)
        return best_move

    return fxn

