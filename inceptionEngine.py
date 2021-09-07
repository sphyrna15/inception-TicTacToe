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

        # Track who wins the sub-tic-tac-toes
        self.shellBoard = np.array([
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"]]
        )
        # Temporary 3by3 board to check if a sub-ttt has a winner (see checkSubWin())
        self.tempBoard = np.array([
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
                 # note that sub-ttt's with a subwinner have no free squares anymore
                subloc = self.findSubLocation(r, c)
                if self.board[r, c] == "-" and self.shellBoard[subloc[0], subloc[1]] == "-":
                    freeSquares.append((r,c))
        return freeSquares
    
    """ 
    determine which sub-tic-tac-toe and index is located in 
    Not required as long as we set all taken sub-ttt squares to value "t"
    """
    def findSubLocation(self, row, col):
        for subrow in range(3):
            for subcol in range(3):
                for pos in self.sub_indices[subrow, subcol]:
                    if pos[0] == row and pos[1] == col:
                        return (subrow, subcol)

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
        # If the dictated sub-ttt is full, return all free squares
        if validSquares == []: 
            return freeSquares
        # Otherwise, return valid squares
        return validSquares

    """
    Function to Undo the previouse move
    """
    def undoMove(self):
        postSubWins = self.findSubWins() # Nr. of sub-wins post move
        # remove move from log
        lastSquare = self.moveLog.pop()
        self.board[lastSquare[0], lastSquare[1]] = "-"
        # check if last move scored a sub-win
        preSubWins = self.findSubWins() # Nr. of sub-wins pre move
        if len(postSubWins) == len(preSubWins) + 1: # move scored a subwin
            #remove that sub-win
            for win in postSubWins:
                if win not in preSubWins:
                    self.shellBoard[win[0], win[1]] = "-"





    """ 
    Check if someone has won the game overall (shell tic-tac-toe winner) 
    or if there are no squares left
    """
    def checkGameOver(self):

        # If there are nomore squares left, return GameOver
        if self.getFreeSquares() == []:
            return True
        else:
            return self.checkWin(self.shellBoard)

    """ Check if a tic-tac-toe cofiguration has a winner """
    def checkWin(self, board):
        # Vertical Win 
        for col in range(3):
            if board[0,col] == board[1,col] and board[0,col] == board[2,col] and board[0,col] != "-":
                return True
        # Horizontal Win
        for row in range(3):
            if board[row,0] == board[row,1] and board[row,0] == board[row,2] and board[row,0] != "-":
                return True
        # Diagonal Win - Top Left to Bottom Right
        if board[0,0] == board[1,1] and board[0,0] == board[2,2] and board[0,0] != "-":
            return True
        # Diagonal Win - Bottom Left to Top Right
        if board[2,0] == board[1,1] and board[1,1] == board[0,2] and board[1,1] != "-":
            return True
        # No Winner
        return False
    
    """ 
    Find all indices where a sub-ttt has a winner
    This handles the edge case where the new winner does not follow a dictating move
    """
    def findSubWins(self):
        subWinners = []
        # iterate over all 9 fields to find subwinners
        for r in range(3):
            for c in range(3):
                for pos in self.sub_indices[r, c]:
                    row = pos[0] ; col = pos[1]
                    self.tempBoard[row%3, col%3] = self.board[row,col]
                # now check sub-ttt for win
                if self.checkWin(self.tempBoard):
                    subWinners.append((r,c))
        return subWinners


    """ 
    Check if current sub-tic-tac-toe has a winner 
    This Function is not currently used
    """
    def checkSubWin(self, dictatingMove): 
        #the dictating move determines the follow up sub-ttt
        # Find sub-tic-tac-toe index
        subrow = dictatingMove[0] % 3
        subcol = dictatingMove[1] % 3
        for pos in self.sub_indices[subrow, subcol]:
            r = pos[0] ; c = pos[1]
            self.tempBoard[r%3, c%3] = self.board[r,c]
        # Check if someone has won in this sub-ttt
        return self.checkWin(self.tempBoard)

        

        


