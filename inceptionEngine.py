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

        self.moveLog = []

    """ Will return a list of available squares """
    def getFreeSquares(self):
        return np.where(self.board == "-")