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
