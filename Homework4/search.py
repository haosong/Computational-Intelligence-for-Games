tt = {}


# alpha-beta without tt
def depth_limited_search(pos, alpha, beta, depth, h):
    if pos.game_over() or depth == 0:
        return h.evaluate(pos), None
    else:
        if pos.next_player() == 0:
            # max player
            a = -h.inf
            best_move = None
            moves = pos.legal_moves()
            for move in moves:
                if alpha >= beta:
                    break
                child = pos.result(move)
                mm, _ = depth_limited_search(child, alpha, beta, depth - 1, h)
                alpha = max(alpha, a)
                if mm > a:
                    a = mm
                    best_move = move
            return a, best_move
        else:
            # min player
            b = h.inf
            best_move = None
            moves = pos.legal_moves()
            for move in moves:
                if alpha >= beta:
                    break
                child = pos.result(move)
                mm, _ = depth_limited_search(child, alpha, beta, depth - 1, h)
                beta = min(beta, b)
                if mm < b:
                    b = mm
                    best_move = move
            return b, best_move


def depth_limited_search_strategy(depth, h):
    def fxn(pos):
        value, move = depth_limited_search(pos, -h.inf, h.inf, depth, h)
        return move

    return fxn


# alpha-beta with tt
def depth_unlimited_search(pos, alpha, beta, depth, h):
    if pos in tt:
        [low, up], move, d = tt[pos]
        if d >= depth and (low == up or low >= beta or up <= alpha):
            return [low, up], move
    if pos.game_over() or depth == 0:
        v = h.evaluate(pos)
        tt[pos] = [v, v], None, depth
        return [v, v], None
    else:
        if pos.next_player() == 0:
            # max player
            bound = [-h.inf, -h.inf]
            best_move = None
            moves = pos.legal_moves()
            for move in moves:
                if alpha >= beta:
                    bound[1] = h.inf
                    break
                child = pos.result(move)
                mm, _ = depth_unlimited_search(child, alpha, beta, depth - 1, h)
                if mm[0] > bound[0]:
                    best_move = move
                bound = [max(bound[0], mm[0]), max(bound[1], mm[1])]
                alpha = max(alpha, bound[0])
            tt[pos] = bound, best_move, depth
            return bound, best_move
        else:
            # min player
            bound = [h.inf, h.inf]
            best_move = None
            moves = pos.legal_moves()
            for move in moves:
                if alpha >= beta:
                    bound[0] = -h.inf
                    break
                child = pos.result(move)
                mm, _ = depth_unlimited_search(child, alpha, beta, depth - 1, h)
                if mm[1] < bound[1]:
                    best_move = move
                bound = [min(bound[0], mm[0]), min(bound[1], mm[1])]
                beta = min(beta, bound[1])
            tt[pos] = bound, best_move, depth
            return bound, best_move


def depth_unlimited_search_strategy(depth, h):
    def fxn(pos):
        value, move = depth_unlimited_search(pos, -h.inf, h.inf, depth, h)
        return move

    return fxn
