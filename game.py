from time import perf_counter_ns

import numpy as np

from state import State


class Game:
    def __init__(self) -> None:
        self.move_functions = {
            1: self.generate_pawn,
            2: self.generate_knight,
            3: self.generate_sliding,
            4: self.generate_sliding,
            5: self.generate_sliding
        }
        self.move_range = {
            1: 1,
            2: 1,
            3: 2,
            4: 999,
            5: 1
        }
        self.avg_move_time = 0

    def bind_move(self, rank, file, board_size) -> tuple[int, int]:
        rank = max(0, min(rank, board_size - 1))
        file = max(0, min(file, board_size - 1))
        return rank, file

    def is_in_bounds(self, rank, file, board_size) -> bool:
        return 0 <= file < board_size and 0 <= rank < board_size

    def get_color(self, piece_id: np.int8) -> np.int8:
        return 1 if piece_id > 0 else -1

    def generate_sliding(self, board: np.ndarray, src_rank: np.uint8,
                         src_file: np.uint8) -> list[int]:
        piece_id = abs(board[src_rank][src_file])
        move_range = self.move_range[piece_id]
        start_rank, start_file = self.bind_move(
            src_rank - move_range,
            src_file - move_range,
            board.shape[0])
        end_rank, end_file = self.bind_move(
            src_rank + move_range,
            src_file + move_range,
            board.shape[0])

        player_color = self.get_color(board[src_rank][src_file])

        # include diagonal moves for the queen
        if piece_id == 4 or piece_id == 5:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                          (1, 1), (-1, 1), (1, -1), (-1, -1)]
        else:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        move_hashes = []

        for rank_dir, file_dir in directions:
            rank, file = src_rank + rank_dir, src_file + file_dir
            while start_rank <= rank <= end_rank and start_file <= file <= end_file:
                square = board[rank][file]
                if board[rank][file] != 0 and self.get_color(board[rank][file]) == player_color:
                    break
                move_hashes.append(hash((src_rank, src_file, rank, file)))
                if board[rank][file] != 0:
                    break
                rank += rank_dir
                file += file_dir
        return move_hashes

    def generate_knight(self, board: np.ndarray, src_rank: np.uint8,
                        src_file: np.uint8) -> list[int]:
        player_color = self.get_color(board[src_rank][src_file])
        move_hashes = []
        for file_dir, rank_dir in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                   (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            rank, file = src_rank + rank_dir, src_file + file_dir
            if self.is_in_bounds(rank, file, board.shape[0]):
                if board[rank][file] != 0 and self.get_color(board[rank][file]) == player_color:
                    pass
                else:
                    move_hashes.append(hash((src_rank, src_file, rank, file)))
        return move_hashes

    def generate_pawn(self, board: np.ndarray, src_rank: np.uint8,
                      src_file: np.uint8) -> list[int]:
        player_color = self.get_color(board[src_rank][src_file])
        rank = src_rank + player_color
        move_hashes = []
        if self.is_in_bounds(rank, src_file, board.shape[0]):
            if board[rank][src_file] == 0:
                move_hashes.append(hash((src_rank, src_file, rank, src_file)))

        for side_dir in [-1, 1]:
            file = src_file + side_dir
            player_color = self.get_color(board[src_rank][src_file])
            if self.is_in_bounds(rank, file, board.shape[0]):
                if board[rank][file] != 0:
                    if self.get_color(board[rank][file]) != player_color:
                        move_hashes.append(
                            hash((src_rank, src_file, rank, file)))
        return move_hashes

    def generate_moves(self, board: np.ndarray, player_turn: np.int8) -> list[int]:
        move_hashes = []
        for rank in range(board.shape[0]):
            for file in range(board.shape[1]):
                if board[rank][file] != 0 and self.get_color(board[rank][file]) == player_turn:
                    piece_id = abs(board[rank][file])
                    move_hashes.extend(
                        self.move_functions[piece_id](board, rank, file))
        return move_hashes

    def generate_one_piece(self, board: np.ndarray, src_rank: np.uint8, src_file: np.uint8) -> list[int]:
        move_hashes = []
        if board[src_rank][src_file] != 0:
            piece_id = abs(board[src_rank][src_file])
            move_hashes.extend(self.move_functions[piece_id](
                board, src_rank, src_file))
        return move_hashes

    def fenn_decode(self, fenn_string, board_size: int) -> State:
        piece_dict = {
            'P': 1,
            'N': 2,
            'R': 3,
            'Q': 4,
            'K': 5,
            'p': -1,
            'n': -2,
            'r': -3,
            'q': -4,
            'k': -5
        }
        board: np.ndarray = np.zeros((board_size, board_size), dtype=np.int8)
        player_turn: np.int8 = np.int8(1)
        state: State = State(board, player_turn)
        file: int = 0
        rank: int = board_size - 1
        for char in fenn_string:
            if char == '/':
                file = 0
                rank -= 1
            elif char.isdigit():
                file += int(char)
            elif char in piece_dict:
                board[rank][file] = piece_dict[char]
                file += 1
            else:
                raise ValueError(f'Unsupported character {char} in FEN string')
        return state

    def load_default(self, board_size: int) -> State:
        return self.fenn_decode('rnqknr/pppppp///PPPPPP/RNQKNR', board_size)
