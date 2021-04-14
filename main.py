import aima3
import itertools
import functools
from aima3.games import Game, GameState, Player, MCTSPlayer, MiniMaxPlayer, HumanPlayer, RandomPlayer

class TicTacToe3D(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        moves = [(x, y, z) for x in range(1, 5)
                 for y in range(1, 5)
                 for z in range(1, 5)]
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
        print(state.board)

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        deltas = list(itertools.combinations_with_replacement([-1,0,1],3))
        deltas.remove((0,0,0))
        checks = [self.four_in_row(board, move, player, d) for d in deltas]
        check = functools.reduce(lambda a,b: a or b, checks)
        if (check):
            return +1 if player == 'X' else -1
        else:
            return 0

    def four_in_row(self, board, move, player, delta_x_y_z):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y, delta_z) = delta_x_y_z
        x, y, z = move
        n = 0  # n is number of moves in row
        while board.get((x, y, z)) == player:
            n += 1
            x, y, z = x + delta_x, y + delta_y, z + delta_z
        x, y, z = move
        while board.get((x, y, z)) == player:
            n += 1
            x, y, z = x - delta_x, y - delta_y, z - delta_z
        n -= 1  # Because we counted move itself twice
        return n >= 4

class HybridPlayer(Player):
    COUNT = 0
    def get_action(self, state, turn=1, verbose=0):
        """A player that chooses a legal move at random."""
        return random.choice(self.game.actions(state))

def main():
    game = TicTacToe3D()
    players = [MCTSPlayer(), MiniMaxPlayer()]
    players2 = [HumanPlayer(), RandomPlayer()]
    game.play_game(*players2)
main()
