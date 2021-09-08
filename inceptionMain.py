
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

""" Draw large letters for the shell-tic-tac-toe wins """    
def draw_shellLetters(screen, shellBoard):
    # all dimensions / sizes must be multiplied by 3
    # to fit the shell squares
    Sqs = square_size * 3 # note capitalizes S for shell square size etc
    Sq2 = Sqs // 2
    Circle_rad = circle_radius * 4
    field = space * 3.5
    Cross_w = cross_width * 3
    Circle_w = circle_width * 3
    cross_color = p.Color("blue")
    circle_color = p.Color("Blue")

    # not draw figures on shell board
    for r in range(len(shellBoard[:,0])):
        for c in range(len(shellBoard[0,:])):

            if shellBoard[r,c] == "o":
                p.draw.circle(screen, circle_color, (int(c*Sqs+Sq2), int(r*Sqs+Sq2)), 
                Circle_rad, Circle_w)

            elif shellBoard[r,c] == "x":
                p.draw.line(screen, cross_color, (c*Sqs+field, r*Sqs+Sqs-field), 
                (c*Sqs+Sqs-field, r*Sqs+field), Cross_w)
                p.draw.line(screen, cross_color, (c*Sqs+field, r*Sqs+field),
                (c*Sqs+Sqs-field, r*Sqs+Sqs-field), Cross_w)
    
""" Draw winning lines if the game is over """
def draw_winLines(screen, shellBoard):

    Sqs = square_size * 3 # note capitalizes S for shell square size etc
    Sq2 = Sqs // 2
    color = p.Color("blue")
    win_width = circle_width * 3

    # horizontal winning line
    for row in range(3):
            if shellBoard[row,0] == shellBoard[row,1] and \
            shellBoard[row,0] == shellBoard[row,2] and shellBoard[row,0] != "-":
                Y = row * Sqs + Sq2 # position Y
                p.draw.line(screen, color, (win_width, Y), (width-win_width, Y), win_width)
                break
    # vertical winning line
    for col in range(3):
            if shellBoard[0,col] == shellBoard[1,col] and \
            shellBoard[0,col] == shellBoard[2,col] and shellBoard[0,col] != "-":
                X = col * Sqs + Sq2 # position X
                p.draw.line(screen, color, (X, win_width), (X, width-win_width), win_width)
                break
    # Diagonal winning line - Top Left to Bottom Right
    if shellBoard[0,0] == shellBoard[1,1] and \
    shellBoard[0,0] == shellBoard[2,2] and shellBoard[0,0] != "-":
        p.draw.line(screen, color , (width-win_width, height-win_width), (win_width, win_width), win_width)
        
    # Diagonal winning line - Bottom Left to Top Right
    if shellBoard[2,0] == shellBoard[1,1] and \
    shellBoard[1,1] == shellBoard[0,2] and shellBoard[1,1] != "-":
        p.draw.line(screen, color , (win_width, height-win_width), (width-win_width, win_width), win_width)


    



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
                                print("local winner is player: " + player)
                         # append move to moveLog
                        gs.moveLog.append((row,col))
                        # update player only if valid move made
                        if player == "o":
                            player = "x"
                        else:
                            player = "o"
                        # check if game is over now
                        gameOver = gs.checkGameOver() #GAME OVER
                        if gameOver: 
                            print("GAME OVER!!")
                        # get new valid squares
                        validSquares = gs.getValidSquares()
            
            # key event handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # 'z' Key to undo move
                    gs.undoMove()
                    # switch players
                    if player == "o":
                        player = "x"
                    else:
                        player = "o"
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




