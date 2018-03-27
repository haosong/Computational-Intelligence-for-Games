class Kalah:
    def __init__(self, p):
        ''' Creates a Kalah board with the given number of houses
            per side (plus two store pits) each containing the given.
            p -- a nonnegative integer
        '''
        if p < 0:
            raise ValueError('Number of pits must be positive: %d' % p)

        # pits are numbered 0, ..., 2p-1 with p and 2p+1 being the home
        # pit for player 0 and player 1 respectively and pits numbered
        # clockwise around the board
        self.pits = p;
        self.size = 2 * p + 2
        self.stores = [p, 2 * p + 1]

        # the sequence to sow in starting from each house
        self.sequence = []
        # sequences for player 0
        for i in range(0, p):
            self.sequence.append([])
            for j in range(1, self.size + 1):
                if (i + j) % self.size != self.stores[1]:
                    self.sequence[-1].append((i + j) % self.size)
        self.sequence.append(None) # no sequence for P0's store

        # sequences for player 1
        for i in range(p + 1, self.size - 1):
            self.sequence.append([])
            for j in range(1, self.size + 1):
                if (i + j) % self.size != self.stores[0]:
                    self.sequence[-1].append((i + j) % self.size)
        self.sequence.append(None) # no sequence for P1's store

        # compute which pits are opposite each other (home pits have no opposite)
        # and which pits are owned (sowable from) by which player
        self.opposite = [None] * (self.size)
        self.owner = [None] * (self.size)
        for i in range(0, p):
            self.opposite[i] = self.size - 2 - i
            self.opposite[self.size - 2 - i] = i
            self.owner[i] = 0
            self.owner[p + 1 + i] = 1

    def initial_position(self, s):
        ''' Creates the initial position for this board with s seeds
            per house and starting with P0's turn.

            s -- a positive integer
        '''
        if s < 0:
            raise ValueError('Number of seeds must be positive: %d' % s)
        seeds = []
        for i in range(0, self.size):
            if self.owner[i] is not None:
                seeds.append(s)
            else:
                seeds.append(0)
        return Kalah.Position(self, seeds, 0)

    class Position:
        def __init__(self, board, seeds, turn):
            if board is None:
                raise ValueError('board cannot be None')
            if len(seeds) != board.size:
                raise ValueError('mismatch between size of seeds list and size of board: %d vs %d' % len(seeds), board.size)
            if turn != 0 and turn != 1:
                raise ValueError('invalid turn %d' % turn)
            
            self._secret_prefix_board = board
            self._secret_prefix_seeds = seeds
            self._secret_prefix_turn = turn

            self._secret_prefix_seeds_left = [sum(seeds[0:board.pits]), sum(seeds[board.pits + 1:board.pits * 2 + 1])]
            
            self._compute_hash()

        def next_player(self):
            ''' Returns the index of the player who makes the next move from
                this position.
            '''
            return self._secret_prefix_turn
            
        def is_legal(self, p):
            ''' Determines if sowing from the given move is legal from this position.

                p -- the index of a pit in this position
            '''
            if p < 0 or p >= self._secret_prefix_board.size:
                raise ValueError('Illegal house %d' % p)

            return self._secret_prefix_board.owner[p] == self._secret_prefix_turn and self._secret_prefix_seeds[p] > 0

        def legal_moves(self):
            ''' Returns a list of legal moves from this position.
                The list of moves is given as a list of pits to sow from.
                Pits are indexed clockwise starting with 0 for player 0's
                first pit.
            '''
            moves = []
            if self._secret_prefix_turn == 0:
                first = 0
            else:
                first = self._secret_prefix_board.pits + 1

            for i in range(0, self._secret_prefix_board.pits):
                if self._secret_prefix_seeds[first + i] > 0:
                    moves.append(first + i)

            return moves

        def result(self, p):
            ''' Returns the position that results from sowing from the given pit
                from this position.

                p -- the index of a legal pit to sow from in this position
            '''
            if (p < 0 or p >= self._secret_prefix_board.size) or self._secret_prefix_board.owner[p] != self._secret_prefix_turn or self._secret_prefix_seeds[p] <= 0:
                raise ValueError('Illegal move: %d' % p)

            succ = Kalah.Position(self._secret_prefix_board, self._secret_prefix_seeds[:], self._secret_prefix_turn)

            sowing = succ._secret_prefix_seeds[p];
            succ._secret_prefix_seeds[p] = 0
            succ._secret_prefix_seeds_left[self._secret_prefix_turn] -= sowing
            timesAround = sowing // (self._secret_prefix_board.size - 1) # number of complete times around
            extras = sowing % (self._secret_prefix_board.size - 1) # number of pits to sow into after complete
            last = succ._secret_prefix_board.sequence[p][(extras - 1 + self._secret_prefix_board.size - 1) % (self._secret_prefix_board.size - 1)] # pit ending in
            for i in range(0, extras):
                pit = succ._secret_prefix_board.sequence[p][i]
                succ._secret_prefix_seeds[pit] += timesAround + 1
                if succ._secret_prefix_board.owner[pit] is not None:
                    succ._secret_prefix_seeds_left[succ._secret_prefix_board.owner[pit]] += timesAround + 1
            if timesAround > 0:
                for i in range(extras, self._secret_prefix_board.size - 1):
                    pit = succ._secret_prefix_board.sequence[p][i]
                    succ._secret_prefix_seeds[pit] += timesAround
                    if succ._secret_prefix_board.owner[pit] is not None:
                        succ._secret_prefix_seeds_left[succ._secret_prefix_board.owner[pit]] += timesAround

            # capture opposite seeds if end in own empty pit and opposite is not empty
            if succ._secret_prefix_seeds[last] == 1 and succ._secret_prefix_board.opposite[last] is not None and succ._secret_prefix_seeds[succ._secret_prefix_board.opposite[last]] > 0 and succ._secret_prefix_board.owner[last] == self._secret_prefix_turn:
                captured = succ._secret_prefix_seeds[succ._secret_prefix_board.opposite[last]]
                succ._secret_prefix_seeds[succ._secret_prefix_board.stores[self._secret_prefix_turn]] += (1 + captured)
                succ._secret_prefix_seeds_left[self._secret_prefix_turn] -= 1
                succ._secret_prefix_seeds_left[1 - self._secret_prefix_turn] -= captured
                succ._secret_prefix_seeds[last] = 0
                succ._secret_prefix_seeds[succ._secret_prefix_board.opposite[last]] = 0

            # free turn if ending in store
            if last == succ._secret_prefix_board.stores[self._secret_prefix_turn]:
                succ._secret_prefix_turn = self._secret_prefix_turn
            else:
                succ._secret_prefix_turn = 1 - self._secret_prefix_turn

            # game is over if one player has no seeds left
            if succ._secret_prefix_seeds_left[0] == 0 or succ._secret_prefix_seeds_left[1] == 0:
                for p in range(0, 2):
                    succ._secret_prefix_seeds[succ._secret_prefix_board.stores[p]] += succ._secret_prefix_seeds_left[p]
                    succ._secret_prefix_seeds_left[p] = 0
                for p in range(0, succ._secret_prefix_board.size):
                    if succ._secret_prefix_board.owner[p] is not None:
                        succ._secret_prefix_seeds[p] = 0

            succ._compute_hash()
                
            return succ

        def game_over(self):
            ''' Determines if this position is terminal -- whether the game is over having reached this position.
            '''
            return sum(self._secret_prefix_seeds_left) == 0

        def _winner(self):
            return self.winner()
        
        def winner(self):
            ''' Returns the winner of a game in this position, or None if this position is not final.
            '''
            if not self.game_over():
                return None
            else:
                difference = self._secret_prefix_seeds[self._secret_prefix_board.stores[0]] - self._secret_prefix_seeds[self._secret_prefix_board.stores[1]]
                return (difference > 0) - (difference < 0)

        def _secret_prefix_seeds_stored(self, p):
            ''' Returns the number of seeds in the store for the given player.
               
                p -- the index of a player; either 0 or 1
            '''
            return self._secret_prefix_seeds[self._secret_prefix_board.stores[p]]

        def __str__(self):
            result = []
            if self._secret_prefix_turn == 1:
                result.append('> ')
            else:
                result.append('  ')
            for i in range(0, self._secret_prefix_board.pits + 1):
                result.append('%2d ' % self._secret_prefix_seeds[self._secret_prefix_board.size - 1 - i])
            result.append('   ')
            result.append('\n')
            if self._secret_prefix_turn == 0:
                result.append('>    ')
            else:
                result.append('     ')
            for i in range(0, self._secret_prefix_board.pits + 1):
                result.append('%2d ' % self._secret_prefix_seeds[i])
            result.append('\n')
            result.append('%d %d' % (self._secret_prefix_seeds_left[0], self._secret_prefix_seeds_left[1]))
            return "".join(result)

        def __repr__(self):
            return '%r %r %r' % (self._secret_prefix_seeds, self._secret_prefix_seeds_left, self._secret_prefix_turn)
        
        def _compute_hash(self):
            self.hash = 0
            for x in self._secret_prefix_seeds:
                self.hash = self.hash * 37 + x # should probably truncate this
            self.hash = self.hash * 2 + self._secret_prefix_turn
        
        def __hash__(self):
            return self.hash

        def __eq__(self, other):
            return self._secret_prefix_seeds == other._secret_prefix_seeds and self._secret_prefix_turn == other._secret_prefix_turn and self._secret_prefix_board is other._secret_prefix_board
