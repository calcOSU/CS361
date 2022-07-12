# Author: Charles Cal
# Date: 7/11/2022
# Description:
# ::todo:: mess between globals & parameters: make it class based?
import TicTacToe
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import datetime
import json

game = TicTacToe.TicTacToeGame()
root = tk.Tk()
root.title(f"{game.showTurn()}'s turn")
root.columnconfigure(1, weight=1)
turn_tracker = tk.Label(
    root, text = f"{game.showTurn()}'s turn",
    font=("TkDefaultFont",16)
)
turn_tracker.grid()


board = ttk.LabelFrame(
    root,
    text='Make a move'
)

# create styles for highlighted vs non-highlighted
s = ttk.Style()
s.configure('open.TButton', background= 'yellow', relief='raised')
s.configure('taken.TButton', background='gray', relief='flat')


def updateTitle():
    """
    Function to display whose turn it is in on the central label
    :return:
    """
    global root
    if gameUpdate():
        turn_tracker.config(text = f"{gameUpdate()}")
    else:
        turn_tracker.config(text = f"{game.showTurn()}'s turn")

def makeAMove(button, grid):
    """
    Callback function for selecting a tic tac toe grid item
    :param button:
    :param grid:
    :return:
    """
    game.move(grid)
    print(game)
    button['text'] = show(grid)
    button['style'] = 'taken.TButton'
    # button.state(['pressed'])

    print(gameUpdate())
    updateTitle()
    highlight_available_moves(button_list)

def display_comments():
    """An optional method to display encouraging comments in the log"""
    comments = ['Nice move', 'Wow!', 'No way they saw that coming!', 'Good thinking']
    pass

def display_message(text_box, your_message):
    """
    a message to display a string in the text box
    :param text_box:
    :param your_message:
    :return:
    """
    text_box['state'] = 'normal'
    text_box.insert('end', '\n\n')
    text_box.insert('end', str(your_message))
    text_box['state'] = 'disabled'


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

def gameUpdate():
    """
    Checks if the game has been won or tied
    :return:
    """
    if game.win_check() or game.tie_check():
        return game.win_check() or game.tie_check()

#definitions and placement for grid buttons
grid_00 = ttk.Button(board, text=f'{show((0,0))}', padding = 5, command = lambda: makeAMove(grid_00, (0,0)))
grid_01 = ttk.Button(board, text=f'{show((0,1))}', padding = 5, command = lambda: makeAMove(grid_01, (0,1)))
grid_02 = ttk.Button(board, text=f'{show((0,2))}', padding = 5, command = lambda: makeAMove(grid_02, (0,2)))
grid_10 = ttk.Button(board, text=f'{show((1,0))}', padding = 5, command = lambda: makeAMove(grid_10,(1,0)))
grid_11 = ttk.Button(board, text=f'{show((1,1))}', padding = 5, command = lambda: makeAMove(grid_11,(1,1)))
grid_12 = ttk.Button(board, text=f'{show((1,2))}', padding = 5, command = lambda: makeAMove(grid_12,(1,2)))
grid_20 = ttk.Button(board, text=f'{show((2,0))}', padding = 5, command = lambda: makeAMove(grid_20,(2,0)))
grid_21 = ttk.Button(board, text=f'{show((2,1))}', padding = 5, command = lambda: makeAMove(grid_21,(2,1)))
grid_22 = ttk.Button(board, text=f'{show((2,2))}', padding = 5, command = lambda: makeAMove(grid_22,(2,2)))
button_list = [grid_00, grid_01, grid_02, grid_10, grid_11, grid_12, grid_20, grid_21, grid_22]
grid_00.grid(row=0,column=0)
grid_01.grid(row=0,column=1)
grid_02.grid(row=0,column=2)
grid_10.grid(row=1,column=0)
grid_11.grid(row=1,column=1)
grid_12.grid(row=1,column=2)
grid_20.grid(row=2,column=0)
grid_21.grid(row=2,column=1)
grid_22.grid(row=2,column=2)
board.grid()

gameboard = ttk.Label(root, text='tic tac toef')

# for button in button_list:
#     button['style'] = 'open.TButton'

# Controls frame and associated buttons w/ callback functions
controls = ttk.LabelFrame(
    root,
    text='Options'
)

game_is_paused = False
def pause_game(button_list):
    """Callback function to 'pause' the game"""
    if game_is_paused:
        for button in button_list:
            button.state(['disabled'])
    else:
        for button in button_list:
            button.state(['!disabled'])

def highlight_message(button_list):
    """
    A method to display a simple method before highlighting open spaces
    :param button_list:
    :return:
    """
    global text_box
    text_box['state'] = 'normal'
    text_box.insert('end', '\n\n')
    if movesShown.get():
        text_box.insert('end', 'Showing available moves')
    else:
        text_box.insert('end', 'No longer showing available moves')
    text_box['state'] = 'disabled'
    highlight_available_moves(button_list)

