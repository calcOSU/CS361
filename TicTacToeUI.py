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


class TicTacToeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = TicTacToe.TicTacToeGame()
        self.columnconfigure(1, weight=1)
        self.turn_tracker = tk.Label(self, text = f"{self.game.showTurn()}'s turn", font=("TkDefaultFont",16))
        self.turn_tracker.grid()
        self.board = ttk.LabelFrame(self,text='Make a move')
        self.gameboard = ttk.Label(self, text='tic tac toe')

# create styles for highlighted vs non-highlighted
        s = ttk.Style()
        s.configure('open.TButton', background= 'yellow', relief='raised')
        s.configure('taken.TButton', background='gray', relief='flat')
        self.grid_setup()
        self.setup_controls()
        self._setup_text_box()

    def _setup_text_box(self):
        """A method to set up the text box"""
        self.text_box = tk.Text(self, state='disabled', width=80, height=14)
        self.text_box.grid(row=2, column=0)

        self.display_message("You can now save and load your previous games, to relive your most glorious moments!")

    def updateTitle(self):
        """
        Function to display whose turn it is in on the central label
        :return:
        """
        if self.gameUpdate():
            self.turn_tracker.config(text = f"{self.gameUpdate()}")
        else:
            self.turn_tracker.config(text = f"{self.game.showTurn()}'s turn")

    def makeAMove(self,button, grid):
        """
        Callback function for selecting a tic tac toe grid item
        :param button:
        :param grid:
        :return:
        """
        self.game.move(grid)
        print(self.game)
        button['text'] = self.show(grid)
        button['style'] = 'taken.TButton'

        print(self.gameUpdate())
        self.updateTitle()
        self.highlight_available_moves()

    def display_comments(self):
        """An optional method to display encouraging comments in the log"""
        comments = ['Nice move', 'Wow!', 'No way they saw that coming!', 'Good thinking']
        pass

    def display_message(self, your_message):
        """
        a message to display a string in the text box
        :param text_box:
        :param your_message:
        :return:
        """
        self.text_box['state'] = 'normal'
        self.text_box.insert('end', '\n\n')
        self.text_box.insert('end', str(your_message))
        self.text_box['state'] = 'disabled'


    def show(self,grid):
        """
        A function to show the current item in a given grid square
        :param grid:
        :return:
        """
        if self.game.board[grid[0]][grid[1]]:
            return self.game.board[grid[0]][grid[1]]
        else:
            return ""

    def gameUpdate(self):
        """
        Checks if the game has been won or tied
        :return:
        """
        if self.game.win_check() or self.game.tie_check():
            return self.game.win_check() or self.game.tie_check()

    #definitions and placement for grid buttons
    def grid_setup(self):
        """a method to setup the grid"""
        grid_00 = ttk.Button(self.board, text=f'{self.show((0,0))}', padding = 5, command = lambda: self.makeAMove(grid_00, (0,0)))
        grid_01 = ttk.Button(self.board, text=f'{self.show((0,1))}', padding = 5, command = lambda: self.makeAMove(grid_01, (0,1)))
        grid_02 = ttk.Button(self.board, text=f'{self.show((0,2))}', padding = 5, command = lambda: self.makeAMove(grid_02, (0,2)))
        grid_10 = ttk.Button(self.board, text=f'{self.show((1,0))}', padding = 5, command = lambda: self.makeAMove(grid_10,(1,0)))
        grid_11 = ttk.Button(self.board, text=f'{self.show((1,1))}', padding = 5, command = lambda: self.makeAMove(grid_11,(1,1)))
        grid_12 = ttk.Button(self.board, text=f'{self.show((1,2))}', padding = 5, command = lambda: self.makeAMove(grid_12,(1,2)))
        grid_20 = ttk.Button(self.board, text=f'{self.show((2,0))}', padding = 5, command = lambda: self.makeAMove(grid_20,(2,0)))
        grid_21 = ttk.Button(self.board, text=f'{self.show((2,1))}', padding = 5, command = lambda: self.makeAMove(grid_21,(2,1)))
        grid_22 = ttk.Button(self.board, text=f'{self.show((2,2))}', padding = 5, command = lambda: self.makeAMove(grid_22,(2,2)))
        self.button_list = [grid_00, grid_01, grid_02, grid_10, grid_11, grid_12, grid_20, grid_21, grid_22]
        grid_00.grid(row=0,column=0)
        grid_01.grid(row=0,column=1)
        grid_02.grid(row=0,column=2)
        grid_10.grid(row=1,column=0)
        grid_11.grid(row=1,column=1)
        grid_12.grid(row=1,column=2)
        grid_20.grid(row=2,column=0)
        grid_21.grid(row=2,column=1)
        grid_22.grid(row=2,column=2)
        self.board.grid()


    def setup_controls(self):
        """set up the controls widget"""
        # Controls frame and associated buttons w/ callback functions
        self.controls = ttk.LabelFrame(self, text='Options')
        self.game_is_paused = False
        self.controls.columnconfigure(1, weight=1)
        undo_button = ttk.Button(self.controls, text='Undo', command=self.undo).grid()
        forfeit_button = ttk.Button(self.controls, text='Forfeit', command=self.forfeit_game).grid()
        new_game_button = ttk.Button(self.controls, text='New game', command=self.newGame).grid()
        save_button = ttk.Button(self.controls, text='Save', command=self.save_game).grid()
        load_button = ttk.Button(self.controls, text='Load', command=self.load_game).grid()
        rules_button = ttk.Button(self.controls, text='Rules', command=self.show_rules)
        rules_button.grid()
        self.movesShown = tk.BooleanVar()
        self.showAvailMoves = ttk.Checkbutton(self.controls, text='Show Available Moves', variable=self.movesShown,
                                              onvalue=True,
                                              offvalue=False, command=lambda: self.highlight_message(self.button_list))
        self.showAvailMoves.grid()
        self.controls.grid(row=1, column=1)

    def pause_game(self, button_list):
        """Callback function to 'pause' the game"""
        if self.game_is_paused:
            for button in self.button_list:
                button.state(['disabled'])
        else:
            for button in self.button_list:
                button.state(['!disabled'])

    def undo(self):
        """
        a function to undo the last move made
        """
        self.game.undo()
        self.update_game_screen()

    def highlight_message(self,button_list):
        """
        A method to display a simple method before highlighting open spaces
        :param button_list:
        :return:
        """
        self.text_box['state'] = 'normal'
        self.text_box.insert('end', '\n\n')
        if self.movesShown.get():
            self.text_box.insert('end', 'Showing available moves')
        else:
            self.text_box.insert('end', 'No longer showing available moves')
        self.text_box['state'] = 'disabled'
        self.highlight_available_moves(button_list)

    def highlight_available_moves(self):
        """
        A method to highlight open buttons using styles
        :param button_list:
        :return:
        """
        for button in self.button_list:
            if self.movesShown.get():
                if button['text'] != '':
                    button['style'] = 'taken.TButton'
                else:
                    button['style'] = 'open.TButton'
            else:
                button['style'] = 'TButton'


    def newGame(self):
        '''
        Callback function to clear the board and create a new game
        :return:
        '''
        rsp = messagebox.askyesno('Start a new game', 'Are you sure you want to start a new game?')
        if rsp:
            self.game = TicTacToe.TicTacToeGame()
            for button in self.button_list:
                button['text'] = ''
                button.state(['!pressed'])
            self.turn_tracker.config(text = f"{self.game.showTurn()}'s turn")
            self.highlight_available_moves(self.button_list)

    def show_rules(self):
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
        self.text_box['state'] = 'normal'
        self.text_box.insert('end', rules)
        self.text_box['state'] = 'disabled'

    def save_game(self):
        """
        A function to save the game in a text file
        :return:

        https://tkdocs.com/tutorial/windows.html
        """
        # filename = filedialog.asksaveasfilename()
        if not os.path.isdir('TicTacToe_saves'):
            os.mkdir('TicTacToe_saves')

        now = datetime.datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
        save_name = "TicTacToe_saves\\TicTacToe " +dt_string+".json"
        print(save_name)
        export = self.game.export_game()
        with open(save_name, 'w') as f:
            json.dump(export,f)
        self.display_message(f'Saved game as {save_name}')

    def load_game(self):
        """
        A function to load a previous saved game
        # reference: https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
        :return:
        """
        t = tk.Toplevel(self)
        saved_files = [x for x in os.listdir('TicTacToe_saves') if x[-4:] == 'json']
        for save in saved_files:
            ttk.Button(t, text = save, command = lambda save=save: self.open_game(save,t)).grid()


    def open_game(self,file_name, window):
        """
        A method to handle opening previously saved game once the save file has been selected
        :param file_name:
        :param window:
        :return:
        """
        rsp = messagebox.askyesno('Open saved game', 'Are you sure you want to open this save?')
        if rsp:
            with open('TicTacToe_saves\\'+file_name, 'r') as f:
                import_game = json.load(f)
                self.game.import_game(import_game[1],import_game[0])
            grid_list = list()
            for x in range(3):
                for y in range(3):
                    grid_list.append((x,y))
            for index, button in enumerate(self.button_list):
                button['text'] = f'{self.show(grid_list[index])}'
                print(self.show((1,0)))
            self.updateTitle()
            window.destroy()
            self.display_message(f'loaded game {file_name}')

    def update_game_screen(self):
        """A method to update the buttons once the underlying game has been changed"""
        grid_list = list()
        for x in range(3):
            for y in range(3):
                grid_list.append((x, y))
        for index, button in enumerate(self.button_list):
            button['text'] = f'{self.show(grid_list[index])}'
            print(self.show((1, 0)))
        self.updateTitle()

    def forfeit_game(self):
        rsp = messagebox.askyesno('Forfeit', 'Are you sure you want to forfeit? You\'ll lose the game!')
        if rsp:
            winner = "X" if self.game.showTurn() == 'O' else 'O'
            self.turn_tracker.config(text=f"{winner} wins!")






if __name__ == "__main__":
    game = TicTacToeUI()
    game.mainloop()



# References:
# https://tkdocs.com/tutorial/
# https://tkdocs.com/tutorial/widgets.html#button