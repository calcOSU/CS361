# Author: Charles Cal
# Date: 7/3/2022
# Description:


class TicTacToeGame():
    """
    A class for a tic tac toe game
    """
    def __init__(self):
        """
        initializes the game by creating a blank 3x3 board
        """
        self.turn = 0
        self.board = list()
        for _ in range(3):
            self.board.append([None for _ in range(3)])
        self.turnDict = {0:'X',1:'O'}

    def __str__(self):
        """
        A string representation of the current state of the board
        :return: a string representation
        """
        board_str = ""
        for row in range(len(self.board)):
            row_str = ""
            for col in range(len(self.board[row])):
                if self.board[row][col] == "X":
                    row_str += " X "
                elif self.board[row][col] == "O":
                    row_str += " O "
                else:
                    row_str += "   "
                if col < len(self.board[row])-1:
                    row_str += "|"
            board_str += '\n' + row_str
            if row < len(self.board) -1:
                board_str += '\n' + '___________'
        return board_str

    def showTurn(self):
        """Displays which team's turn it is"""
        return self.turnDict[self.turn]

    def move(self, selection):
        """
        A method for making a move based on an input row and column.  Returns false if the position is already filled
        :param selection: a tuple consisting of (row, column)
        :return:
        """
        if self.win_check() or self.tie_check():
            return False
        if self.board[selection[0]][selection[1]]:
            return False
        elif self.turn == 0:
            self.board[selection[0]][selection[1]] = 'X'
            self.turn = 1
        else:
            self.board[selection[0]][selection[1]] = 'O'
            self.turn = 0

    def win_check(self):
        """
        Checks for a win condition by checking the horizontal, vertical, and diagonal directions
        :return:
        """
        def horizontal():
            """
            A check for wins along a row
            :return: True if a win is found, false otherwise
            """
            for row in range(len(self.board)):
                if self.board[row][0] is None:
                    continue
                win_found = True
                for col in range(len(self.board[row])):
                    if self.board[row][col] != self.board[row][0]:
                        win_found = False
                if win_found:
                    return f'{self.board[row][0]} wins!'
            return False

        def vertical():
            """
            A check for wins along a column
            :return:  True if a win is found, false otherwise
            """
            for col in range(len(self.board[0])):
                if self.board[0][col] is None:
                    continue
                win_found = True
                for row in range(len(self.board)):
                    if self.board[row][col] != self.board[0][col]:
                        win_found = False
                if win_found:
                    return f'{self.board[0][col]} wins!'
            return False

        def diagonal1():
            """
            A check for a win from the upper left to lower right diagonal
            :return: True if a win is found, false otherwise
            """
            if self.board[0][0] is None:
                return False
            for row_col in range(len(self.board)):
                if self.board[row_col][row_col] != self.board[0][0]:
                    return False
            return f'{self.board[0][0]} wins!'

        def diagonal2():
            """
            A check for a win from the lower left to upper right diagonal
            :return: True if a win is found, false otherwise
            """
            if self.board[0][-1] is None:
                return False
            for row_col in range(len(self.board)):
                if self.board[row_col][len(self.board)-1-row_col] != self.board[0][-1]:
                    return False
            return f'{self.board[0][-1]} wins!'
        return horizontal() or vertical() or diagonal1() or diagonal2()

    def tie_check(self):
        """
        A check to see if there remains any open spaces
        :return: True if a tie is found (no open spaces), false otherwise
        """
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if not self.board[row][col]:
                    return False
        return "It's a tie!"

    def export_game(self):
        """Export a game for the purpose of saving"""
        return (self.turn, self.board)

    def import_game(self, board, turn):
        """Import a game for the purpose of loading
        ::todo:: add more input validation to ensure it's a proper game
        """
        self.board = board
        self.turn = turn

    def game_flow(self):
        """
        A method to initialize and play a tic tac toe game
        :return:
        """
        print('welcome to tictactoe')
        while (self.win_check() or self.tie_check()) is False:
            print(self)
            print('make a selection')
            row_select = True
            while row_select:
                print('pick a row (0-2)')
                try:
                    row = int(input())
                    row_select = False
                except:
                    print('invalid')
            col_select = True
            while col_select:
                print('pick a col (0-2)')
                try:
                    col = int(input())
                    col_select = False
                except:
                    print('invalid')
            self.move((row,col))
        if self.tie_check():
            print('draw')
        if self.turn == 1:
            print('x wins')
        else:
            print('O wins')






if __name__ == "__main__":
    game = TicTacToeGame()
    game.game_flow()
    # def basic_tests():
    #     horizontal_win_x_check = ([0,0],[1,1],[0,1],[2,2],[0,2])
    #     game = TicTacToeGame()
    #     for _ in horizontal_win_x_check:
    #         game.move(_)
    #     print(game.win_check())
    #     vertical_win_o_check = ([1,1],[0,0],[0,2],[1,0],[2,2],[2,0])
    #     game = TicTacToeGame()
    #     for _ in vertical_win_o_check:
    #         game.move(_)
    #     print(game.win_check())
    #     diagonal1_win_x_check = ([0,0],(0,1),(1,1),(1,0),(2,2))
    #     game = TicTacToeGame()
    #     for _ in diagonal1_win_x_check:
    #         game.move(_)
    #     print(game.win_check())
    #     diagonal2_win_o_check = ((0,0),(0,2),(0,1),(1,1),(1,0),(2,0))
    #     game = TicTacToeGame()
    #     for _ in diagonal2_win_o_check:
    #         game.move(_)
    #     print(game.win_check())
    #     draw_check = ((0,0),(1,1),(0,1),(0,2),(2,0),(1,0),(2,1),(2,2),(1,2))
    #     game = TicTacToeGame()
    #     for _ in draw_check:
    #         game.move(_)
    #     print(game.tie_check())
