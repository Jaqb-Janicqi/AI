from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from decode_fenn_piece import type_from_char
from move import Move


class Board:
    def __init__(self, size):
        self.size = size
        self.__board = [[None for file in range(size)] for rank in range(size)]
        self.__win_state = None
        self.player_color = "White"
        self.player_turn = "White"

    def print(self):  # print matrix of the board with fenn notation for pieces
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

    def add_piece(self, color, piece_type, file, rank):
        # add piece based on type
        if piece_type == 'Pawn':
            self.__board[rank][file] = Pawn(color, file, rank)
        elif piece_type == 'Knight':
            self.__board[rank][file] = Knight(color, file, rank)
        elif piece_type == 'Rook':
            self.__board[rank][file] = Rook(color, file, rank)
        elif piece_type == 'Queen':
            self.__board[rank][file] = Queen(color, file, rank)
        elif piece_type == 'King':
            self.__board[rank][file] = King(color, file, rank)
        else:
            pass

    def setup(self):
        self.fenn_decode('rnqknr/pppppp///PPPPPP/RNQKNR')

    def fenn_decode(self, fenn_string):
        self.__board = [[None for file in range(self.size)] for rank in range(self.size)]
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
                (color, piece_type) = type_from_char(char)
                self.add_piece(color, piece_type, file, self.size - 1 - rank)
                file += 1

    def is_valid_move(self, move, color):
        # check if move (file, rank) is in bounds and not occupied by same color
        if self.is_in_bounds(move):
            if not self.is_occupied_by_same_color(move, color):
                return True
        return False

    def is_in_bounds(self, move):
        # check if move (file, rank) is in bounds of the board
        (file, rank) = move
        if file < 0 or file >= self.size or rank < 0 or rank >= self.size:
            return False
        return True

    def is_occupied(self, move):
        # check if move (file, rank) is occupied by a piece
        (file, rank) = move
        if self.__board[rank][file] is not None:
            return True
        return False

    def is_occupied_by_same_color(self, move, color):
        # check if move (file, rank) is occupied by a piece of the same color
        (file, rank) = move
        if self.__board[rank][file] is not None:
            if self.__board[rank][file] is None or self.__board[rank][file].color == color:
                return True
        return False

    def square(self, file, rank):
        return self.__board[rank][file]

    def push(self, move):
        if self.__board[move.dest_rank][move.dest_file] is not None:
            if self.__board[move.dest_rank][move.dest_file].piece_type == 'King':
                self.__win_state = move.piece.color
        self.__board[move.dest_rank][move.dest_file] = self.__board[move.piece.rank][move.piece.file]
        self.__board[move.piece.rank][move.piece.file] = None
        self.__board[move.dest_rank][move.dest_file].rank = move.dest_rank
        self.__board[move.dest_rank][move.dest_file].file = move.dest_file
        self.__board[move.dest_rank][move.dest_file].moved()

    @property
    def win_state(self):
        return self.__win_state
