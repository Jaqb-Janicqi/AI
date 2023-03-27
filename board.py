from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from decode_fenn_piece import type_from_char

class Board:
    def __init__(self, size):
        self.size = size
        self.__board = [[None for file in range(size)] for rank in range(size)]
        self.__white_king = None
        self.__white_pawns = []
        self.__white_knights = []
        self.__white_rooks = []
        self.__white_queens = []
        self.__black_king = None
        self.__black_pawns = []
        self.__black_knights = []
        self.__black_rooks = []
        self.__black_queens = []
        self.__win_state = None

    def print(self): # print matrix of the board with fenn notation for pieces
        for rank in range(self.size):
            print(rank, end='  ')
            for file in range(self.size):
                if self.__board[rank][file] == None:
                    print('  ', end='')
                else:
                    print(self.__board[rank][file], end=' ')
                if file == self.size - 1:
                    print()
        print()
        print('   ', end='')
        for file in range(self.size):
            print(file, end=' ')

    def add_piece(self, color, type, file, rank):
        # add piece based on type
        if type == 'Pawn':
            self.__board[rank][file] = Pawn(color, file, rank)
            if color == 'White':
                self.__white_pawns.append(self.__board[rank][file])
            else:
                self.__black_pawns.append(self.__board[rank][file])
        elif type == 'Knight':
            self.__board[rank][file] = Knight(color, file, rank)
            if color == 'White':
                self.__white_knights.append(self.__board[rank][file])
            else:
                self.__black_knights.append(self.__board[rank][file])
        elif type == 'Rook':
            self.__board[rank][file] = Rook(color, file, rank)
            if color == 'White':
                self.__white_rooks.append(self.__board[rank][file])
            else:
                self.__black_rooks.append(self.__board[rank][file])
        elif type == 'Queen':
            self.__board[rank][file] = Queen(color, file, rank)
            if color == 'White':
                self.__white_queens.append(self.__board[rank][file])
            else:
                self.__black_queens.append(self.__board[rank][file])
        elif type == 'King':
            self.__board[rank][file] = King(color, file, rank)
            if color == 'White':
                self.__white_king = self.__board[rank][file]
            else:
                self.__black_king = self.__board[rank][file]
        else:
            pass

    def setup(self):
        for file in range(self.size):
            self.add_piece('White', 'Pawn', file, 1)
            self.add_piece('Black', 'Pawn', file, self.size - 1)

        self.add_piece('White', 'Rook', 0, 0)
        self.add_piece('White', 'Knight', 1, 0)
        self.add_piece('White', 'Queen', 2, 0)
        self.add_piece('White', 'King', 3, 0)
        self.add_piece('White', 'Knight', 4, 0)
        self.add_piece('White', 'Rook', 5, 0)

        self.add_piece('Black', 'Rook', 0, 5)
        self.add_piece('Black', 'Knight', 1, 5)
        self.add_piece('Black', 'Queen', 2, 5)
        self.add_piece('Black', 'King', 3, 5)
        self.add_piece('Black', 'Knight', 4, 5)
        self.add_piece('Black', 'Rook', 5, 5)

    def fenn_decode(self, fenn_string):
        # decode fenn string and add pieces to the board
        file = 0
        rank = 0
        for char in fenn_string:
            if char == '/':
                file = 0
                rank += 1
            elif char.isdigit():
                file += int(char)
            else:
                (color, type) = type_from_char(char)
                self.add_piece(color, type, file, self.size - 1 - rank)
                file += 1

    def is_valid_move(self, move, color):
        # check if move (file, rank) is in bounds and not occupied by same color
        if self.is_in_bounds(move) and not self.is_occupied_by_same_color(move, color):
            return True
        return False
    
    def is_in_bounds(self, file, rank):
        # check if move (file, rank) is in bounds of the board
        if file < 0 or file >= self.size or rank < 0 or rank >= self.size:
            return False
        return True
    
    def is_occupied(self, move):
        # check if move (file, rank) is occupied by a piece
        (file, rank) = move
        if self.__board[rank][file] != 0:
            return True
        return False

    def is_occupied_by_same_color(self, file, rank, color):
        # check if move (file, rank) is occupied by a piece of the same color
        if self.__board[rank][file] != 0:
            if self.__board[rank][file].color == color:
                return True
        return False
    

    # this may not be needed, one can capture the king instead
    # def is_attacked(self, move, color):
    #     # check if move (file, rank) is attacked by other color
    #     if color == 'White':
    #         return self.is_attacked_by_black(move)
    #     else:
    #         return self.is_attacked_by_white(move)

    @property
    def win_state(self):
        return self.__win_state