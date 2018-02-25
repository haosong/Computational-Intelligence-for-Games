# defenses are 4-3 Blast Man-to-man, 4-3 Sam-Will Blitz, Prevent
# outcomes are (yards, time, turnover)
# probability of outcomes are .20, .05, .25, .1, .4 (not measured carefully)

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

