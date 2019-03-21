Name: Viet H. Nguyen
ID: vienguyen
Class: CS210
Project#: 2
-------------------------------------------
The board is a 14-element array with each element is 4 except for the 6th and 13th element where the values are 0 to indicate the mancala of the 2 players. Moves are integers 0, 1, 2, 3, 4, 5.
The program has the following functions:
- to_move() to check whose turn is it
- legal_moves() to return all moves that can take from the current board state
- make_move() to make a move from the legal_moves list and return the new board state
- utility() to return the number of pieces the player owns with the current board state
- terminal_test() to check if this is the final board state
- display() to display the board state
-------------------------------------------
Setting d at 10 with size of 20 games, the game starts to take too long.
-------------------------------------------
With each cutoff depth limit, 20 matches are played:
d=4: Wins = 19, winrate = 0.95, average difference = 24.316.
d=5: Wins = 20, winrate = 1.0, average difference = 24.6.
d=6: Wins = 18, winrate = 0.90, average difference = 20.333.
d=7: Wins = 20, winrate = 1.0, average difference = 22.6.
d=8: Wins = 19, winrate = 0.95, average difference = 22.316.
-------------------------------------------

