import cs210_utils
from utils import Struct
from games import Game

class MancalaGame(Game):
    """
    Manacala Game class and functions
    """

    #Constants
    P0 = 0
    P1 = 1
    P0_mancala = 6
    P1_mancala = 13
    P0_start = 0
    P1_start = 7
    Num_Piece = 4

    def __init__(self):
        #Create a list of 14 elements with number of pieces
        self.board = [self.Num_Piece] * 14
        #Set Players' macalas to 0
        self.board[self.P0_mancala] = 0
        self.board[self.P1_mancala] = 0
        self.moves = [0, 1, 2, 3, 4, 5]
        self.start = Struct(to_move = self.P0, utility = 0, board = self.board, moves = self.moves)

    def legal_moves(self, state):
        """Return a list of the allowable moves at this point. A state represents the number of stones in each pit on the board."""
        return state.moves 

    def make_move(self, move, state):
        """Return the state that results from making a move from a state. For Mancala, a move is an integer in the range 0 to 5, inclusive."""
        if move not in state.moves:
            return state

        board = state.board.copy()

        to_move = self.to_move(state)

        #Whose turn is this
        if to_move == self.P0:
            P_start = self.P0_start
            P_mancala = self.P0_mancala
        else:
            P_start = self.P1_start
            P_mancala = self.P1_mancala

        #number of pieces to move
        position = P_start + move
        num_move = board[position]

        #make a move
        board[position] = 0
        while num_move > 0:
            if position > 12:
                position = 0
            else:
                position += 1
            if position == 13 and to_move == self.P0:
                position = 0
            elif position == 6 and to_move == self.P1:
                position += 1
            board[position] += 1
            num_move -= 1

        #if land on empty slot on the player's side, capture opponent's pieces on the other side
        if position != 13 and position != 6:
            if board[position] == 1 and position//7 == to_move and board[12 - position] != 0:
                board[P_mancala] += board[position] 
                board[P_mancala] += board[12 - position]
                board[position] = 0
                board[12 - position] = 0
            to_move = 1 - to_move

        #prepare new state
        moves = []
        utility = 0
        if to_move == self.P0:
            for i in range(self.P0_start, self.P0_mancala):
                if board[i] != 0:
                    moves.append(i)
                    utility = board[self.P0_mancala]
        else:
            for i in range(self.P1_start, self.P1_mancala):
                if board[i] != 0:
                    moves.append(i - 7)
            utility = board[self.P1_mancala]
        return Struct(to_move = to_move, utility = utility, board = board, moves = moves)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        val = 0
       	if player == self.P0:
        	for i in range (self.P0_start, self.P0_mancala + 1):
        		val += state.board[i]
       	else:
        	for i in range (self.P1_start, self.P1_mancala + 1):
        		val += state.board[i]
       	return val    

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        end = True
        if state.to_move == self.P0:
            for i in range(self.P1_start, self.P1_mancala):
                if state.board[i] != 0:
                    end = False
                    break
        else:
            for i in range(self.P0_start, self.P0_mancala):
                if state.board[i] != 0:
                    end = False
                    break            
        return state.moves == [] or end

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        board = state.board
        for i in range(self.P0_start, self.P0_mancala + 1):
            if i == 0:
                print(" ", board[13])
                print(board[i], " - ", board[12 - i])
            elif i == 6:
                print(" ", board[i])
            else:
                print(board[i], " - ", board[12 - i])
        print("\n")

    def eval(self, state):
        return state.utility*(1 - 2 * state.to_move)