def highlight_available_moves(button_list):
    """
    A method to highlight open buttons using styles
    :param button_list:
    :return:
    """
    for button in button_list:
        if movesShown.get():
            if button['text'] != '':
                button['style'] = 'taken.TButton'
            else:
                button['style'] = 'open.TButton'
        else:
            button['style'] = 'TButton'


def newGame():
    '''
    Callback function to clear the board and create a new game
    :return:
    '''
    rsp = messagebox.askyesno('Start a new game', 'Are you sure you want to start a new game?')
    if rsp:
        global game
        game = TicTacToe.TicTacToeGame()
        for button in button_list:
            button['text'] = ''
            button.state(['!pressed'])
        turn_tracker.config(text = f"{game.showTurn()}'s turn")
        highlight_available_moves(button_list)

def show_rules(text_box):
    """
    Callback function to display the rules of the game in a text box
    :param text_box:
    :return:
    """
    rules = """\n\n
    Rules of Tic Tac Toe:

    1. The game is played on a grid that's 3 squares by 3 squares.

    2. You are X, your friend (or the computer in this case) is O. Players take turns putting their marks in empty squares.

    3. The first player to get 3 of her marks in a row (up, down, across, or diagonally) is the winner.

    4. When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.
    https://www.exploratorium.edu/brain_explorer/tictactoe.html"""
    text_box['state'] = 'normal'
    text_box.insert('end', rules)
    text_box['state'] = 'disabled'

def save_game():
    """
    A function to save the game in a text file
    :return:

    https://tkdocs.com/tutorial/windows.html
    """
    # filename = filedialog.asksaveasfilename()
    if not os.path.isdir('saves'):
        os.mkdir('saves')

    now = datetime.datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    save_name = "saves\\TicTacToe " +dt_string+".json"
    print(save_name)
    global game
    export = game.export_game()
    with open(save_name, 'w') as f:
        json.dump(export,f)
    display_message(text_box,f'Saved game as {save_name}')

def load_game():
    """
    A function to load a previous saved game
    :return:
    """
    t = tk.Toplevel(root)
    saved_files = [x for x in os.listdir('saves') if x[-4:] == 'json']
    for save in saved_files:
        ttk.Button(t, text = save, command = lambda: open_game(save,t)).grid()


def open_game(file_name, window):
    rsp = messagebox.askyesno('Open saved game', 'Are you sure you want to open this save?')
    if rsp:
        with open('saves\\'+file_name) as f:
            import_game = json.load(f)
            game.import_game(import_game[1],import_game[0])
        grid_list = list()
        for x in range(3):
            for y in range(3):
                grid_list.append((x,y))
        for index, button in enumerate(button_list):
            button['text'] = f'{show(grid_list[index])}'
            print(show((1,0)))
        updateTitle()
        window.destroy()
        display_message(text_box, f'loaded game {file_name}')

def forfeit_game():
    rsp = messagebox.askyesno('Forfeit', 'Are you sure you want to forfeit? You\'ll lose the game!')
    if rsp:
        winner = "X" if game.showTurn() == 'O' else 'O'
        turn_tracker.config(text=f"{winner} wins!")


controls.columnconfigure(1, weight=1)
undo_button = ttk.Button(controls, text='Undo').grid()
forfeit_button = ttk.Button(controls, text = 'Forfeit', command = forfeit_game).grid()
new_game_button = ttk.Button(controls, text = 'New game', command = newGame).grid()
save_button = ttk.Button(controls, text= 'Save', command = save_game).grid()
load_button = ttk.Button(controls, text='Load', command = load_game).grid()
rules_button = ttk.Button(controls, text = 'Rules', command = lambda:show_rules(text_box))
rules_button.grid()
# pause_button = ttk.Checkbutton(controls, text = 'pause game', variable = game_is_paused, command = lambda: pause_game(button_list))
# pause_button.grid()
movesShown = tk.BooleanVar()
showAvailMoves = ttk.Checkbutton(controls,text = 'Show Available Moves',variable=movesShown, onvalue= True,
                 offvalue = False, command = lambda: highlight_message(button_list))
showAvailMoves.grid()
controls.grid(row=1, column = 1)

text_box = tk.Text(root, state ='disabled', width=80, height=14)
text_box.grid(row=2, column=0)

display_message(text_box,"You can now save and load your previous games, to relive your most glorious moments!")

root.mainloop()



# References:
# https://tkdocs.com/tutorial/
# https://tkdocs.com/tutorial/widgets.html#button