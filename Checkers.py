# Author: Charles Cal
# Date: 7/4/2022
# Description:

class Piece():
    def __init__(self, side):

        self.side = side
        if self.side == 0:
            self.color = "Red"
            self.directions = [1]
        else:
            self.color = "Black"
            self.directions = [-1]
        self.king = False

    def __str__(self):
        return self.color[0]


class Checkers():
    def __init__(self):
        self.turn = 0
        self.moves = list()
        self.board = list()
        for _ in range(8):
            self.board.append([None for _ in range(8)])
        for row in range(3):
            for col in range(8):
                if row % 2 == 0:
                    if col % 2 == 0:
                        self.board[row][col] = Piece(0)
                else:
                    if col % 2 == 1:
                        self.board[row][col] = Piece(0)
        for row in range(5,8):
            for col in range(8):
                if row % 2 == 0:
                    if col % 2 == 0:
                        self.board[row][col] = Piece(1)
                else:
                    if col % 2 == 1:
                        self.board[row][col] = Piece(1)

    def __str__(self):
        """
        A string representation of the current state of the board
        :return: a string representation
        """
        board_str = "   "
        for x in range(8):
            board_str += f" {x}  "
        board_str += '\n'
        for row in range(len(self.board)):
            row_str = f" {row} "
            for col in range(len(self.board[row])):
                if not self.board[row][col]:
                    row_str += "   "
                else:
                    row_str += " " + str(self.board[row][col]) + " "
                if col < len(self.board[row])-1:
                    row_str += "|"
            board_str += '\n' + row_str
            if row < len(self.board) -1:
                board_str += '\n' +"   " + '_' * 31
        return board_str

    def build_game(self,cell):
        """The purpose of this function is to build a game from a list of moves (for example, generated from the moves
        of a previous game
        ::TODO:: write this function, consider challenge of extended jumps"""
        pass

    def board_cell(self, cell):
        """ returns the piece at a given cell"""
        return self.board[cell[0]][cell[1]]

    def cell_validation(self,cell):
        """
        basic validation for a pairing of two integers in a cell (as a list, tuple, etc.)
        ::todo:: PEP8 violation w/ too broad of except-- specific exceptions
        :param cell:
        :return:
        """
        try:
            if len(cell) != 2:
                print('improper length')
                return False
            else:
                try:
                    val1 = int(cell[0])
                    val2 = int(cell[1])
                    if  0 < val1 < len(self.board) and 0 < val2 < len(self.board[0]):
                        return True
                    else:
                        print('outside of board boundaries')
                        return False
                except:
                    print('invalid data types in input')
                    return False
        except:
            print('pairing of coordinates is invalid')
            return False

    def move(self, source,destination):
        """a method to combine jump moves and normal moves"""
        if not self.board[source[0]][source[1]]:
            print('no piece')
            return False
        elif self.board[source[0]][source[1]].side != self.turn:
            print('wrong piece')
            return False
        if abs(source[0]-destination[0]) == 1:
            self.normal_move(source,destination)
            self.turn = 0 if self.turn == 1 else 1
            self.king_me(destination)
        elif abs(source[0]-destination[0]) == 2:
            self.jump_move(source,destination)
            current = destination
            while self.find_jump_moves(current):
                self.extended_jump(current)
            self.king_me(destination)
            self.game_end_check()
        else:
            print('not valid')
            return False

    def game_end_check(self):
        tie = True
        red_wins = True
        black_wins = True
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board_cell((row,col)) is not None:
                    if self.board_cell((row,col)).side == 0:
                        black_wins = False
                    else:
                        red_wins = False
                    if self.turn == 0:
                        if self.board_cell((row,col)).side == 0:
                            if self.find_jump_moves((row,col)) or self.find_normal_moves((row,col)):
                                tie = False
                    else:
                        if self.board_cell((row,col)).side == 1:
                            if self.find_jump_moves((row,col)) or self.find_normal_moves((row,col)):
                                tie = False
        if red_wins:
            print('red wins')
            return 1
        if black_wins:
            print('black wins')
            return 2
        if tie:
            print('tie')
            return 3
        return False

    def extended_jump(self,source):
        current = source
        while self.find_jump_moves(current):
            print('Would you like to jump again?')
            ans = input().lower()[0]
            if ans == 'y':
                while True:
                    try:
                        print('pick the next row')
                        row = input()
                        print('pick the next col')
                        col = input()
                        row = int(row)
                        col = int(col)
                        if self.board[row][col] in self.find_jump_moves(current):
                            self.board[row][col] = self.board[current[0]][current[1]]
                            self.board[current[0]][current[1]] = None
                            jumped_row = int((row - current[0]) / 2)
                            jumped_col = int((col - current[1]) / 2)
                            self.board[jumped_row][jumped_col] = None
                            self.moves.append((current, (row,col), (jumped_row,jumped_col)))
                            current = (row,col)
                            self.king_me(current)
                            self.game_end_check()
                            if len(self.find_jump_moves(current)) > 0:
                                print('more jumps possible')
                        break
                    except:
                        pass
                    print('invalid row and column selection')
            else:
                break
        else:
            return False

    def normal_move(self, source, destination):
        """A method to allow a piece to move without jumping another piece"""
        if destination in self.find_normal_moves(source):
            self.board[destination[0]][destination[1]] = self.board[source[0]][source[1]]
            self.board[source[0]][source[1]] = None
            self.moves.append((source,destination))
        else:
            print('invalid move')
            return False

    def jump_move(self, source,destination):
        """A method to allow a piece to jump another piece"""
        if destination in self.find_jump_moves(source):
            self.board[destination[0]][destination[1]] = self.board[source[0]][source[1]]
            self.board[source[0]][source[1]] = None
            jumped_row = int((destination[0] + source[0])/2)
            jumped_col = int((destination[1] + source[1])/2)
            self.board[jumped_row][jumped_col] = None
            if self.find_jump_moves(destination):
                print('more jumps possible')
                return True
            else:
                self.turn = 0 if self.turn == 1 else 1
                self.king_me(destination)
                self.moves.append((source, destination, (jumped_row,jumped_col)))
        else:
            print(f'{source} to {destination} is not a valid jump move')
            return False

    def king_me(self,source):
        """A method to check if a piece should be a king, and king them if appropriate"""
        if not self.board_cell(source):
            return False
        if self.board_cell(source).side == 0:
            if source[0] == len(self.board) - 1:
                self.board_cell(source).king = True
        else:
            if source[0] == 0:
                self.board_cell(source).king = True

    def find_jump_moves(self,source):
        """A method to find all possible jump moves for a given piece"""
        if not self.board[source[0]][source[1]]:
            return False
        piece = self.board[source[0]][source[1]]
        possible_moves = list()
        for row_change in piece.directions:
            new_row = source[0] + row_change*2
            if 0 < new_row < len(self.board):
                pass
            else:
                continue
            for new_col in [source[1] + 2, source[1] -2]:
                if 0 < new_col < len(self.board[0]):
                    if self.board[new_row][new_col] is None:
                        jumped_row = int((new_row + source[0])/2)
                        jumped_col = int((new_col + source[1])/2)
                        try:
                            if self.board[jumped_row][jumped_col] is not None:
                                if self.board[jumped_row][jumped_col].side != piece.side:
                                    possible_moves.append((new_row,new_col))
                        except IndexError:
                            print(f'{source} to {jumped_row,jumped_col} is not a valid board move')
        return possible_moves

    def find_normal_moves(self, source):
        if not self.board[source[0]][source[1]]:
            return False
        piece = self.board[source[0]][source[1]]
        possible_moves = list()
        for row_change in piece.directions:
            new_row = source[0] + row_change
            if 0 < new_row < len(self.board):
                for new_col in [source[1] + 1, source[1] - 1]:
                    if 0 < new_col < len(self.board[0]):
                        if self.board[new_row][new_col] is None:
                            possible_moves.append((new_row, new_col))
            else:
                continue

        return possible_moves

    def undo(self):
        """
        A method to undo the last move made
        :return:
        """
        try:
            last_move = self.moves.pop()
        except IndexError:
            print('moves list is empty.  Nothing to undo')
        self.board[last_move[0][0]][last_move[0][1]] = self.board[last_move[1][0]][last_move[1][1]]
        self.board[last_move[1][0]][last_move[1][1]] = None
        if len(last_move) > 2:
            jump_side = 1 if self.board[last_move[0][0]][last_move[0][1]].side == 0 else 0
            self.board[last_move[2][0]][last_move[2][1]] = Piece(jump_side)
        self.turn = self.board[last_move[0][0]][last_move[0][1]].side

    def game_flow(self):
        """A method to play the game
        ::TODO:: more testing"""
        while not self.game_end_check():
            print(self)
            while True:
                if self.turn == 0:
                    print("red's turn")
                else:
                    print("black's turn")
                try:
                    print('pick a piece to move')
                    print('enter a row (0-7)')
                    row = input()
                    print('enter a col (0-7)')
                    col = input()
                    source = int(row), int(col)
                    print('pick a location to move to')
                    print('enter a row (0-7)')
                    row = input()
                    print('enter a col (0-7)')
                    col = input()
                    destination = int(row), int(col)
                    self.move(source,destination)
                    break
                except Exception as e:
                    print(e.__class__)
                    pass
                print('invalid')
        print('game over')




if __name__ == "__main__":
    game = Checkers()
    # game.game_flow()
    game.move((2,2),(3,3))
    game.move((5,1),(4,2))
    game.move((3,3),(5,1))
    print(game)
    print(game.turn)
    game.undo()
    print(game)
    print(game.turn)
    # print(f'valid jump moves for 3,3')
    # print(game.find_jump_moves((3,3)))
    # print('\njump moves: \n')
    # print(game.find_jump_moves((1,5)))
    # game.move((3,3),(5,1))
    # print(game)
