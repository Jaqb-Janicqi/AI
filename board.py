from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from decode_fenn_piece import type_from_char
from move import Move
import copy
import numpy as np

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
        self.action_space_size = 0
        self.action_space = []

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
        print()
        print()

    def add_piece(self, color, piece_type, file, rank, board=None):
        if board == None:
            board = self.__board
        # add piece based on type
        if piece_type == 'Pawn':
            board[rank][file] = Pawn(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'Knight':
            board[rank][file] = Knight(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'Rook':
            board[rank][file] = Rook(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'Queen':
            board[rank][file] = Queen(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        elif piece_type == 'King':
            board[rank][file] = King(color, file, rank)
            if color == 'White':
                self.white_pieces.append(self.__board[rank][file])
            else:
                self.black_pieces.append(self.__board[rank][file])
        else:
            pass

    def setup(self):
        self.__board = [[None for file in range(self.size)] for rank in range(self.size)]
        self.__win_state = None
        self.player_color = "White"
        self.player_turn = "White"
        self.white_pieces = []
        self.black_pieces = []
        self.moves = []
        self.fenn_decode('rnqknr/pppppp///PPPPPP/RNQKNR')
        # self.player_turn = "White"
        # self.fenn_decode('/P///p/')
        # self.fenn_decode('/////')
        # self.fenn_decode('k/K')
        # self.fenn_decode('kqq/////K')

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

    def push(self, move, state = None):
        if state is None:
            state = self
        if isinstance(move, int):
            move = state.action_space[move]
        if state.__board[move.dest_rank][move.dest_file] is not None:
            if state.__board[move.dest_rank][move.dest_file].piece_type == 'King':
                state.__win_state = state.player_turn
        captured_piece = state.__board[move.dest_rank][move.dest_file]
        source_piece = state.__board[move.source_rank][move.source_file]
        if captured_piece is not None:
            if state.player_turn == 'White':
                state.black_pieces.remove(captured_piece)
            else:
                state.white_pieces.remove(captured_piece)
        if source_piece.piece_type is 'Pawn' and (move.dest_rank == 0 or move.dest_rank == state.size - 1):
            state.add_piece(source_piece.color, 'Queen', move.dest_file, move.dest_rank)
        else:
            state.__board[move.dest_rank][move.dest_file] = state.__board[move.source_rank][move.source_file]
        state.__board[move.dest_rank][move.dest_file].moved()
        state.__board[move.source_rank][move.source_file] = None
        state.__board[move.dest_rank][move.dest_file].file = move.dest_file
        state.__board[move.dest_rank][move.dest_file].rank = move.dest_rank
        state.player_turn = 'White' if state.player_turn == 'Black' else 'Black'

    def get_legal_moves(self, state):
        legal_moves = []
        if state.player_turn == 'White':
            for piece in state.white_pieces:
                piece.generate_moves(state)
                legal_moves.extend(piece.moves)
        else:
            for piece in state.black_pieces:
                piece.generate_moves(state)
                legal_moves.extend(piece.moves)
        return legal_moves
    
    def generate_moves(self, state):
        state.moves = state.get_legal_moves(state)

    def get_next_state(self, state, move):
        if isinstance(move, int):
            move = state.action_space[move]
        next_state = copy.deepcopy(state)
        next_state.push(move, next_state)
        next_state.generate_moves(next_state)
        return next_state

    def get_value(self, state):
        if state.win_state is not None:
            if state.win_state == 'White':
                return 1
            else:
                return -1
        return 0
    
    def is_terminal(self, state):
        if state.win_state is not None:
            return True
        return False

    def encode_state(self, state=None):
        if state is None:
            state = self
        encoded_white = np.zeros((state.size, state.size)).astype(np.float32)
        encoded_black = np.zeros((state.size, state.size)).astype(np.float32)
        encoded_blank = np.zeros((state.size, state.size)).astype(np.float32)
        for piece in state.white_pieces:
            encoded_white[piece.rank][piece.file] = np.float32(piece.id)
            encoded_blank[piece.rank][piece.file] = np.float32(piece.id)
        for piece in state.black_pieces:
            encoded_black[piece.rank][piece.file] = np.float32(piece.id)
            encoded_blank[piece.rank][piece.file] = np.float32(piece.id)
        encoded_blank = np.logical_not(encoded_blank)
        encoded_state = np.stack((encoded_white, encoded_black, encoded_blank)).astype(np.float32)
        return encoded_state
    
    def calculate_action_space(self):
        actions = []
        pieces = ['r', 'n', 'q', 'k']
        for piece_char in pieces:
            for file in range(self.size):
                for rank in range(self.size):
                    self.add_piece('White', type_from_char(piece_char)[1], file, rank)
                    self.__board[rank][file].generate_moves(self) # type: ignore
                    actions.extend(self.__board[rank][file].moves) # type: ignore
                    self.__board[rank][file] = None

        piece_char = 'p'
        for file in range(self.size):
            for rank in range(1, self.size):
                self.add_piece(type_from_char(piece_char)[0], type_from_char(piece_char)[1], file, rank)
                for file_offset, rank_offset in[(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    if self.is_in_bounds((file + file_offset, rank + rank_offset)):
                        if piece_char == 'P':
                            self.add_piece('Black', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset)
                        else:
                            self.add_piece('White', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset)
                self.__board[rank][file].generate_moves(self) # type: ignore
                actions.extend(self.__board[rank][file].moves) # type: ignore
                self.__board = [[None for file in range(self.size)] for rank in range(self.size)]

        piece_char = 'P'
        for file in range(self.size):
            for rank in range(self.size - 1):
                self.add_piece(type_from_char(piece_char)[0], type_from_char(piece_char)[1], file, rank)
                for file_offset, rank_offset in[(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    if self.is_in_bounds((file + file_offset, rank + rank_offset)):
                        if piece_char == 'P':
                            self.add_piece('Black', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset)
                        else:
                            self.add_piece('White', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset)
                self.__board[rank][file].generate_moves(self) # type: ignore
                actions.extend(self.__board[rank][file].moves) # type: ignore
                self.__board = [[None for file in range(self.size)] for rank in range(self.size)]
        return actions
    
    def encode_to_action_space(self, move):
        # from action_space return index of move having same source and dest
        for i, action in enumerate(self.action_space):
            if action.source_file == move.source_file and action.source_rank == move.source_rank and action.dest_file == move.dest_file and action.dest_rank == move.dest_rank:
                return i

    @property
    def win_state(self):
        return self.__win_state