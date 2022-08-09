# Author: Charles Cal
# Date: 7/12/2022
# Description:

import Checkers
import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
import json
import webbrowser

class GridButton(tk.Button):
    """
    A method to define the button used in the board
    """
    def __init__(self, position,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.position = position

class CheckersUI(tk.Tk):
    """
    a class for a checkers UI
    referenced: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-window/
    """
    def __init__(self):
        super().__init__()
        self.game = Checkers.Checkers()
        self.first_square_is_selected = False
        self.first_selected = (0,0)
        self.second_selected = (0,0)
        self.source = 0, 0
        self.first_move = True
        self.board = ttk.LabelFrame(self, text='make a move')
        self.grid_list = []
        self.button_maker()
        self.board.grid(row=1, column=0)
        self.controls_creation()
        self.status_bar()

    def controls_creation(self):
        """
        A method for creating the controls widget
        :return:
        """
        self.controls = ttk.LabelFrame(self, text='Options')
        self.controls.columnconfigure(0, weight=1)
        self.undo_button = ttk.Button(self.controls, text='Undo', command=self.undo).grid()
        self.forfeit_button = ttk.Button(self.controls, text='Forfeit', command=self.forfeit_game).grid()
        self.new_game_button = ttk.Button(self.controls, text='New game', command=self.new_game).grid()
        self.save_button = ttk.Button(self.controls, text='Save', command=self.save_game).grid()
        self.load_button = ttk.Button(self.controls, text='Load', command=self.load_game).grid()
        self.rules_button = ttk.Button(self.controls, text='Rules Link', command=self.link_to_rules).grid()
        self.controls.grid(row=0, column=1)

    def status_bar(self):
        self.status_bar = tk.Label(
            self, text=f"Red Select a piece",
            font=("TkDefaultFont", 16)
        )
        self.status_bar.grid(row=0, column = 0)

    def make_a_move(self, square):
        """The function to be invoked when clicking on a game grid square"""
        print(square)
        print(self.game)
        if self.game.more_jumps:
            self.more_jumps_available(square)
        else:
            self.square_switcher()
            if self.first_square_is_selected:
                self.first_selected = square
            else:
                self.second_selected = square
                self.game.move1(self.first_selected,square)
                self.update_game_screen()
        self.update_status_bar()

    def more_jumps_available(self,destination):
        """A method to handle if there are more jumps available"""
        self.game.move1(self.second_selected,destination)


    def update_status_bar(self):
        """Updates the status bar to prompt the player what to do"""
        color = 'Red' if self.game.turn == 0 else 'Black'
        if self.game.more_jumps:
            self.more_jumps_message()
        else:
            if self.first_square_is_selected:
                message = ' select a destination'
            else:
                message = ' select a piece'
            self.status_bar['text'] = color + message

    def more_jumps_message(self):
        text = 'More jumps available\nSelect another position to jump to or select the same piece to pass your turn'
        self.status_bar['text'] = text

    def square_switcher(self):
        """switches the first_square_selected attribute"""
        if self.first_square_is_selected:
            self.first_square_is_selected = False
        else:
            self.first_square_is_selected = True

    def update_game_screen(self):
        """A method to update the buttons once the underlying game has been changed"""
        for row in range(8):
            for col in range(8):
                self.button_list[row][col]['text'] = f'{self.show((row,col))}'

    def clean_slate(self):
        """A method for starting a new game fresh"""
        self.game.fresh_board()
        self.update_game_screen()
        self.update_status_bar()

    def show(self, grid):
        """
        A function to show the current item in a given grid square
        :param grid:
        :return:
        """
        if self.game.board[grid[0]][grid[1]]:
            return self.game.board[grid[0]][grid[1]]
        else:
            return ""

    def undo(self):
        self.game.undo()
        self.update_game_screen()
        self.update_status_bar()

    def forfeit_game(self):
        rsp = messagebox.askyesno('Forfeit', 'Are you sure you want to forfeit? You\'ll lose the game!')
        if rsp:
            winner = "Red " if game.turn == '1' else 'Black '
            self.status_bar['text'] = f'{winner}wins!'

    def new_game(self):
        rsp = messagebox.askyesno('New Game', "Are you sure you want to start a new game?\nThis won't count on either player's record'")
        if rsp:
            self.clean_slate()

    def save_game(self):
        """
        a function to save the game in a json file
        :return:
        """
        if not os.path.isdir('CheckersSaves'):
            os.mkdir('CheckersSaves')

        now = datetime.datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
        save_name = "CheckersSaves\\Checkers_" +dt_string+".json"
        export = self.game.export_game()
        with open(save_name,'w') as f:
            json.dump(export,f)
        tk.messagebox.showinfo(title="Saved Game", message = f'Saved game as {save_name}')

    def load_game(self):
        """
        A method to load a perviously saved game
        :return:
        """
        t = tk.Toplevel(self)
        saved_files = [x for x in os.listdir('CheckersSaves') if x[-4:] == 'json']
        for save in saved_files:
            ttk.Button(t,text = save, command = lambda: self.open_game(save,t)).grid()

    def open_game(self,file_name,window):
        """
        A method to load a perviously saved game once the save file has been selected
        :return:
        """
        rsp = tk.messagebox.askyesno('Open Saved game', "Are you sure you want to open this save?\nThe current game will be discarded")
        if rsp:
            with open('CheckersSaves\\'+file_name, 'r') as f:
                import_game = json.load(f)
                self.game.import_game(import_game)
            self.update_game_screen()
            self.update_status_bar()
            window.destroy()



    def link_to_rules(self):
        """
        callback function for the rules button
        :return:
        """
        webbrowser.open_new_tab('https://www.ultraboardgames.com/checkers/game-rules.php')

    def button_maker(self):
        """
        A method to generate all the grid squares as buttons
        :return:
        """
        self.button_list = list()
        row = list()
        button00 = GridButton(position=(0, 0), bg='#EDAA9B', master=self.board, text=f'{self.show((0, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 0)))
        button00.grid(row=0, column=0)
        row.append(button00)
        button01 = GridButton(position=(0, 1), bg='#AEF0E9', master=self.board, text=f'{self.show((0, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 1)))
        button01.grid(row=0, column=1)
        row.append(button01)
        button02 = GridButton(position=(0, 2), bg='#EDAA9B', master=self.board, text=f'{self.show((0, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 2)))
        button02.grid(row=0, column=2)
        row.append(button02)
        button03 = GridButton(position=(0, 3), bg='#AEF0E9', master=self.board, text=f'{self.show((0, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 3)))
        button03.grid(row=0, column=3)
        row.append(button03)
        button04 = GridButton(position=(0, 4), bg='#EDAA9B', master=self.board, text=f'{self.show((0, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 4)))
        button04.grid(row=0, column=4)
        row.append(button04)
        button05 = GridButton(position=(0, 5), bg='#AEF0E9', master=self.board, text=f'{self.show((0, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 5)))
        button05.grid(row=0, column=5)
        row.append(button05)
        button06 = GridButton(position=(0, 6), bg='#EDAA9B', master=self.board, text=f'{self.show((0, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 6)))
        button06.grid(row=0, column=6)
        row.append(button06)
        button07 = GridButton(position=(0, 7), bg='#AEF0E9', master=self.board, text=f'{self.show((0, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((0, 7)))
        button07.grid(row=0, column=7)
        row.append(button07)
        self.button_list.append(row)
        row = list()
        button10 = GridButton(position=(1, 0), bg='#AEF0E9', master=self.board, text=f'{self.show((1, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 0)))
        button10.grid(row=1, column=0)
        row.append(button10)
        button11 = GridButton(position=(1, 1), bg='#EDAA9B', master=self.board, text=f'{self.show((1, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 1)))
        button11.grid(row=1, column=1)
        row.append(button11)
        button12 = GridButton(position=(1, 2), bg='#AEF0E9', master=self.board, text=f'{self.show((1, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 2)))
        button12.grid(row=1, column=2)
        row.append(button12)
        button13 = GridButton(position=(1, 3), bg='#EDAA9B', master=self.board, text=f'{self.show((1, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 3)))
        button13.grid(row=1, column=3)
        row.append(button13)
        button14 = GridButton(position=(1, 4), bg='#AEF0E9', master=self.board, text=f'{self.show((1, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 4)))
        button14.grid(row=1, column=4)
        row.append(button14)
        button15 = GridButton(position=(1, 5), bg='#EDAA9B', master=self.board, text=f'{self.show((1, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 5)))
        button15.grid(row=1, column=5)
        row.append(button15)
        button16 = GridButton(position=(1, 6), bg='#AEF0E9', master=self.board, text=f'{self.show((1, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 6)))
        button16.grid(row=1, column=6)
        row.append(button16)
        button17 = GridButton(position=(1, 7), bg='#EDAA9B', master=self.board, text=f'{self.show((1, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((1, 7)))
        button17.grid(row=1, column=7)
        row.append(button17)
        self.button_list.append(row)
        row = list()
        button20 = GridButton(position=(2, 0), bg='#EDAA9B', master=self.board, text=f'{self.show((2, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 0)))
        button20.grid(row=2, column=0)
        row.append(button20)
        button21 = GridButton(position=(2, 1), bg='#AEF0E9', master=self.board, text=f'{self.show((2, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 1)))
        button21.grid(row=2, column=1)
        row.append(button21)
        button22 = GridButton(position=(2, 2), bg='#EDAA9B', master=self.board, text=f'{self.show((2, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 2)))
        button22.grid(row=2, column=2)
        row.append(button22)
        button23 = GridButton(position=(2, 3), bg='#AEF0E9', master=self.board, text=f'{self.show((2, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 3)))
        button23.grid(row=2, column=3)
        row.append(button23)
        button24 = GridButton(position=(2, 4), bg='#EDAA9B', master=self.board, text=f'{self.show((2, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 4)))
        button24.grid(row=2, column=4)
        row.append(button24)
        button25 = GridButton(position=(2, 5), bg='#AEF0E9', master=self.board, text=f'{self.show((2, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 5)))
        button25.grid(row=2, column=5)
        row.append(button25)
        button26 = GridButton(position=(2, 6), bg='#EDAA9B', master=self.board, text=f'{self.show((2, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 6)))
        button26.grid(row=2, column=6)
        row.append(button26)
        button27 = GridButton(position=(2, 7), bg='#AEF0E9', master=self.board, text=f'{self.show((2, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((2, 7)))
        button27.grid(row=2, column=7)
        row.append(button27)
        self.button_list.append(row)
        row = list()
        button30 = GridButton(position=(3, 0), bg='#AEF0E9', master=self.board, text=f'{self.show((3, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 0)))
        button30.grid(row=3, column=0)
        row.append(button30)
        button31 = GridButton(position=(3, 1), bg='#EDAA9B', master=self.board, text=f'{self.show((3, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 1)))
        button31.grid(row=3, column=1)
        row.append(button31)
        button32 = GridButton(position=(3, 2), bg='#AEF0E9', master=self.board, text=f'{self.show((3, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 2)))
        button32.grid(row=3, column=2)
        row.append(button32)
        button33 = GridButton(position=(3, 3), bg='#EDAA9B', master=self.board, text=f'{self.show((3, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 3)))
        button33.grid(row=3, column=3)
        row.append(button33)
        button34 = GridButton(position=(3, 4), bg='#AEF0E9', master=self.board, text=f'{self.show((3, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 4)))
        button34.grid(row=3, column=4)
        row.append(button34)
        button35 = GridButton(position=(3, 5), bg='#EDAA9B', master=self.board, text=f'{self.show((3, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 5)))
        button35.grid(row=3, column=5)
        row.append(button35)
        button36 = GridButton(position=(3, 6), bg='#AEF0E9', master=self.board, text=f'{self.show((3, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 6)))
        button36.grid(row=3, column=6)
        row.append(button36)
        button37 = GridButton(position=(3, 7), bg='#EDAA9B', master=self.board, text=f'{self.show((3, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((3, 7)))
        button37.grid(row=3, column=7)
        row.append(button37)
        self.button_list.append(row)
        row = list()
        button40 = GridButton(position=(4, 0), bg='#EDAA9B', master=self.board, text=f'{self.show((4, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 0)))
        button40.grid(row=4, column=0)
        row.append(button40)
        button41 = GridButton(position=(4, 1), bg='#AEF0E9', master=self.board, text=f'{self.show((4, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 1)))
        button41.grid(row=4, column=1)
        row.append(button41)
        button42 = GridButton(position=(4, 2), bg='#EDAA9B', master=self.board, text=f'{self.show((4, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 2)))
        button42.grid(row=4, column=2)
        row.append(button42)
        button43 = GridButton(position=(4, 3), bg='#AEF0E9', master=self.board, text=f'{self.show((4, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 3)))
        button43.grid(row=4, column=3)
        row.append(button43)
        button44 = GridButton(position=(4, 4), bg='#EDAA9B', master=self.board, text=f'{self.show((4, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 4)))
        button44.grid(row=4, column=4)
        row.append(button44)
        button45 = GridButton(position=(4, 5), bg='#AEF0E9', master=self.board, text=f'{self.show((4, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 5)))
        button45.grid(row=4, column=5)
        row.append(button45)
        button46 = GridButton(position=(4, 6), bg='#EDAA9B', master=self.board, text=f'{self.show((4, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 6)))
        button46.grid(row=4, column=6)
        row.append(button46)
        button47 = GridButton(position=(4, 7), bg='#AEF0E9', master=self.board, text=f'{self.show((4, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((4, 7)))
        button47.grid(row=4, column=7)
        row.append(button47)
        self.button_list.append(row)
        row = list()
        button50 = GridButton(position=(5, 0), bg='#AEF0E9', master=self.board, text=f'{self.show((5, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 0)))
        button50.grid(row=5, column=0)
        row.append(button50)
        button51 = GridButton(position=(5, 1), bg='#EDAA9B', master=self.board, text=f'{self.show((5, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 1)))
        button51.grid(row=5, column=1)
        row.append(button51)
        button52 = GridButton(position=(5, 2), bg='#AEF0E9', master=self.board, text=f'{self.show((5, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 2)))
        button52.grid(row=5, column=2)
        row.append(button52)
        button53 = GridButton(position=(5, 3), bg='#EDAA9B', master=self.board, text=f'{self.show((5, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 3)))
        button53.grid(row=5, column=3)
        row.append(button53)
        button54 = GridButton(position=(5, 4), bg='#AEF0E9', master=self.board, text=f'{self.show((5, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 4)))
        button54.grid(row=5, column=4)
        row.append(button54)
        button55 = GridButton(position=(5, 5), bg='#EDAA9B', master=self.board, text=f'{self.show((5, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 5)))
        button55.grid(row=5, column=5)
        row.append(button55)
        button56 = GridButton(position=(5, 6), bg='#AEF0E9', master=self.board, text=f'{self.show((5, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 6)))
        button56.grid(row=5, column=6)
        row.append(button56)
        button57 = GridButton(position=(5, 7), bg='#EDAA9B', master=self.board, text=f'{self.show((5, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((5, 7)))
        button57.grid(row=5, column=7)
        row.append(button57)
        self.button_list.append(row)
        row = list()
        button60 = GridButton(position=(6, 0), bg='#EDAA9B', master=self.board, text=f'{self.show((6, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 0)))
        button60.grid(row=6, column=0)
        row.append(button60)
        button61 = GridButton(position=(6, 1), bg='#AEF0E9', master=self.board, text=f'{self.show((6, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 1)))
        button61.grid(row=6, column=1)
        row.append(button61)
        button62 = GridButton(position=(6, 2), bg='#EDAA9B', master=self.board, text=f'{self.show((6, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 2)))
        button62.grid(row=6, column=2)
        row.append(button62)
        button63 = GridButton(position=(6, 3), bg='#AEF0E9', master=self.board, text=f'{self.show((6, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 3)))
        button63.grid(row=6, column=3)
        row.append(button63)
        button64 = GridButton(position=(6, 4), bg='#EDAA9B', master=self.board, text=f'{self.show((6, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 4)))
        button64.grid(row=6, column=4)
        row.append(button64)
        button65 = GridButton(position=(6, 5), bg='#AEF0E9', master=self.board, text=f'{self.show((6, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 5)))
        button65.grid(row=6, column=5)
        row.append(button65)
        button66 = GridButton(position=(6, 6), bg='#EDAA9B', master=self.board, text=f'{self.show((6, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 6)))
        button66.grid(row=6, column=6)
        row.append(button66)
        button67 = GridButton(position=(6, 7), bg='#AEF0E9', master=self.board, text=f'{self.show((6, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((6, 7)))
        button67.grid(row=6, column=7)
        row.append(button67)
        self.button_list.append(row)
        row = list()
        button70 = GridButton(position=(7, 0), bg='#AEF0E9', master=self.board, text=f'{self.show((7, 0))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 0)))
        button70.grid(row=7, column=0)
        row.append(button70)
        button71 = GridButton(position=(7, 1), bg='#EDAA9B', master=self.board, text=f'{self.show((7, 1))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 1)))
        button71.grid(row=7, column=1)
        row.append(button71)
        button72 = GridButton(position=(7, 2), bg='#AEF0E9', master=self.board, text=f'{self.show((7, 2))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 2)))
        button72.grid(row=7, column=2)
        row.append(button72)
        button73 = GridButton(position=(7, 3), bg='#EDAA9B', master=self.board, text=f'{self.show((7, 3))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 3)))
        button73.grid(row=7, column=3)
        row.append(button73)
        button74 = GridButton(position=(7, 4), bg='#AEF0E9', master=self.board, text=f'{self.show((7, 4))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 4)))
        button74.grid(row=7, column=4)
        row.append(button74)
        button75 = GridButton(position=(7, 5), bg='#EDAA9B', master=self.board, text=f'{self.show((7, 5))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 5)))
        button75.grid(row=7, column=5)
        row.append(button75)
        button76 = GridButton(position=(7, 6), bg='#AEF0E9', master=self.board, text=f'{self.show((7, 6))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 6)))
        button76.grid(row=7, column=6)
        row.append(button76)
        button77 = GridButton(position=(7, 7), bg='#EDAA9B', master=self.board, text=f'{self.show((7, 7))}', height=4,
                              width=6, command=lambda: self.make_a_move((7, 7)))
        button77.grid(row=7, column=7)
        row.append(button77)
        self.button_list.append(row)


if __name__ == "__main__":
    game = CheckersUI()
    for x in range(3):
        for y in range(8):
            if x == 2 and y == 2:
                pass
            else:
                game.game.admin_move((x,y), None)
    game.update_game_screen()
    game.mainloop()





#References:
# https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter
# https://elfi-y.medium.com/super-inherit-your-python-class-196369e3377a
