import sys
import scipy.optimize
import numpy
import pickle


def getPayoff(cur_down, down_yards, touchdown_yards, time):
    try:
        cur_down = int(cur_down)
        down_yards = int(down_yards)
        touchdown_yards = int(touchdown_yards)
        time = int(time)
    except ValueError:
        raise ValueError()

    data = pickle.load(open("two_minute.pickle", "rb"))
    tuple = (42, 1, 30, 24)
    data[tuple]

    slant_37 = [[(-1, 4, False), (20, 3, False), (10, 2, False), (7, 2, False), (4, 2, False)],
                [(1, 3, False), (10, 2, False), (5, 2, False), (1, 4, False), (2, 2, False)],
                [(8, 2, False), (20, 3, False), (4, 2, False), (2, 2, False), (6, 2, False)]]

    y_cross_80 = [[(0, 1, True), (-7, 4, False), (0, 1, False), (0, 1, True), (24, 2, False)],
                  [(0, 1, False), (0, 1, True), (-6, 4, False), (18, 2, False), (13, 2, False)],
                  [(19, 4, False), (0, 1, True), (22, 2, False), (47, 3, False), (0, 1, False)]]

    z_corner_82 = [[(28, 3, False), (-9, 4, False), (47, 3, False), (0, 1, False), (0, 1, False)],
                   [(30, 3, False), (-9, 4, False), (8, 2, False), (-8, 4, False), (0, 1, False)],
                   [(38, 3, False), (0, 1, True), (0, 1, False), (-9, 4, False), (0, 1, False)]]

    plays = [slant_37, y_cross_80, z_corner_82]
    prob = [0.20, 0.05, 0.25, 0.1, 0.4]

    P = []
    for i in range(0, 3):
        row = []
        for j in range(0, 3):
            payoff = 0
            for k in range(0, 5):
                play = plays[i][j][k]
                new_time = max(0, time / 5 - play[1])
                if not play[2]: # Not turn over and still have time
                    gain_yards = play[0]
                    new_touchdown_yards = max(0, touchdown_yards - gain_yards)
                    if new_touchdown_yards == 0:
                        tuple = (0, 0, 0, 0) # TouchDown!
                    elif gain_yards >= down_yards:
                        tuple = (new_touchdown_yards, 4, min(new_touchdown_yards, (new_touchdown_yards / 10 + 1) * 10 - new_touchdown_yards), new_time)
                    elif cur_down < 4:
                        tuple = (new_touchdown_yards, 4 - cur_down, down_yards - gain_yards, new_time)
                    else:
                        tuple = (1, 0, 0, 0) # Loss!
                    # print(tuple)
                    payoff += prob[k] * data[tuple]
            row.append(payoff)
        P.append(row)
    return P


def getEquilibrium(P):
    rows = 3
    cols = 3

    a1 = -1 * numpy.transpose(P)
    bounds = (0, 1 / min([min(tmp) for tmp in P]))
    b_ub = [-1.0] * rows
    c = [1.0] * cols
    result = scipy.optimize.linprog(c, a1, b_ub, None, None, bounds)
    value = 1.0 / result.fun
    x = [xi * value for xi in result.x]

    a2 = P
    b_ub = [1.0] * rows
    c = [-1.0] * cols
    result = scipy.optimize.linprog(c, a2, b_ub, None, None, bounds)
    y = [yi * value for yi in result.x]

    print_array(x, 6)
    print_array(y, 6)
    print(format(value, '.6f'))


def print_array(nums, digit):
    print('[%s]' % (', '.join([format(x, '.' + str(digit) + 'f') for x in nums])))


def main(argv):
    try:
        if len(argv) == 6 and argv[1] == "-matrix":
            P = getPayoff(argv[2], argv[3], argv[4], argv[5])
            for row in P:
                print_array(row, 6)
        elif len(argv) == 5:
            P = getPayoff(argv[1], argv[2], argv[3], argv[4])
            getEquilibrium(P)
    except ValueError:
        pass


if __name__ == "__main__":
    main(sys.argv)

