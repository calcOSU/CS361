# Author: Charles Cal
# Date: 8/8/2022
# Description:
#import TicTacToeUI
import CheckersUI
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from functools import partial

import TicTacToeUI


class MainWindow(tk.Tk):
    def __init__(self):
        """initialize a window"""
        super().__init__()
        self.button_list_player1 = list()
        self.button_list_player2 = list()
        self.player1_options = ttk.LabelFrame(self, text = "Player 1 options")
        self.player2_options = ttk.LabelFrame(self, text="Player 2 options")
        self._button_setups()
        self.player1_auth = False
        self.player2_auth = False
        self.player1_username = ''
        self.player2_username = ''

    def _button_setups(self):
        """A method to initialize all of the buttons in this window"""
        self.DEFAULT_BUTTON_HEIGHT = 5
        self.DEFAULT_BUTTON_WIDTH = 15
        self._button_setup_player1()
        self._button_setup_player2()
        self.player1_options.grid(row=0, column = 0)
        self.player2_options.grid(row=0, column = 1)

    def _button_setup_player1(self):
        """
        Set up the basic button functionality
        :return:
        """
        new_user = tk.Button(self.player1_options, text = "New User", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = self.new_user_creation)
        new_user.grid(row = 0, column = 0)
        self.button_list_player1.append(new_user)

        existing_user = tk.Button(self.player1_options, text = "Existing User", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = lambda: self.login(self.player1_auth))
        self.button_list_player1.append(existing_user)
        existing_user.grid(row = 1, column = 0)

        guest_login = tk.Button(self.player1_options, text = "Guest Player", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = lambda: self.guest_user(1))
        self.button_list_player1.append(guest_login)
        guest_login.grid(row = 2, column = 0)

        tic_tac_toe = tk.Button(self.player1_options, text = "Play Tic Tac Toe", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = self.play_tictactoe, state = "disabled")
        self.button_list_player1.append(tic_tac_toe)
        tic_tac_toe.grid(row = 3, column = 0)

        checkers = tk.Button(self.player1_options, text = "Play Checkers", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = self.play_checkers, state = "disabled")
        self.button_list_player1.append(checkers)
        checkers.grid(row = 4, column = 0)

        elo = tk.Button(self.player1_options, text = "View ELO", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = lambda: self.view_elo(1), state = "disabled")
        self.button_list_player1.append(elo)
        elo.grid(row = 5, column = 0)

    def _button_setup_player2(self):
        """
        Set up the basic button functionality
        :return:
        """
        new_user = tk.Button(self.player2_options, text = "New User", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = self.new_user_creation)
        new_user.grid(row = 0, column = 0)
        self.button_list_player2.append(new_user)

        existing_user = tk.Button(self.player2_options, text = "Existing User", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = lambda: self.login(self.player1_auth))
        self.button_list_player2.append(existing_user)
        existing_user.grid(row = 1, column = 0)

        guest_login = tk.Button(self.player2_options, text = "Guest Player", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = lambda: self.guest_user(2))
        self.button_list_player2.append(guest_login)
        guest_login.grid(row = 2, column = 0)

        tic_tac_toe = tk.Button(self.player2_options, text = "Play Tic Tac Toe", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = self.play_tictactoe, state = "disabled")
        self.button_list_player2.append(tic_tac_toe)
        tic_tac_toe.grid(row = 3, column = 0)

        checkers = tk.Button(self.player2_options, text = "Play Checkers", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = self.play_checkers, state = "disabled")
        self.button_list_player2.append(checkers)
        checkers.grid(row = 4, column = 0)

        elo = tk.Button(self.player2_options, text = "View ELO", height = self.DEFAULT_BUTTON_HEIGHT, width = self.DEFAULT_BUTTON_WIDTH, command = lambda: self.view_elo(2), state = "disabled")
        self.button_list_player2.append(elo)
        elo.grid(row = 5, column = 0)

    def new_user_creation(self):
        """a method generate a window to create a new user account
        referenced: https://pythonexamples.org/python-tkinter-login-form/
        """
        self.new_user_window = tk.Toplevel(self)
        self.new_user_window.title('New User Creation')

        username_label = tk.Label(self.new_user_window, text = "Enter User Name").grid(row = 0, column = 0)
        self.username = tk.StringVar()
        username_entry = tk.Entry(self.new_user_window, textvariable = self.username)
        username_entry.grid(row= 0, column = 1)

        password_label = tk.Label(self.new_user_window,text = "Enter Password").grid(row = 1, column = 0)
        self.password = tk.StringVar()
        password_entry = tk.Entry(self.new_user_window, textvariable=self.password, show = "*").grid(row =1, column = 1)

        password_confirm_label = tk.Label(self.new_user_window,text = "Confirm Password").grid(row = 2, column = 0)
        self.password_confirm = tk.StringVar()
        confirm_password = tk.Entry(self.new_user_window, textvariable=self.password_confirm, show = "*")
        confirm_password.grid(row =2, column = 1)

        create_account = tk.Button(self.new_user_window, text= "Create New Player", command = self.validate_new_user)
        create_account.grid(row = 3, column = 0)

    def validate_new_user(self):
        """A method to validate new user account creation"""
        password = self.password.get()
        username = self.username.get()
        password_confirm = self.password_confirm.get()
        if password != password_confirm:
            tk.messagebox.showerror(title="mismatched passwords", message = "passwords do not match")
            return
        self.password_file_handling(username,password)

    def password_file_handling(self, username,password):
        """
        A method to handle the json password file
        :param username:
        :param password:
        :return:
        """
        with open('user_name_file.json', 'r') as f:
            user_password_combo = json.load(f)
        if username in user_password_combo.keys():
            tk.messagebox.showerror(title="Account Exists", message ="That username already exists")
        else:
            user_password_combo[username] = [password,1000,1000,1000]
            with open('user_name_file.json','w') as f:
                json.dump(user_password_combo,f)
            tk.messagebox.showinfo(title="Account Created", message="Your account has been created")
            self.new_user_window.destroy()


    def login(self, player_auth):
        """
        A method to generate a window to allow an existing user to login
        Referenced: https://pythonexamples.org/python-tkinter-login-form/
        :return:
        """
        self.login_window = tk.Toplevel(self)
        self.new_user_window.title('Login')

        username_label = tk.Label(self.login_window, text = "Enter User Name").grid(row = 0, column = 0)
        self.username_login = tk.StringVar()
        username_entry = tk.Entry(self.login_window, textvariable = self.username_login)
        username_entry.grid(row= 0, column = 1)

        password_label = tk.Label(self.login_window,text = "Enter Password").grid(row = 1, column = 0)
        self.password_login = tk.StringVar()
        password_entry = tk.Entry(self.login_window, textvariable = self.password_login, show = "*")
        password_entry.grid(row=1,column = 1)

        login_button = tk.Button(self.login_window, text = "login", command = self.validate_login)
        login_button.grid(row = 2, column = 0)

    def validate_login(self, player_auth):
        """validates the login of username and password"""
        username = self.username_login.get()
        password = self.password_login.get()
        with open('user_name_file.json', 'r') as f:
            user_password_combo = json.load(f)
        if user_password_combo[username]:
            if user_password_combo[username][0] == password:
                player_auth = True
                if player_auth == self.player1_auth:
                    self.player1_username = username
                else:
                    self.player2_username = username
                self.unlock_buttons()

    def unlock_buttons(self):
        """A method to enable the locked buttons"""
        if self.player1_auth:
            self.button_list_player1[5]['state']= 'active'
        if self.player2_auth:
            self.button_list_player2[5]['state'] = 'active'
        if self.player2_auth and self.player1_auth:
            self.button_list_player2[3]['state'] = 'active'
            self.button_list_player2[4]['state'] = 'active'
            self.button_list_player1[3]['state'] = 'active'
            self.button_list_player1[4]['state'] = 'active'



    def guest_user(self, player):
        """
        A method to allow a user to login as anonymous
        :return:
        """
        if player == 1:
            self.player1_auth = True
            self.player1_username = "Anon"
        elif player == 2:
            self.player2_auth = True
            self.player2_username = "Anon"
        self.unlock_buttons()

    def play_tictactoe(self):
        """
        A method to allow a user to start a tic tac toe game
        :return:
        """
        tic_tac_toe_game = TicTacToeUI.TicTacToeUI()

    def play_checkers(self):
        """
        A method to allow a user to start a tic tac toe game
        :return:
        """
        checkers_game = CheckersUI.CheckersUI()

    def view_elo(self, player):
        """
        A method to allow a user to view their ELO scores
        :return:
        """
        with open('user_name_file.json', 'r') as f:
            user_data = json.load(f)
        if player == 1:
            user = self.player1_username
        elif player == 2:
            user = self.player2_username
        user_elo = user_data[user]
        self.display_elo(user_elo)

    def display_elo(self,elo_data):
        self.elo_window = tk.Toplevel(self)
        self.elo_window.title('ELO Data')
        tictactoe_elo = tk.Label(self.elo_window,text = f'Tic Tac Toe ELO: {elo_data[1]}').grid(row = 0, column = 0)
        checkers_elo = tk.Label(self.elo_window,text = f'Checkers ELO: {elo_data[2]}').grid(row = 1, column = 0)
        chess_elo = tk.Label(self.elo_window, text=f'Chess ELO: {elo_data[3]}').grid(row=2, column=0)

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()


# reference:
# https://pythonexamples.org/python-tkinter-login-form/
# https://docs.python.org/3/library/tkinter.messagebox.html


