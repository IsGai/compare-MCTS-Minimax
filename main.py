import aima3
from aima3.mcts import MCTS, Node, softmax, np
import itertools
import functools
import copy
from aima3.games import Game, GameState, Player, MCTSPlayer, MiniMaxPlayer, HumanPlayer, RandomPlayer, AlphaBetaPlayer, TicTacToe, AlphaBetaCutoffPlayer, alphabeta_cutoff_search

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
        #print("move: ")
        #print(move)
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


class MinimaxBenchmarkPlayer(Player):
    COUNT = 0
    def get_action(self, state, turn=1, verbose=0):
        a = alphabeta_cutoff_search(state, self.game, d=4,
                                       cutoff_test=None, eval_fn=None)
        return a


class HybridPlayer(Player):
    """
    AI player based on MCTS
    Use higher temp for exploring the tree. Use is_selfplay=False
    for best play.
    """
    COUNT = 0
    def __init__(self, name=None, n_playout=100, c_puct=5, is_selfplay=False, temp=0.5):
        super().__init__(name)
        self.n_playout = n_playout
        self.c_puct = c_puct
        self.is_selfplay = is_selfplay
        self.temp = temp

    def policy(self, game, state):
        """
        A function that takes in a board state and outputs a list of
        (action, probability) tuples and also a score in [-1, 1]
        (i.e. the expected value of the end game score from the
        current player's perspective) for the current player.
        """
        value = game.utility(state, game.to_move(state))
        actions = game.actions(state)
        if len(actions) == 0:
            result = [], value
        else:
            prob = 1/len(actions)
            result = [(action, prob) for action in actions], value
        return result

    def set_game(self, game):
        self.game = game
        self.mcts = MCTS(self.game, self.policy, self.c_puct, self.n_playout, self.temp)

    def get_action(self, state, turn=1, verbose=0, return_prob=0):
        sensible_moves = self.game.actions(state)
        all_moves = self.game.actions(self.game.initial)
        move_probs = {key: 0.0 for key in all_moves} # the pi vector returned by MCTS as in the alphaGo Zero paper
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move_probs(state)
            move_probs.update({key: val for (key,val) in zip(acts, probs)})
            if self.is_selfplay:
                # add Dirichlet Noise for exploration (needed for self-play training)
                move_index = np.random.choice(range(len(acts)), p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs))))
                move = acts[move_index]
                self.mcts.update_with_move(move) # update the root node and reuse the search tree
            else:
                if verbose >= 3:
                    for i in range(len(acts)):
                        print("%7s" % (acts[i],), end=" | ")
                    print()
                    for i in range(len(probs)):
                        print("%7.2f" % (probs[i],), end=" | ")
                    print()
                for prob in probs:
                    if prob > 0.04:
                        return alphabeta_cutoff_search(state, self.game, d=4,
                                       cutoff_test=None, eval_fn=None)
                move_index = np.argmax(probs)
                #move_index = np.random.choice(range(len(acts)), p=probs)
                move = acts[move_index]
                # reset the root node
                self.mcts.update_with_move(-1)
            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)

def main():
    game = TicTacToe3D()
    players = [HybridPlayer(), AlphaBetaCutoffPlayer()]
    players2 = [MCTSPlayer(), RandomPlayer()]
    game.play_game(*players)
main()
