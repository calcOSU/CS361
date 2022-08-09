# Author: Charles Cal
# Date: 8/6/2022
# Description:
# ::todo:: en passant
# ::todo:: castling
# ::todo:: three types of draw: stalemate, threefold repetition, fifty-move rule
DEBUG = False
ERROR_MSGS = list()


class Chess:
    def __init__(self):
        self.move_list = list()
        self.gameBoard = list()
        for row in range(8):
            rowl = list()
            for col in range(8):
                rowl.append(None)
            self.gameBoard.append(rowl)
        self.turn = 0  # 0 for white, 1 for black
        self.fill_board()
        self.promotion_required = False
        print(self)

    def fill_board(self):
        """ a method to fill the board"""
        func_list = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
        for col in range(8):
            self.gameBoard[1][col] = Pawn(1)
            self.gameBoard[6][col] = Pawn(0)
            self.gameBoard[0][col] = func_list[col](1)
            self.gameBoard[7][col] = func_list[col](0)
        self.white_king, self.black_king = (7, 3), (0, 3)

    def __repr__(self):
        """intent for repr is to recreate conditions of board"""
        return str(self.gameBoard)

    def __str__(self):
        """string representation to print board"""
        board_header = [f'  {x}' for x in range(8)]
        board_str = '  '.join(board_header)
        board_str = '     ' + board_str + '\n'
        for row in range(len(self.gameBoard)):
            board_str += f'  {row}  '
            for col in range(len(self.gameBoard[row])):
                space = self.gameBoard[row][col]
                if space == None:
                    board_str += "    "
                else:
                    board_str += str(space)
                if col != len(self.gameBoard[row]) - 1:
                    board_str += "|"
            board_str += '\n'
            if row != len(self.gameBoard) - 1:
                board_str += '     ' + '_' * (4 * len(self.gameBoard) + len(self.gameBoard) - 1) + '\n'
        return board_str

    def all_positions(self):
        """returns all possible positions"""
        results = list()
        for row in range(8):
            for col in range(8):
                results.append((row, col))
        return results

    def stalemate_check(self):
        """
        This method considers whose turn it is, and checks every piece on the board.  If no valid moves exist, but the player is not in check
        """
        all_squares = self.all_positions()
        for position in all_squares:
            piece = self.gameBoard[position[0]][position[1]]
            if not piece:
                continue
            elif piece.side != self.turn and self.attacking_king(position):
                return False
            elif len(self.piece_possible_moves(position)) > 0:
                return False
        return True

    def checkmate_check(self):
        """This method checks all squares to see if the king is in check, and if so """
        all_squares = self.all_positions()
        king_under_attack, nowhere_to_move = False, True
        for square in all_squares:
            if self.get_piece(square):
                if self.get_piece(square).side != self.turn and self.attacking_king(square):
                    print(f'Check from the {self.get_piece(square)} at {square}')
                    king_under_attack = True
                elif self.piece_possible_moves(square):
                    nowhere_to_move = False
        if king_under_attack and not nowhere_to_move:
            return True
        return False

    def piece_possible_moves(self, source, hypo_check=True):
        """
        A method that finds all the possible moves of a piece at a given square
        :param source:
        :param hypo_check:
        :return:
        """
        results = list()
        tgt_piece = self.gameBoard[source[0]][source[1]]
        if tgt_piece is None:
            print('no piece')
            return False
        pos_moves = tgt_piece.find_possible_moves(source)
        if DEBUG:
            err_msg = f'finding possible moves for piece: {tgt_piece} at location {source}\npossible moves: {pos_moves}'
            print(err_msg)
            ERROR_MSGS.append(err_msg)
        if not pos_moves:
            return False
        self.validate_moves(source, pos_moves, results, hypo_check)
        if tgt_piece.get_type() == "Pawn":
            self.pawn_capture_validation(source, results)
        return results

    def pawn_capture_validation(self, source, moves_list):
        """A method to determine if a pawn can capture any pieces"""
        capture_squares = self.get_piece(source).find_capture_moves(source)
        for square in capture_squares:
            if self.get_piece(square).side != self.get_piece(source.side):
                moves_list.append(square)

    def validate_moves(self, source, pos_moves, results, hypo_check):
        """
        Given a list of possible moves, validates whether those moves are actually possible based on the gameboard
        :param source:
        :param pos_moves:
        :param results:
        :param hypo_check:
        :return:
        """
        tgt_piece = self.gameBoard[source[0]][source[1]]
        for pos in pos_moves:
            row0, col0 = pos
            if not (0 <= row0 < 8 and 0 <= col0 < 8):
                continue
            if tgt_piece.get_type() == "Pawn":  # need to consider separate attack and movement squares
                self.pawn_moves(source, pos, results, hypo_check)

            elif tgt_piece.get_type() == "Knight":  # don't need to check for intervening squares
                self.knight_moves(source, pos, results, hypo_check)

            else:
                self.other_moves(source, pos, results, hypo_check)

    def pawn_moves(self, source, destination, results, hypo_check):
        """
        A method to check if a potential move is valid for a pawn
        :param source: gameboard location of the pawn
        :param destination: gameboard location of the potential move (assumes that the pawn can legally move here)
        :param results: a running list of potential moves
        :param hypo_check: whether to check for if the move will allow it's own king to be checked
        :return:
        ::todo:: need to add for capture moves
        """
        if self.gameBoard[destination[0]][destination[1]]:  # space already occupied
            return False
        elif self.route_is_clear(source, destination) is False:  # consider moving two spaces off the beginning
            return False
        else:
            if hypo_check and self.hypothetical_check(source, destination):
                return False
            results.append(destination)
            return True

    def knight_moves(self, source, destination, results, hypo_check):
        """
        A method to determine valid moves for a knight
        :param source:
        :param destination:
        :param results:
        :param hypo_check:
        :return:
        """
        dst_square = self.gameBoard[destination[0]][destination[1]]
        if (not dst_square or dst_square.side != self.gameBoard[source[0]][source[1]].side):
            if hypo_check and self.hypothetical_check(source, destination):
                return False
            else:
                results.append(destination)
        return False

    def other_moves(self, source, destination, results, hypo_check):
        """
        A method for all other pieces (bishops, rooks, queens, king)
        :param source:
        :param destination:
        :param results:
        :param hypo_check:
        :return:
        """
        dst_square = self.gameBoard[destination[0]][destination[1]]
        if DEBUG:
            print(f'validating the move from {source} to {destination}')
            print(f'source piece is a {self.gameBoard[source[0]][source[1]]}')
        if (not dst_square or dst_square.side != self.gameBoard[source[0]][source[1]].side) and self.route_is_clear(
                source, destination):
            if hypo_check and self.hypothetical_check(source, destination):
                return False
            else:
                results.append(destination)
        else:
            return False

    def hypothetical_check(self, source, dst):
        """a method to check if a movement form source to dst would place the team's king in check
        returns a list containing the squares that would put the king into check"""
        results = None
        source_piece = self.gameBoard[source[0]][source[1]]
        if not source_piece:
            return False
        place_holder = self.admin_move(source, dst)
        for row in range(8):
            for col in range(8):
                if self.gameBoard[row][col]:  # is there a piece there?
                    if self.attacking_king((row, col)):
                        results.append((row, col))
        self.gameBoard[source[0]][source[1]] = self.gameBoard[dst[0]][dst[1]]
        self.gameBoard[dst[0]][dst[1]] = place_holder
        return results if results else False

    def attacking_king(self, source):
        """
        A method to determine if the the piece at source position is attacking the opposing king
        :param source:
        :return:
        """
        potential_attacker = self.gameBoard[source[0]][source[1]]
        attacking_positions = list()
        if potential_attacker is None:
            return False
        pos_moves = self.piece_possible_moves(source, False)
        if not pos_moves:
            return False
        self.validate_moves(source, pos_moves, attacking_positions, False)
        if self.is_king_attacked(attacking_positions, potential_attacker.side):
            return True
        return False

    def is_king_attacked(self, position_list, side):
        """
        A method to determine if the king is being attacked based on the opposing side given
        :param position_list: a list of positions that may contain the king
        :param side: the side of the potential attacker
        :return: True if the opposing king is being attacked, False otherwise
        """
        for pos in position_list:
            tgt = self.gameBoard[pos[0]][pos[1]]
            if not tgt:
                continue
            if tgt.get_type() == 'King' and tgt.side != side:
                return True
        return False

    def admin_move(self, source, dst):
        """A method to make an admin move, returns the piece that was occupying the destination square"""
        result = self.gameBoard[dst[0]][dst[1]]
        self.gameBoard[dst[0]][dst[1]] = self.gameBoard[source[0]][source[1]]
        self.gameBoard[source[0]][source[1]] = None
        return result

    def check_check(self, source):
        """a method to check if a given square is a king and if they are, if they are currently in check
        will return a list consisting of positions of attackers of the king (empty list if it's safe)"""
        results = list()
        tgt_piece = self.gameBoard[source[0]][source[1]]
        if not tgt_piece:
            return False
        if tgt_piece.get_type() != "King":
            return False
        else:
            for row1 in range(8):
                for col1 in range(8):
                    potential_attacker = self.gameBoard[row1][col1]
                    if not potential_attacker:
                        continue
                    elif potential_attacker.side == tgt_piece.side:
                        continue
                    else:
                        if source in self.piece_possible_moves((row1, col1)):
                            results.append((row1, col1))
        return results

    def move(self, source, dst):
        """a method from moving a piece from a source square to a destination square"""
        if self.upgrade_required:
            print('a pawn promotion must be made')
            return False
        tgt_piece = self.gameBoard[source[0]][source[1]]
        if self.move_input_validation(source, dst) is False:
            return False
        pos_moves = self.piece_possible_moves(source)
        if dst not in pos_moves:
            self.move_debug_msg()
            return False
        else:
            self.update_move_list(source, dst)
            self.admin_move(source, dst)
            self.turn = 0 if self.turn == 1 else 1
            tgt_piece.moved = True
            tgt_piece.king_update(dst)

    def update_move_list(self, source, destination):
        """a method to update the move list"""
        self.move_list.append(source, self.get_piece(source),destination, self.get_piece(destination))

    def undo(self):
        """
        A method to undo the last move made
        :return:
        ::todo:: implement a way to rebuild the move list as part of a saved game
        """
        try:
            last_move = self.my_list.pop()
        except IndexError:
            print('no moves to undo!')
        self.set_gameboard(last_move[2],last_move[3])
        self.set_gameboard(last_move[0],last_move[1])

    def set_gameboard(self,target_square,piece):
        """
        A method to set the target square to a given piece
        :param target:
        :param piece:
        :return:
        """
        self.gameBoard[target_square[0]][target_square[1]] = piece

    def move_debug_msg(self,source, destination, pos_moves):
        """
        A debug message for the move method
        :param source:
        :param destination:
        :param pos_moves:
        :return:
        """
        tgt_piece = self.get_piece(source)
        print('move not possible')
        if DEBUG:
            self.move_debug_msg(source, dst, pos_moves)
            error_msg = f'you tried to move from {source} to {dst}\nthe valid moves from {source}, which is a {tgt_piece} are:\n{pos_moves}'
            print(error_msg)
            ERROR_MSGS.append(error_msg)
            print(f'you tried to move from {source} to {dst}')
            print(f'the valid moves from {source}, which is a {tgt_piece} are:')
            print(pos_moves)

    def get_piece(self, position):
        """
        This method returns the piece at a given location
        """
        return self.gameBoard[position[0]][position[1]]

    def king_update(self, position):
        """
        This method updates the king position tracker if the piece given at position is a king, else it does nothing
        """
        piece = self.get_piece(position)
        if piece.type == 'King':
            if piece.side == 0:
                self.white_king = position
            else:
                self.black_king = position

    def move_input_validation(self, source, dst):
        """
        basic input validation for the move method
        :param source:
        :return:
        """
        if not (0 <= dst[0] < 8 and 0 <= dst[1] < 8 and 0 <= source[0] < 8 and 0 <= source[1] < 8):
            print('bad input')
            return False
        tgt_piece = self.gameBoard[source[0]][source[1]]
        if tgt_piece is None:
            print('no piece')
            return False
        elif tgt_piece.side != self.turn:
            print('not your turn')
            return False
        else:
            return True

    def route_is_clear(self, start, finish):
        """Given a starting location and a finishing location, checks if obstructions exist
        Returns False if an intervening space is not empty, otherwise returns the list of intervening spaces
        Note: does not check if the finish square is free or not"""
        if DEBUG:
            print(f'checking if the route is clear between {start} and {finish}')
        in_between_spaces = self.find_in_between_spaces(start, finish)
        for space in in_between_spaces:
            if self.gameBoard[space[0]][space[1]] is not None:
                return False
        return in_between_spaces

    def find_in_between_spaces(self, source, dst):
        """
        A helper method to find the squares that are in between the source and the destination (not inclusive)
        :param source:
        :param dst:
        :return:
        """
        spaces = list()
        if source[0] != dst[0]:  # it changes row
            row_range = list(range(source[0] + 1, dst[0]) if source[0] < dst[0] else range(source[0] - 1, dst[0], -1))
        else:
            row_range = [source[0] for _ in range(abs(source[1] - dst[1]) - 1)]
        if source[1] != dst[1]:
            col_range = list(range(source[1] + 1, dst[1]) if source[1] < dst[1] else range(source[1] - 1, dst[1], -1))
        else:
            col_range = [source[1] for _ in range(abs(source[0] - dst[0]) - 1)]
        if DEBUG:
            print(f'spaces between {source} and {dst}:')
            print(f'row range: {row_range}, col range: {col_range}')
        for _ in range(len(row_range)):
            spaces.append((row_range[_], col_range[_]))
        return spaces

    def promotion(self, location, upgrade):
        """A method to promote a pawn if they've reached the opposite end of the board"""
        row, col = location
        if self.promo_checks(location, upgrade) is False:
            return False
        side = self.gameBoard[row][col].side
        if upgrade == 'K':
            self.gameBoard[row][col] = Knight(side)
        elif upgrade == 'B':
            self.gameBoard[row][col] = Bishop(side)
        elif upgrade == 'R':
            self.gameBoard[row][col] = Rook(side)
        elif upgrade == 'Q':
            self.gameBoard[row][col] = Rook(side)

    def promo_checks(self, location, upgrade):
        """a method for the input validation checks for the promotion function"""
        row, col = location
        if self.gameBoard[row][col] is None:
            print('no piece')
            return False
        if self.gameBoard[row][col].get_type() != 'Pawn':
            print('not a pawn')
            return False
        if upgrade not in ['K', 'B', 'R', 'Q']:
            print(
                'improper promotion, possible choices are "K" for knight, "B" for bishop, "R" for rook and "Q" for queen')
            return False
        self.upgrade_required = False
        return True


