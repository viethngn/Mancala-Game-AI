
##############################################################################
#
# File:         games.py
# Date:         Thu  6 Oct 2011  15:37
# Author:       Ken Basye
# Description: Game search and game support (borrowed heavily from AIMA Python
# package)
#
##############################################################################


"""
Games, or Adversarial Search

"""
from utils import Struct, infinity
import random 
import cs210_utils

#______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s))
        return v

    # Body of minimax_decision starts here:
    action, state = argmax(game.successors(state),
                           lambda a, s: min_value(s))
    return action


#______________________________________________________________________________
    
def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_full_search starts here:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.legal_moves(state):
        # because we are assuming the root of the tree is a max node,
        # the first level of recursion is to min_value
        v = min_value(game.make_move(a, state), best_score, beta)
        if v > best_score:  # Here we do the maximizing for the root explicitly
            best_score = v
            best_action = a
    return best_action

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(game, state)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(game, state)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda game, state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.legal_moves(state):
        # because we are assuming the root of the tree is a max node,
        # the first level of recursion is to min_value
        v = min_value(game.make_move(a, state), best_score, beta, 1)
        if v > best_score:  # Here we do the maximizing for the root explicitly
            best_score = v
            best_action = a
    return best_action

#______________________________________________________________________________
# Players for Games

def query_player(game, state, display = True):
    "Make a move by querying standard input."
    if display: game.display(state)
    return num_or_str(input('Your move? '))

def query_player_py_exp(game, state, display=True):
    """
    Make a move by querying standard input. The input string is evaluated as a
    Python expression and returned
    """
    if display: game.display(state)
    return eval(input('Your move? '))

def random_player(game, state, display=True):
    "A player that chooses a legal move at random."
    if display: game.display(state)
    return random.choice(game.legal_moves(state))

def alphabeta_full_player(game, state, display=True):
    if display: game.display(state)
    return alphabeta_full_search(state, game)

def alphabeta_player(game, state, display=True):
    if display: game.display(state)
    return alphabeta_search(state, game)

def alphabeta_player2(game, state, eval_fn, display=True):
    if display: game.display(state)
    return alphabeta_search(state, game, eval_fn=eval_fn)

def play_game(game, named_players):
    """Play an n-person, move-alternating game.
    game is a Game instance;
    named_players is a tuple of pairs (player_name, player_function)
    player_functions take a game and a state and return a move to make (see above)

    >>> g0 = TicTacToe()
    >>> quiet_af_player = lambda g, s: alphabeta_full_player(g, s, False)
    >>> players = (('X', quiet_af_player), ('O', quiet_af_player))
    >>> play_game(g0, players)
    Game over - last move was by player X
    XXO
    OOX
    XOX
    Player X has utility: 0
    Player O has utility: 0
    """

    state = game.initial
    game_over = False
    while not game_over:
        for named_player in named_players:
            player_name, player_function = named_player
            move = player_function(game, state)
            state = game.make_move(move, state)
            if game.terminal_test(state):
                print
                print("Game over - last move was by player %s" % (player_name,))
                game.display(state)
                game_over = True
                break # for loop

    # Announce results
    for named_player in named_players:
        player_name, player_function = named_player
        print("Player %s has utility: %s" % (player_name, game.utility(state, player_name)))


def play_game2(game, named_players):
    """Play an n-person game where moves don't have to alternate.
    game is a Game instance;
    named_players is a tuple of pairs (player_name, player_function)
    player_functions take a game and a state and return a move to make (see above)"""

    # TODO
    state = game.start
    game_over = False
    while not game_over:
        for named_player in named_players:
            player_name, player_function = named_player
            while state.to_move == player_name:
                move = player_function(game, state)
                state = game.make_move(move, state)                
                if game.terminal_test(state):
                    print
                    print("Game over - last move was by player %s" % (player_name,))
                    game.display(state)
                    game_over = True
                    break
            if game_over:
                break

    # Announce results
    results = {}
    for named_player in named_players:
        player_name, player_function = named_player
        results[player_name] = game.utility(state, player_name)
    return results


#______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        abstract
            
    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def eval(self, state):
        "Return the minimax value for a given state"
        abstract

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=3, v=3, k=3):
        self.__dict__.update(h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def make_move(self, move, state):
        if move not in state.moves:
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.to_move
        moves = list(state.moves); moves.remove(move)
        return Struct(to_move= ('O' if state.to_move == 'X' else 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        if player == 'X':
            return state.utility
        else:
            assert player == 'O'
            return -state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(board.get((x, y), '_'), end="")
            print()

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return  +1 if player == 'X' else -1 
        else:
            return 0

    def k_in_row(self, board, move, player, deltas):
        delta_x, delta_y = deltas
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""
    
    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return [(x, y) for (x, y) in state.moves
                if y == 0 or (x, y-1) in state.board]


if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()
