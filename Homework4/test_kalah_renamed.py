import random
import sys
import minimax_renamed as minimax
import search

from kalah_renamed import Kalah


class KalahParseError(Exception):
    pass
        

def random_choice(position):
    moves = position.legal_moves()
    return random.choice(moves)


def compare_strategies(board, p1, p2, games, prob):
    p1_wins = 0
    p2_wins = 0

    for i in range(games):
        position = board.initial_position(4)

        while not position.game_over():
            if random.random() < prob:
                if position.next_player() == i % 2:
                    move = p1(position)
                else:
                    move = p2(position)
            else:
                move = random_choice(position)
            position = position.result(move)

        if position.winner() == 0:
            p1_wins += 0.5
            p2_wins += 0.5
        elif (position.winner() > 0 and i % 2 == 0) or (position.winner() < 0 and i % 2 == 1):
            p1_wins += 1
        else:
            p2_wins += 1

    return p1_wins / games


def test_move(pos_list, turn, depth, test_strategy, h):
    ''' Prints the move suggested by the given strategy..
    
        pos_list -- a list of nonnegative integers giving the number of seeds in each pit in Kalah
        turn -- 0 or 1 to indicate which player is to make the next move
        depth -- a positive integer giving the depth to search to
        test_strategy -- a function that takes a depth and heuristic and returns
                         a function that takes a position and returns the move suggested
                         by a search to the given depth
        h -- a heuristic function that takes a game position and returns an integer heuristic
             value, positive for positions where P1 has an advantage and negative where
             P2 has an advantage
    '''
    board = Kalah(len(pos_list) // 2 - 1)
    pos = Kalah.Position(board, pos_list, turn)
    h = minimax.Heuristic(h)
    strategy = test_strategy(depth, h)
    print(strategy(pos))

    
def test_game(count, depth, p_random, win_cutoff, size_cutoff, test_strategy, p1_h, p2_h):
    ''' Tests a search strategy through a series of complete games of Kalah.
        The test passes if the search wins at least the given percentage of
        games and calls its heuristic function at most the given proportion of times
        relative to Minimax.

        count -- a positive integer
        depth -- the depth to search to
        p_random -- the probability of making a random move instead of the suggested move
        win_cutoff -- the proportion of games won needed to pass
        size_cutoff -- the proportion of calls to the heurustic to allow compared to minimax
        test_strategy -- a function that takes a depth and heuristic and returns
                         a function that takes a position and returns the move suggested by
                         a search to the given depth
        p1_h -- a heuristic function that takes a game position and returns an integer heuristic
             value, positive for positions where P1 has an advantage and negative where
             P2 has an advantage
        p2_h -- a heuristic function that takes a game position and returns an integer heuristic
             value, positive for positions where P1 has an advantage and negative where
             P2 has an advantage
    '''
    board = Kalah(6)

    h1 = minimax.Heuristic(p1_h)
    h2 = minimax.Heuristic(p2_h)
    
    p1_strategy = minimax.minimax_strategy(depth, h1)
    p2_strategy = test_strategy(depth, h2)
    
    win_pct = compare_strategies(board, p1_strategy, p2_strategy, count, 1.0 - p_random)

    if win_pct <= 1.0 - win_cutoff and h2.count_calls() < h1.count_calls() * size_cutoff:
        print("PASS")
    else:
        print("FAIL")
        print(win_pct)
        print(h1.count_calls())
        print(h2.count_calls())

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 8 and len(sys.argv) % 2 == 0 and sys.argv[1] == '-move':
            try:
                depth = int(sys.argv[2])
                turn = int(sys.argv[3])
                pos = [int(sys.argv[i]) for i in range(4, len(sys.argv))]
            except:
                raise KalahParseError("values must be numeric")
            if depth < 0:
                raise KalahParseError("depth must be non-negative")
            if turn != 0 and turn != 1:
                raise KalahParseError("turn must be 0 or 1")
            for x in pos:
                if x < 0:
                    raise KalahParseError("seeds in each pit and store must be non-negative")
            pits = len(pos) / 2 - 1
            if sum(pos) / pits != sum(pos) // pits:
                raise KalahParseError("total number of seeds must be multiple of home pits")
            test_move(pos, turn, depth, search.depth_limited_search_strategy, minimax.seeds_stored_heuristic)
            sys.exit(0)
        elif len(sys.argv) == 7 and (sys.argv[1] == '-game' or sys.argv[1] == '-heuristic'):
            # use student-defined heuristic if specified
            h = minimax.seeds_stored_heuristic
            search_fxn = search.depth_unlimited_search_strategy
            if sys.argv[1] == '-heuristic':
                try:
                    h = search.heuristic
                    search_fxn = minimax.minimax_strategy
                except:
                    raise KalahParseError("no heuristic defined in module search")

            # parse and verify other command-line arguments
            try:
                count = int(sys.argv[2])
                depth = int(sys.argv[3])
                p_random = float(sys.argv[4])
                wins_cutoff = float(sys.argv[5])
                size_cutoff = float(sys.argv[6])
            except:
                raise KalahParseError("values must be numeric")
            if count < 1:
                raise KalahParseError("count must be positive")
            if depth < 1:
                raise KalahParseError("depth must be positive")
            if p_random < 0.0 or p_random > 1.0:
                raise KalahParseError("prob-random must be between 0.0 and 1.0 inclusive")
            if wins_cutoff <= 0.0:
                raise KalahParseError("wins_cutoff must be positive")
            if size_cutoff <= 0.0:
                raise KalahParseError("size_cutoff must be positive")
            
            test_game(count, depth, p_random, wins_cutoff, size_cutoff, search_fxn, minimax.seeds_stored_heuristic, h)
            sys.exit(0)
    except KalahParseError as err:
        print(sys.argv[0] + ":", str(err))
        sys.exit(1)
    
    print("USAGE: {python3 | pypy3}", sys.argv[0], "{-move depth turn pit1...pit14 | {-game | -heuristic} count depth prob-random wins_cutoff size_cutoff}")
    