class Piece:
    def __init__(self, side):
        """
        initialize the piece, side is 0 for white, 1 for black"""
        self.side = side
        self._type = None
        self.moved = False

    def movement(self):
        pass

    def __repr__(self):
        res = 'w' if self.side == 0 else 'b'
        res += self._type[0]
        if self._type == "King":
            res = "*" + res + "*"
        else:
            res = " " + res + " "
        return res

    def get_type(self):
        return self._type


class Pawn(Piece):
    def __init__(self, side):
        self._type = "Pawn"
        self.side = side
        self.modifier = 1 if self.side == 1 else -1

    def find_possible_moves(self, pos):
        x, y = pos
        pos_moves = list()
        if x == 1 or x == 6:
            pos_move = x + 2 * self.modifier, y
            pos_moves.append(pos_move)
        pos_moves.append((x + 1 * self.modifier, y))
        return pos_moves

    def find_capture_moves(self, pos):
        row, col = pos
        pos_moves = list()
        pos_moves.append((row + 1 * self.modifier, col + 1))
        pos_moves.append((row + 1 * self.modifier, col - 1))
        return pos_moves


class Rook(Piece):
    def __init__(self, side):
        self.side = side
        self._type = "Rook"
        self.moved = False

    def find_possible_moves(self, pos):
        row, col = pos
        pos_moves = list()
        for _ in range(1, 9):
            pos_moves.append((row + _, col))
            pos_moves.append((row - _, col))
            pos_moves.append((row, col + _))
            pos_moves.append((row, col - _))
        return pos_moves


