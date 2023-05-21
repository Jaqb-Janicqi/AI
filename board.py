from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from decode_fenn_piece import type_from_char
from move import Move
import copy


class Board:
    def __init__(self, size):
        self.size = size
        self.__board = [[None for file in range(size)] for rank in range(size)]
        self.__win_state = None
        self.player_color = "White"
        self.player_turn = "White"
        self.white_pieces = []
        self.black_pieces = []
        self.moves = []

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
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'Knight':
            self.__board[rank][file] = Knight(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'Rook':
            self.__board[rank][file] = Rook(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'Queen':
            self.__board[rank][file] = Queen(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'King':
            self.__board[rank][file] = King(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        else:
            pass

    def setup(self):
        self.fenn_decode('rnqknr/pppppp///PPPPPP/RNQKNR')
        self.player_turn = "White"
        # self.fenn_decode('/P///p/')

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
        captured_piece = self.__board[move.dest_rank][move.dest_file]
        if captured_piece is not None:
            if self.player_turn == 'White':
                self.black_pieces.remove(captured_piece)
            else:
                self.white_pieces.remove(captured_piece)
        if move.piece.piece_type is 'Pawn' and (move.dest_rank == 0 or move.dest_rank == self.size - 1):
            self.add_piece(move.piece.color, 'Queen', move.dest_file, move.dest_rank)
        else:
            self.__board[move.dest_rank][move.dest_file] = self.__board[move.piece.rank][move.piece.file]
        self.__board[move.dest_rank][move.dest_file].moved()
        self.__board[move.piece.rank][move.piece.file] = None
        self.__board[move.dest_rank][move.dest_file].file = move.dest_file
        self.__board[move.dest_rank][move.dest_file].rank = move.dest_rank
        self.player_turn = 'White' if self.player_turn == 'Black' else 'Black'

    def get_legal_moves(self, color):
        legal_moves = []
        if color == 'White':
            for piece in self.white_pieces:
                legal_moves.extend(piece.get_legal_moves(self))
        else:
            for piece in self.black_pieces:
                legal_moves.extend(piece.get_legal_moves(self))
        return legal_moves
    
    def get_opponent_value(self, value):
        return -value

    def get_next_state(self, state, move):
        next_state = copy.deepcopy(state)
        next_state.push(move)
        return next_state

    def get_value_and_terminal(self, state, move): # TODO
        self.__board = state.__board
        self.player_turn = state.player_turn
        self.push(move)
        if self.win_state is not None:
            if self.win_state == 'White':
                return (100, True)
            else:
                return (-100, True)
        return (0, False)

    @property
    def win_state(self):
        return self.__win_state
