"""
Inception Tic-Tac-Toe 

Driver to Play against Computer program
"""

import pygame as p
import numpy as np
import time
import inceptionEngine
import inceptionAlgorithm

# Import modules
from inceptionMain import draw_lines
from inceptionMain import draw_letters
from inceptionMain import draw_shellLetters
from inceptionMain import draw_winLines


""" define Brain object from alroithm library """

brain = inceptionAlgorithm.Brain()

''' Define global variables '''

width = 900
height = 900 
line_width = 10
win_line_width = 5

# Number of rows and collumns
nrows = 3
ncols = 3

square_size = 100

# figure dimensions
circle_radius = 30
circle_width = 5
cross_width = 7
space = 75

# set color scheme
red = (225, 0, 0)
bg_color = (20, 200, 160)
line_color = (23, 145, 135)
circle_color = (239, 231, 200)
cross_color = circle_color #p.Color("white") #(66, 66, 66)


def main():

    p.init()
    screen = p.display.set_mode((width, height))
    p.display.set_caption("Inception TIC TAC TOE")
    clock = p.time.Clock()
    screen.fill(bg_color)
    draw_lines(screen)

    gs = inceptionEngine.GameState() #initialize game state

    running = True
    gameOver = False # Game is over flag
    validSquares = gs.getValidSquares()
    player = "x"
    while running: 
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
            
            # mouse event handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #(x,y) coordinates of mouse
                    col = location[0] // square_size # // double divide to get integers
                    row = location[1] // square_size
                    # check if square is free
                    if (row,col) in validSquares:
                        gs.board[row, col] = player # Add symbol
                        # Find all the Sub-ttt winners
                        for subWin in gs.findSubWins(): 
                            # if the winner is not yet noted, update shellBoard
                            if gs.shellBoard[subWin[0], subWin[1]] == "-":
                                gs.shellBoard[subWin[0], subWin[1]] = player
                                print("you have won a local square")
                         # append move to moveLog
                        gs.moveLog.append((row,col))
                        # draw letters for time delay
                        draw_letters(screen, gs.board)
                        p.display.update()

                        """ if valid move was made, let computer choose a move """
                        # switch players
                        if player == "o":
                            player = "x"
                        else:
                            player = "o"
                        validSquares = gs.getValidSquares()

                        move = brain.chooseRandom(validSquares)
                        time.sleep(2)

                        gs.board[move[0], move[1]] = player # Add symbol
                        # switch back players
                        if player == "o":
                            player = "x"
                        else:
                            player = "o"
                        # Find all the Sub-ttt winners
                        for subWin in gs.findSubWins(): 
                            # if the winner is not yet noted, update shellBoard
                            if gs.shellBoard[subWin[0], subWin[1]] == "-":
                                gs.shellBoard[subWin[0], subWin[1]] = player
                                print("the computer has won a local square")
                         # append move to moveLog
                        gs.moveLog.append(move)
                        
                        # check if game is over now
                        gameOver = gs.checkGameOver() #GAME OVER
                        if gameOver: 
                            print("GAME OVER!!")
                        # get new valid squares
                        validSquares = gs.getValidSquares()
            
            # key event handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # 'z' Key to undo move
                    # undo 2 moves, player + AI move
                    gs.undoMove()
                    gs.undoMove()
                    validSquares = gs.getValidSquares()
                    gameOver = False
                if e.key == p.K_r: # resets the board with 'r' Key
                    gs = inceptionEngine.GameState() # re-initialize game state
                    validSquares = gs.getValidSquares()
                    player = "x"
                    gameOver = False
        
        screen.fill(bg_color)
        draw_lines(screen)
        draw_letters(screen, gs.board)
        draw_shellLetters(screen, gs.shellBoard) 
        if gameOver:
            draw_winLines(screen, gs.shellBoard)  
        p.display.update()





if __name__ == "__main__":
    main()