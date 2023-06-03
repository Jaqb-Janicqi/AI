from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from piece import Piece
from decode_fenn_piece import type_from_char
from move import Move
import copy
import numpy as np


class ActionSpace:
    def __init__(self, size) -> None:
        self.action_space = []
        self.action_space_size = 0
        self.board_size = size
        self.piece_offsets = {
            'r': np.zeros((size, size), dtype=np.uint16),
            'n': np.zeros((size, size), dtype=np.uint16),
            'q': np.zeros((size, size), dtype=np.uint16),
            'k': np.zeros((size, size), dtype=np.uint16),
            'p': np.zeros((size, size), dtype=np.uint16),
            'P': np.zeros((size, size), dtype=np.uint16),
        }

    def encode(self, move: Move) -> int:
        piece_char = move.piece_char.lower() if move.piece_char != 'P' else move.piece_char
        piece_offset = self.piece_offsets[piece_char][move.source_rank][move.source_file]
        for i in range(piece_offset, self.action_space_size):
            if self.action_space[i].source_rank == move.source_rank and \
                self.action_space[i].source_file == move.source_file and \
                self.action_space[i].dest_rank == move.dest_rank and \
                self.action_space[i].dest_file == move.dest_file:
                return i
        raise Exception('Move not found in action space')
    
    def decode(self, action: int) -> Move:
        return self.action_space[action]
    

class State:
    def __init__(self, board: np.ndarray, board_size: int, player_turn: str) -> None:
        self.board: np.ndarray = board
        self.board_size: int = board_size
        self.player_turn: str = player_turn
        self.win_state: str = ''

    def get_legal_moves(self):
        legal_moves = []
        for rank in range(self.board_size):
            for file in range(self.board_size):
                if self.board[rank][file] != 0:
                    if self.board[rank][file].color == self.player_turn:
                        piece = self.board[rank][file]
                        piece.generate_moves(self.board)
                        legal_moves.extend(piece.moves)
                        piece.moves = []
        return legal_moves
    
    def copy(self):
        return copy.deepcopy(self)
    
    def value(self):
        if self.win_state == 'White':
            return 1
        elif self.win_state == 'Black':
            return -1
        return 0

    def encode(self):
        encoded_white = np.zeros((self.board_size, self.board_size)).astype(np.float32)
        encoded_black = np.zeros((self.board_size, self.board_size)).astype(np.float32)
        encoded_blank = np.zeros((self.board_size, self.board_size)).astype(np.float32)
        for rank in range(self.board_size):
            for file in range(self.board_size):
                if self.board[rank][file] != 0:
                    if self.board[rank][file].color == 'White':
                        encoded_white[rank][file] = self.board[rank][file].id
                    else:
                        encoded_black[rank][file] = self.board[rank][file].id
                else:
                    encoded_blank[rank][file] = 1.0
        encoded_state = np.stack((encoded_white, encoded_black, encoded_blank)).astype(np.float32)
        return encoded_state


