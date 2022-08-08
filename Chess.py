# Author: Charles Cal
# Date: 8/6/2022
# Description:
class Chess:
    def __init__(self):
        self.gameBoard = list()
        for row in range(8):
            rowl = list()
            for col in range(8):
                rowl.append(None)
            self.gameBoard.append(rowl)
        self.turn = 0  # 0 for white, 1 for black
        self.fill_board()
        print(self)

    def fill_board(self):
        """ a method to fill the board"""
        func_list = [Rook,Knight,Bishop,King,Queen,Bishop,Knight,Rook]
        for col in range(8):
            self.gameBoard[1][col] = Pawn(1)
            self.gameBoard[6][col] = Pawn(0)
            self.gameBoard[0][col] = func_list[col](1)
            self.gameBoard[7][col] = func_list[col](0)

    def __repr__(self):
        """intent for repr is to recreate conditions of board"""
        return str(self.gameBoard)

    def __str__(self):
        """string representation to print board"""
        board_str = ""
        for row in range(len(self.gameBoard)):
            for col in range(len(self.gameBoard[row])):
                space = self.gameBoard[row][col]
                if space == None:
                    board_str += "    "
                else:
                    board_str += str(space)
                if col != len(self.gameBoard[row]) -1:
                    board_str += "|"
            board_str += '\n'
            if row != len(self.gameBoard) -1:
                board_str += '_' * (4* len(self.gameBoard) + len(self.gameBoard) -1) + '\n'
        return board_str

    def piece_possible_moves(self,source,hypo_check = True):
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
        if not pos_moves:
            return False
        self.validate_moves(source,pos_moves,results,hypo_check)
        return results

    def validate_moves(self,source,pos_moves,results,hypo_check):
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
                self.pawn_moves(source,pos,results,hypo_check)

            elif tgt_piece.get_type() == "Knight":  # don't need to check for intervening squares
                self.knight_moves(source,pos,results,hypo_check)

            else:
                self.other_moves(source,pos,results,hypo_check)

    def pawn_moves(self,source, destination, results, hypo_check):
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

    def knight_moves(self,source,destination, results, hypo_check):
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

    def other_moves(self,source,destination,results,hypo_check):
        """
        A method for all other pieces (bishops, rooks, queens, king)
        :param source:
        :param destination:
        :param results:
        :param hypo_check:
        :return:
        """
        dst_square = self.gameBoard[destination[0]][destination[1]]
        if (not dst_square or dst_square.side != self.gameBoard[source[0]][source[1]].side) and self.route_is_clear(source, destination):
            if hypo_check and self.hypothetical_check(source, destination):
                return False
            else:
                results.append(destination)
        else:
            return False


    def hypothetical_check(self,source, dst):
        """a method to check if a movement form source to dst would place the team's king in check
        returns a list containing the squares that would put the king into check"""
        results = None
        source_piece = self.gameBoard[source[0]][source[1]]
        if not source_piece:
            return False
        place_holder = self.admin_move(source,dst)
        for row in range(8):
            for col in range(8):
                if self.gameBoard[row][col]: # is there a piece there?
                    if self.attacking_king((row,col)):
                        results.append((row,col))
        self.gameBoard[source[0]][source[1]] = self.gameBoard[dst[0]][dst[1]]
        self.gameBoard[dst[0]][dst[1]] = place_holder
        return results if results else False

    def attacking_king(self,source):
        """
        A method to determine if the the piece at source position is attacking the opposing king
        :param source:
        :return:
        """
        potential_attacker = self.gameBoard[source[0]][source[1]]
        attacking_positions = list()
        if potential_attacker is None:
            return False
        pos_moves = self.piece_possible_moves(source,False)
        if not pos_moves:
            return False
        self.validate_moves(source,pos_moves,attacking_positions,False)
        if self.is_king_attacked(attacking_positions,potential_attacker.side):
            return True
        return False

    def is_king_attacked(self,position_list,side):
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



    def admin_move(self,source,dst):
        """A method to make an admin move, returns the piece that was occupying the destination square"""
        result = self.gameBoard[dst[0]][dst[1]]
        self.gameBoard[dst[0]][dst[1]] = self.gameBoard[source[0]][source[1]]
        self.gameBoard[source[0]][source[1]] = None
        return result

    def check_check(self,source):
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
                        if source in self.piece_possible_moves((row1,col1)):
                            results.append((row1,col1))
        return results

    def move(self,source,dst):
        """a method from moving a piece from a source square to a destination square"""
        tgt_piece = self.gameBoard[source[0]][source[1]]
        dst_square = self.gameBoard[dst[0]][dst[1]]
        if self.move_input_validation(source,dst) is False:
            return False
        pos_moves = self.piece_possible_moves(source)
        if dst_square not in pos_moves:
            print('move not possible')
            return False
        else:
            self.admin_move(source,dst)
            self.turn = 0 if self.turn == 1 else 1
            tgt_piece.moved = True

    def move_input_validation(self,source,dst):
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
        in_between_spaces = self.find_in_between_spaces(start,finish)
        for space in in_between_spaces:
            if self.gameBoard[space[0]][space[1]] is not None:
                return False
        return in_between_spaces

    def find_in_between_spaces(self,source,dst):
        spaces = list()
        if source[0] != dst[0]:  # it changes row
            row_range = list(range(source[0]+1,dst[0]) if source[0] < dst[0] else range(source[0]-1,dst[0],-1))
        else:
            row_range = [source[0] for _ in range(abs(source[1]-dst[1])-1)]
        if source[1] != dst[1]:
            col_range = list(range(source[1]+1,dst[1]) if source[1] < dst[1] else range(source[1]-1,dst[1],-1))
        else:
            col_range = [source[1] for _ in range(abs(source[0]-dst[0])-1)]
        for _ in range(len(row_range)):
            spaces.append((row_range[_],col_range[_]))
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

    def promo_checks(self,location,upgrade):
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
    def __init__(self,side):
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
        x, y = pos
        pos_moves = list()
        pos_moves.append((x + 1 * self.modifier, y + 1))
        pos_moves.append((x + 1 * self.modifier, y - 1))
        return pos_moves