class Knight(Piece):
    def __init__(self, side):
        self.side = side
        self._type = "Knight"

    def find_possible_moves(self, pos):
        x, y = pos
        pos_moves = list()
        for jump in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            pos_move = y + jump[0], x + jump[1]
            pos_moves.append(pos_move)
        return pos_moves


class Bishop(Piece):
    def __init__(self, side):
        self.side = side
        self._type = "Bishop"

    def find_possible_moves(self, pos):
        x, y = pos
        pos_moves = list()
        for _ in range(1, 9):
            pos_moves.append((y + _, x + _))
            pos_moves.append((y + _, x - _))
            pos_moves.append((y - _, x + _))
            pos_moves.append((y - _, x - _))


class Queen(Piece):
    def __init__(self, side):
        self.side = side
        self._type = "Queen"

    def find_possible_moves(self, pos):
        row, col = pos
        pos_moves = list()
        for _ in range(1, 9):
            pos_moves.append((row + _, col + _))
            pos_moves.append((row + _, col - _))
            pos_moves.append((row - _, col + _))
            pos_moves.append((row - _, col - _))
            pos_moves.append((row + _, col))
            pos_moves.append((row - _, col))
            pos_moves.append((row, col + _))
            pos_moves.append((row, col - _))
        return pos_moves


class King(Piece):
    def __init__(self, side):
        self.side = side
        self._type = "King"
        self.moved = False

    def find_possible_moves(self, pos):
        row, col = pos
        pos_moves = list()
        combo = [0, -1, 1]
        for m1 in combo:
            for m2 in combo:
                pos_move = row + m1, col + m2
                if (m1, m2) != (0, 0):
                    pos_moves.append(pos_move)
        return pos_moves


if __name__ == "__main__":
    print('initializing')
    game = Chess()
    game.move((6, 3), (5, 3))
    print(game)
    print(game.piece_possible_moves((6, 3)))
    print(game)

    game.move((1, 0), (3, 0))
    print(game)
    game.move((3, 0), (4, 2))
    game.move((7, 4), (3, 0))
    print(game)
    for _ in ERROR_MSGS:
        print(_)
    print(game)