class Game:
    def __init__(self, size: int):
        self.size: int = size
        self.state: State = self.setup()
        self.player_color: str = "White"
        self.moves: list = []
        self.action_space: ActionSpace = self.calculate_action_space()

    def print(self, board, action_taken=None):  # print matrix of the board with fenn notation for pieces
        for rank in range(self.size):
            print(rank, end='  ')
            for file in range(self.size):
                if action_taken != None and \
                    self.action_space.decode(action_taken).source_rank == rank and \
                        self.action_space.decode(action_taken).source_file == file:
                    print('X', end=' ')
                elif board[rank][file] == 0:
                    print(' ', end=' ')
                else:
                    print(board[rank][file], end=' ')
                if file == self.size - 1:
                    print()
        print()
        print('   ', end='')
        for file in range(self.size):
            print(file, end=' ')
        print()
        print()

    def add_piece(self, color, piece_type, file, rank, board) -> None:
        # add piece based on type
        if piece_type == 'Pawn':
            board[rank][file] = Pawn(color, file, rank)
        elif piece_type == 'Knight':
            board[rank][file] = Knight(color, file, rank)
        elif piece_type == 'Rook':
            board[rank][file] = Rook(color, file, rank)
        elif piece_type == 'Queen':
            board[rank][file] = Queen(color, file, rank)
        elif piece_type == 'King':
            board[rank][file] = King(color, file, rank)
        else:
            pass

    def setup(self) -> State:
        return self.fenn_decode('rnqknr/pppppp///PPPPPP/RNQKNR')
        # self.fenn_decode('4kr/2r1n1/p1pq1P/PpP3/RPQ3/K5')
        # self.player_turn = "White"
        # self.fenn_decode('/P///p/')
        # self.fenn_decode('/////')
        # self.fenn_decode('k/K')
        # self.fenn_decode('kqq/////K')
        # self.fenn_decode('r1k2r/p1pppp/q1nn/P2PPP/RPPQ/1N1KNR')

    def fenn_decode(self, fenn_string) -> State:
        board: np.ndarray = np.zeros((self.size, self.size), dtype=Piece)
        player_turn: str = "White"
        state: State = State(board, self.size, player_turn)
        file: int = 0
        rank: int = 0
        for char in fenn_string:
            if char == '/':
                file = 0
                rank += 1
            elif char.isdigit():
                file += int(char)
            else:
                (color, piece_type) = type_from_char(char)
                self.add_piece(color, piece_type, file, self.size - 1 - rank, state.board)
                file += 1
        return state

    def save_to_fenn(self, filename, board=None) -> None:
        if board is None:
            board = self.state.board
        fenn_string = ''
        for rank in range(self.size):
            empty_count = 0
            for file in range(self.size):
                if board[rank][file] == 0:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fenn_string += str(empty_count)
                        empty_count = 0
                    fenn_string += board[rank][file].fenn  # type: ignore
            if empty_count > 0:
                fenn_string += str(empty_count)
            if rank < self.size - 1:
                fenn_string += '/'

        # fenn_string = fenn_string[::-1]
        with open(filename, 'w') as f:
            f.write(fenn_string)
        f.close()

    def square(self, file, rank):   # gui use
        return self.state.board[rank][file]

    def push(self, move_id: int, state: State):
        move = self.action_space.decode(move_id)

        target_square = state.board[move.dest_rank][move.dest_file]
        if target_square != 0:
            if target_square.piece_type == 'King':
                state.win_state = state.player_turn

        source_square = state.board[move.source_rank][move.source_file]
        if source_square == 0:
            return False

        if source_square.piece_type == 'Pawn' and (move.dest_rank == 0 or move.dest_rank == state.board_size - 1):
            target_square = Queen(state.player_turn, move.dest_file, move.dest_rank)
        else:
            target_square = source_square
        target_square.file = move.dest_file
        target_square.rank = move.dest_rank
        state.board[move.dest_rank][move.dest_file] = target_square
        state.board[move.source_rank][move.source_file] = 0
        state.player_turn = 'White' if state.player_turn == 'Black' else 'Black'
        return True

    def get_next_state(self, state: State, move: int):
        next_state = state.copy()
        self.push(move, next_state)
        return next_state

    def is_in_bounds(self, file, rank, board_size):
        return 0 <= file < board_size and 0 <= rank < board_size

    def calculate_action_space(self):
        actions = []
        pieces = ['r', 'n', 'q', 'k']
        board = np.zeros((self.size, self.size), dtype=Piece)
        action_space = ActionSpace(self.size)
        for piece_char in pieces:
            for file in range(self.size):
                for rank in range(self.size):
                    action_space.piece_offsets[piece_char][rank][file] = len(actions)
                    self.add_piece('White', type_from_char(piece_char)[1], file, rank, board)
                    board[rank][file].generate_moves(board)
                    actions.extend(board[rank][file].moves)
                    board[rank][file] = 0

        piece_char = 'p'
        for file in range(self.size):
            for rank in range(1, self.size):
                action_space.piece_offsets[piece_char][rank][file] = len(actions)
                color, piece_type = type_from_char(piece_char)
                self.add_piece(color, piece_type, file, rank, board)
                for file_offset, rank_offset in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    if self.is_in_bounds(file + file_offset, rank + rank_offset, self.size):
                        if piece_char == 'P':
                            self.add_piece('Black', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset, board)
                        else:
                            self.add_piece('White', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset, board)
                board[rank][file].generate_moves(board)
                actions.extend(board[rank][file].moves)
                board = np.zeros((self.size, self.size), dtype=Piece)

        piece_char = 'P'
        for file in range(self.size):
            for rank in range(self.size - 1):
                action_space.piece_offsets[piece_char][rank][file] = len(actions)
                color, piece_type = type_from_char(piece_char)
                self.add_piece(color, piece_type, file, rank, board)
                for file_offset, rank_offset in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    if self.is_in_bounds(file + file_offset, rank + rank_offset, self.size):
                        if piece_char == 'P':
                            self.add_piece('Black', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset, board)
                        else:
                            self.add_piece('White', type_from_char(piece_char)[1], file + file_offset, rank + rank_offset, board)
                board[rank][file].generate_moves(board)
                actions.extend(board[rank][file].moves)
                board = np.zeros((self.size, self.size), dtype=Piece)
    
        action_space.action_space = actions
        action_space.action_space_size = len(actions)
        print(f'Action space size: {action_space.action_space_size}')
        return action_space


    @property
    def win_state(self):
        return self.state.win_state
