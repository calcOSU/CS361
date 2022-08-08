# Author: Charles Cal
# Date: 7/12/2022
# Description:

import Checkers
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import datetime
import json

game = Checkers.Checkers()
root = tk.Tk()


def make_a_move():
    """The function to be invoked when clicking on a game grid square"""
    pass

def show(grid):
    """
    A function to show the current item in a given grid square
    :param grid:
    :return:
    """
    if game.board[grid[0]][grid[1]]:
        return game.board[grid[0]][grid[1]]
    else:
        return ""

source = 0,0
first_move = True
def makeSelection(row,col):
    global first_move
    global source
    if first_move == True:
        source = row,col
        first_move = False
    else:
        destination = row,co
        first_move = True
        game.move(source,destination)

board = ttk.LabelFrame(root, text = 'make a move')
grid_list = []
for row in range(8):
    row_list = []
    for col in range(8):
        button = ttk.Button(board,text=f'{show((row,col))}', padding = 5, command = lambda: makeSelection(row,col))
        if (row+col) % 2 == 1:
            button.state(['disabled']) # something to highlight 'checkered' squares
        button.grid(row = row, column=col)
        row_list.append(button)
    grid_list.append(row_list)

board.grid()
root.mainloop()
