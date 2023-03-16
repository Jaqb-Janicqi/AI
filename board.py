from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from decode_fenn_piece import type_from_char

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for file in range(size)] for rank in range(size)]

    def print(self): # print matrix of the board
        for rank in range(self.size):
            for file in range(self.size):
                if self.board[rank][file] == 0:
                    print('  ', end='')
                else:
                    print(self.board[rank][file], end=' ')
                if file == self.size - 1:
                    print()

    def add_piece(self, color, type, file, rank):
        # add piece based on type
        if type == 'Pawn':
            self.board[rank][file] = Pawn(color)
        elif type == 'Knight':
            self.board[rank][file] = Knight(color)
        elif type == 'Rook':
            self.board[rank][file] = Rook(color)
        elif type == 'Queen':
            self.board[rank][file] = Queen(color)
        elif type == 'King':
            self.board[rank][file] = King(color)

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
                self.add_piece(color, type, file, rank)
                file += 1
