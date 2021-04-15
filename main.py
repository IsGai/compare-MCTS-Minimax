import aima3
from aima3.mcts import MCTS, Node, softmax, np
import itertools
import functools
import copy
from aima3.games import Game, GameState, Player, MCTSPlayer, MiniMaxPlayer, HumanPlayer, RandomPlayer, AlphaBetaPlayer, TicTacToe, AlphaBetaCutoffPlayer, alphabeta_cutoff_search
import csv
import time

def write_to_csv(filename, csv_columns, data):
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for i in data:
                writer.writerow(i)
    except IOError:
        print("I/O error")

def write_to_csv_l(filename, csv_columns, data):
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for i in data:
                writer.writerow(i)
    except IOError:
        print("I/O error")

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


class BenchmarkMCTSPlayer(MCTSPlayer):
    def get_action(self, state, turn=1, verbose=0, return_prob=0):
        t1 = time.time()
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
                move_index = np.argmax(probs)
                #move_index = np.random.choice(range(len(acts)), p=probs)
                move = acts[move_index]
                # reset the root node
                self.mcts.update_with_move(-1)
            if return_prob:
                t2 = time.time()
                MCTSTimeBenchmark.append(t2 - t1) 
                return move, move_probs
            else:
                t2 = time.time()
                MCTSTimeBenchmark.append(t2 - t1) 
                return move
        else:
            print("WARNING: the board is full")

class MinimaxBenchmarkPlayer(Player):
    COUNT = 0
    def get_action(self, state, turn=1, verbose=0):
        t1 = time.time()
        a = alphabeta_cutoff_search(state, self.game, d=4,
                                       cutoff_test=None, eval_fn=None)
        t2 = time.time()
        minimaxTimeBenchmark.append(t2 - t1) 
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
        t1 = time.time()
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
                        a = alphabeta_cutoff_search(state, self.game, d=4,
                                       cutoff_test=None, eval_fn=None)
                        t2 = time.time()
                        hybridTimeBenchmark.append(t2 - t1) 
                        return a
                move_index = np.argmax(probs)
                #move_index = np.random.choice(range(len(acts)), p=probs)
                move = acts[move_index]
                # reset the root node
                self.mcts.update_with_move(-1)
            if return_prob:
                t2 = time.time()
                hybridTimeBenchmark.append(t2 - t1) 
                return move, move_probs
            else:
                t2 = time.time()
                hybridTimeBenchmark.append(t2 - t1) 
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)

def main():
    game = TicTacToe3D()
    
    # Minimax vs. MCTS
    mcts_vs_mini = {}
    data1 = []
    for i in range(0):
        players = [MinimaxBenchmarkPlayer(), BenchmarkMCTSPlayer()]
        retval = game.play_game(*players)
        if retval[0] not in mcts_vs_mini:
            mcts_vs_mini[retval[0]] = 1
        else:
            mcts_vs_mini[retval] += 1

    # write w/l results to csv
    csv_file = "Minimax vs MCTS.csv"
    csv_columns = list(mcts_vs_mini.keys())
    data1.append(mcts_vs_mini)
    write_to_csv(csv_file, csv_columns, data1)

    # Minimax vs. Hybrid
    mini_vs_hybrid = {}
    data2 = []
    for j in range(0):
        players = [MinimaxBenchmarkPlayer(), HybridPlayer()]
        retval = game.play_game(*players)
        if retval[0] not in mini_vs_hybrid:
            mini_vs_hybrid[retval[0]] = 1
        else:
            mini_vs_hybrid[retval] += 1

    # write w/l results to csv
    csv_file = "Minimax vs Hybrid.csv"
    csv_columns = list(mini_vs_hybrid.keys())
    data2.append(mini_vs_hybrid)
    write_to_csv(csv_file, csv_columns, data2)

    # MCTS vs. Hybrid
    mcts_vs_hybrid = {}
    data3 = []
    for k in range(1):
        players = [HybridPlayer(), BenchmarkMCTSPlayer()]
        retval = game.play_game(*players)
        if retval[0] not in mcts_vs_hybrid:
            mcts_vs_hybrid[retval[0]] = 1
        else:
            mcts_vs_hybrid[retval] += 1

    # write w/l results to csv
    csv_file = "MCTS vs Hybrid.csv"
    csv_columns = list(mcts_vs_hybrid.keys())
    data3.append(mcts_vs_hybrid)
    write_to_csv(csv_file, csv_columns, data3)

    # write runtimes to csv
    csv_file ="Runtimes.csv"
    csv_columns = ["Minimax" , "MCTS", "Hybrid"]
    runtime_list = []
    for i in range(len(minimaxTimeBenchmark)):
        runtime_list.append([minimaxTimeBenchmark[i], MCTSTimeBenchmark[i], hybridTimeBenchmark[i]])
    write_to_csv_l(csv_file , csv_columns)

    

    #players = [BenchmarkMCTSPlayer(), BenchmarkMCTSPlayer()]
    #game.play_game(*players)
minimaxTimeBenchmark = []
MCTSTimeBenchmark = []
hybridTimeBenchmark = []
main()