class Rook(Piece):
    def __init__(self,side):
        self.side = side
        self._type = "Rook"
        self.moved = False

    def find_possible_moves(self, pos):
        x, y = pos
        pos_moves = list()
        for _ in range(1, 9):
            pos_moves.append((y + _, x))
            pos_moves.append((y - _, x))
            pos_moves.append((y, x + _))
            pos_moves.append((y, x - _))
        return pos_moves


class Knight(Piece):
    def __init__(self,side):
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
    def __init__(self,side):
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
    def __init__(self,side):
        self.side = side
        self._type = "Queen"

    def find_possible_moves(self, pos):
        x, y = pos
        pos_moves = list()
        for _ in range(1, 9):
            pos_moves.append((y + _, x + _))
            pos_moves.append((y + _, x - _))
            pos_moves.append((y - _, x + _))
            pos_moves.append((y - _, x - _))
            pos_moves.append((y + _, x))
            pos_moves.append((y - _, x))
            pos_moves.append((y, x + _))
            pos_moves.append((y, x - _))


class King(Piece):
    def __init__(self,side):
        self.side = side
        self._type = "King"
        self.moved = False

    def find_possible_moves(self, pos):
        x, y = pos
        pos_moves = list()
        combo = [0, -1, 1]
        for m1 in combo:
            for m2 in combo:
                pos_move = y + m1, x + m2
                if (m1, m2) != (0, 0):
                    pos_moves.append(pos_move)
        return pos_moves

if __name__ == "__main__":
    game = Chess()
    game.move((6,3),(5,3))
    print(game)
    print(game.piece_possible_moves((6,3)))