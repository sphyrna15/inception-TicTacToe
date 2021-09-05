
"""
Inception Tic-Tac-Toe 

Main Driver and Pygame graphics, user input etc.
"""

''' Define global variables '''

width = 600
height = 600 
line_width = 15
win_line_width = 5

# Number of rows and collumns
nrows = 3
ncols = 3

square_size = 200

# figure dimensions
circle_radius = 60
circle_width = 25
cross_width = 25
space = 55

# set color scheme
red = (225, 0, 0)
bg_color = (20, 200, 160)
line_color = (239, 231, 200)
circle_color = (239, 231, 200)
cross_color = (66, 66, 66)

""" draw horizontal and vertical lines to divide up board in n by n grid """
def draw_lines(screen): #draw lines on display
    n = 3 # produce n by n grid
    # Vertical Lines
    vert = int(width / n)
    for i in range(1, n+1):
        p.draw.line(screen, line_color, (vert*i, 0), (vert*i, height), line_width)
    
    # Horizontal Lines
    horz = int(height / n)
    for i in range(1, n+1):
        p.draw.line(screen , line_color, (0, horz*i), (width, horz*i), line_width)
