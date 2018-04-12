import random
import sys
import minimax as minimax
import mcts

from kalah import Kalah


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


def test_game(count, depth, p_random, win_cutoff, p1_h, n):
    ''' Tests a search strategy through a series of complete games of Kalah.
        The test passes if the search wins at least the given percentage of
        games and calls its heuristic function at most the given proportion of times
        relative to Minimax.

        count -- a positive integer
        depth -- the depth to search to
        p_random -- the probability of making a random move instead of the suggested move
        win_cutoff -- the proportion of games won needed to pass
        test_strategy -- a function that takes a depth and heuristic and returns
                         a function that takes a position and returns the move suggested by
                         a search to the given depth
        p1_h -- a heuristic function that takes a game position and returns an integer heuristic
             value, positive for positions where P1 has an advantage and negative where
             P2 has an advantage
        n -- a positive integer
    '''
    board = Kalah(6)

    h1 = minimax.Heuristic(p1_h)
    
    p1_strategy = minimax.minimax_strategy(depth, h1)
    p2_strategy = mcts.mcts_strategy(n)
    
    win_pct = compare_strategies(board, p1_strategy, p2_strategy, count, 1.0 - p_random)

    if win_pct <= 1.0 - win_cutoff:
        print("PASS")
    else:
        print("FAIL")
        print(1.0 - win_pct)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 7 and sys.argv[1] == '-game':
            # parse and verify other command-line arguments
            try:
                count = int(sys.argv[2])
                depth = int(sys.argv[3])
                p_random = float(sys.argv[4])
                wins_cutoff = float(sys.argv[5])
                n = int(sys.argv[6])
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
            if n <= 0:
                raise KalahParseError("n must be positive")
            
            test_game(count, depth, p_random, wins_cutoff, minimax.seeds_stored_heuristic, n)
            sys.exit(0)
    except KalahParseError as err:
        print(sys.argv[0] + ":", str(err))
        sys.exit(1)
    
    print("USAGE: {python3 | pypy3}", sys.argv[0], "-game count depth prob-random wins_cutoff n")
    
