"""
Inception Tic-Tac-Toe

GameState Engine, update moves, determine winner
"""

import numpy as np

class GameState():
    def __init__(self): 

        self.board = np.array([
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"], 
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-"]]
        )

        self.shellBoard = np.array([
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"]]
        )

        # list all valid indices for each of the 9 sub Tic-Tac-Toes
        self.idx00 = np.array([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)])
        self.idx10 = np.array([(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)])
        self.idx20 = np.array([(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)])
        self.idx01 = np.array([(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)])
        self.idx11 = np.array([(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)])
        self.idx21 = np.array([(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)])
        self.idx02 = np.array([(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)])
        self.idx12 = np.array([(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)])
        self.idx22 = np.array([(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)])

        # array of indicies for each sub-tic-tac-toe
        self.sub_indices = np.array([[self.idx00, self.idx01, self.idx02],
        [self.idx10, self.idx11, self.idx12], [self.idx20, self.idx21, self.idx22]])

        self.moveLog = []

    """ Will return a list of available squares """
    def getFreeSquares(self):
        freeSquares = []
        for r in range(9):
            for c in range(9):
                if self.board[r, c] == "-":
                    freeSquares.append((r,c))
        return freeSquares

    """
    Will Return all Squares which can be picked by next player 
    The next move must always be palced in the sub-tic-tac-toe 
    corresponding to the index of the last move modulo 3
    """
    def getValidSquares(self):
        validSquares = []
        freeSquares = self.getFreeSquares()
        # If no moves have been played yet, return all free squares
        if self.moveLog == []:
            return freeSquares
        # get last move
        lastMove = self.moveLog[-1]
        # row,col in current sub tic-tac-toe where last move was made
        last_row = lastMove[0] % 3
        last_col = lastMove[1] % 3
        # if the dictated sub-ttt has already been won, allow all free squares
        if self.shellBoard[last_row, last_col] != "-":
            return freeSquares
        # return all indices which are free and located in dictated sub-ttt
        for pos in freeSquares:
            for i in range(9):
                loc = self.sub_indices[last_row, last_col][i]
                if loc[0] == pos[0] and loc[1] == pos[1]:
                    validSquares.append(pos)
        return validSquares

