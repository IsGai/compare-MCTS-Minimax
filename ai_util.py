from games import game
from itertools import permutations

class TicTacToe3D(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=4, v=4, p=4, k=4, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h = h
        self.v = v
        self.z = z
        self.p = p
        moves = [(x, y, z) for x in range(1, self.h + 1) for y in range(1, self.v + 1) for z in range (1, self.p +1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for y in range(self.v, 0, -1):
            for x in range(1, self.h + 1):
                for z in range (1, self.p +1):
                    print(board.get((x, y, z), '.'), end=' ')
                print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        x, y, z = move
        n = 0
        ways_to_check = [
            (1, 0, 1),
            (1, 1, 0),
            (0, 1, 1),
            (1, 1, 1),
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, -1),
            (1, -1, 0),
            (0, 1, -1),
            (1, -1, 1),
            (1, 1, -1),
            (-1, 1, 1)
        ]

        for way in ways_to_check:
             if four_in_row(self, board, move, player, way):
                 return True
        return False


 

    def four_in_row(self, board, move, player, delta_x_y_z):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y, delta_z) = delta_x_y_z
        x, y, z = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y, z = x + delta_x, y + delta_y, z + delta_z
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y, z - delta_z
        n -= 1  # Because we counted move itself twice
        return n >= 4

    #  def string_to_state(self, string, to_move):
    #     string = string.strip()
    #     board = {}
    #     y = self.v
    #     x = 1
    #     for s in range(len(string)):
    #         if string[s] in [" ", "\n", "\t"]: continue
    #         char = string[s]
    #         pos = (x,y)
    #         if char == ".":
    #             pass
    #         else:
    #             board[pos] = char
    #         x += 1
    #         if (x - 1) % self.h == 0:
    #             x = 1
    #             y -= 1
    #     moves = self.initial.moves[:]
    #     for key in board:
    #         moves.remove(key)
    #     return GameState(board=board, to_move=to_move, utility=0, moves=moves)