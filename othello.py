import numpy
import tkinter as tk

game = numpy.zeros((8, 8))
game[3][3] =  1
game[4][4] =  1
game[3][4] = -1
game[4][3] = -1


# dr \ dc  | -1   |  0   |  1
#------------------------------
# -1       | (2,4)| (2,5)| (2,6)
# 0        | (3,4)| (3,5)| (3,6)
# 1        | (4,4)| (4,5)| (4,6)

def nextgame(game, row, clm, Player):
    if game[row][clm] == 0:
        for d in range(9):
            dc =int(d/3)-1
            dr =d/3 - 1
            length = 0
            while True:
                length += 1
                if row + dr*length < 0 or row + dc*length >7 or clm + dc*length




        