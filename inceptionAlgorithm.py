"""
Inception Tic-Tac-Toe 

Algorithm which can return the best possible move
"""

import numpy as np
import inceptionEngine
import random

class Brain():

    """ Simply returns a random valid square to play """
    def chooseRandom(self, validSquares):
        return random.choice(validSquares)

    """ crude minimax implementation from wikipedia """
    def minimax(self, gameState, player, maximizer):

        # if the game is over, assign value
        if gameState.checkGameOver():
            # draw??
            if gameState.getFreeSquares == []:
                return 0
            else:
                # maximizer won
                if player != maximizer:
                    return 10
                # maximizer lost
                elif player == maximizer:
                    return -10
        
        # Otherwise, enter recursions to check moves:
        if player == maximizer: #maximizing player
            value = -100
            validSquares = gameState.getValidSquares()
            # do all possible moves
            for move in validSquares:
                gameState.makeMove(move, player) # make move
                # get minimax value recursion
                if maximizer == "x":
                    minmax = self.minimax(gameState, "o", maximizer)
                else:
                    minmax = self.minimax(gameState, "x", maximizer)
                gameState.undoMove() # undo the move
                # chosse value to maximize position
                value = max(value, minmax)
            return value
        else: # minimizing player
            value = +100
            validSquares = gameState.getValidSquares()
            # do all possible moves
            for move in validSquares:
                gameState.makeMove(move, player) # make move
                # get minimax value recursion
                if maximizer == "x":
                    minmax = self.minimax(gameState, "x", maximizer)
                else:
                    minmax = self.minimax(gameState, "o", maximizer)
                gameState.undoMove() # undo the move
                # chosse value to maximize position
                value = min(value, minmax)
            return value

