##############################################################################
#
# File:         test1.py
# Date:         Thu  6 Oct 2011  15:39
# Author:       Ken Basye
# Description:  
#
##############################################################################

# Note no doctesting in this file; we want to run this as main to play

import games
import mancala

def test1():
    game = mancala.MancalaGame()
    named_players = ((0, games.query_player_py_exp), (1, games.random_player))
    result = games.play_game2(game, named_players)
    print(result)
    return result

def test2():
    game = mancala.MancalaGame()
    named_players = ((0, games.query_player_py_exp), (1, games.alphabeta_player))
    result = games.play_game2(game, named_players)
    print(result)
    return result

def test3():
    game = mancala.MancalaGame()
    named_players = ((0, games.alphabeta_player), (1, games.random_player))
    result = games.play_game2(game, named_players)
    print(result)
    return result

def test4():
    game = mancala.MancalaGame()
    named_players = ((0, games.alphabeta_full_player), (1, games.alphabeta_player))
    result = games.play_game2(game, named_players)
    print(result)
    return result

if __name__ == '__main__':
    num_match = 20
    win = 0
    dif = 0
    for i in range (0, num_match):
        result = test3()
        if result[0] > result[1]:
            win += 1
            dif += (result[0] - result[1])
    win_rate = win / num_match
    win_dif = dif/win
    print("alpha_beta wins: %s matches" % (win,))
    print("Winrate: %s" % (win_rate,))
    print("Average difference: %s" % (win_dif,))





