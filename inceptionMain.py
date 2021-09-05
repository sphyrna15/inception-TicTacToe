
"""
Inception Tic-Tac-Toe 

Main Driver and Pygame graphics, user input etc.
"""

import pygame as p
import numpy as np
import inceptionEngine

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

""" draw horizontal and vertical lines to divide up board in n by n grid """
def draw_lines(screen): #draw lines on display
    n = 9 # produce n by n grid
    # Vertical Lines
    vert = int(width / n)
    for i in range(1, n+1):
        color = line_color
        p.draw.line(screen, color, (vert*i, 0), (vert*i, height), line_width)
    
    # Horizontal Lines
    horz = int(height / n)
    for i in range(1, n+1):
        color = line_color
        p.draw.line(screen , color, (0, horz*i), (width, horz*i), line_width)

    # Black Vertical Lines
    for i in range(1, 4):
        color = (0, 0, 0)
        p.draw.line(screen, color, (vert*3*i, 0), (vert*3*i, height), line_width)
    # Horizontal Black Lines
    for i in range(1, 4):
        color = (0, 0, 0)
        p.draw.line(screen , color, (0, horz*3*i), (width, horz*3*i), line_width)

""" Draw letters in correct squares """
def draw_letters(screen, board):

    sqs = square_size
    sq2 = sqs // 2

    for r in range(len(board[:,0])):
        for c in range(len(board[0,:])):

            if board[r,c] == "o":
                p.draw.circle(screen, circle_color, (int(c*sqs+sq2), int(r*sqs+sq2)), 
                circle_radius, circle_width)

            elif board[r,c] == "x":
                p.draw.line(screen, cross_color, (c*sqs+space, r*sqs+sqs-space), 
                (c*sqs+sqs-space, r*sqs+space), cross_width)
                p.draw.line(screen, cross_color, (c*sqs+space, r*sqs+space),
                (c*sqs+sqs-space, r*sqs+sqs-space), cross_width)
    


"""
Main Driver to handle user input and update graphics 
"""

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
    selected_sq = () # no square selected initially, tuple (row, col)
    player = "o"
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
                        # Check if the sub-ttt has now a winner
                        if gs.moveLog != []:
                            if gs.checkSubWin(gs.moveLog[-1]): #if yes, update shell-ttt
                                last_row = gs.moveLog[-1][0] ; last_col = gs.moveLog[-1][1]
                                gs.shellBoard[last_row%3, last_col%3] = player
                                print("local winner is player: " + player)
                        # check if game is over now
                        gameOver = gs.checkGameOver() #GAME OVER
                        # append move to moveLog
                        gs.moveLog.append((row,col))
                        # update player only if valid move made
                        if player == "o":
                            player = "x"
                        else:
                            player = "o"
                        # get new valid squares
                        validSquares = gs.getValidSquares()
        
         
        draw_letters(screen, gs.board)    
        p.display.update()





if __name__ == "__main__":
    main()




