import numpy as np

from move import Move


class State:
    def __init__(self, board, player_turn, win=np.int8(0), moves=[]) -> None:
        self.board: np.ndarray = board
        self.player_turn: np.int8 = player_turn
        self.win: np.int8 = win
        self.legal_moves: list[int] = moves

    def next_state(self, move: Move) -> 'State':
        new_board = self.board.copy()
        piece_id = abs(new_board[move.src_rank, move.src_file])
        captured_piece_id = abs(new_board[move.dst_rank, move.dst_file])
        win = np.int8(0)

        if captured_piece_id == 5:
            # King capture and win state change
            win = self.player_turn
        if piece_id == 1:
            # Pawn promotion to queen
            if move.dst_rank == 0 or move.dst_rank == self.board.shape[0] - 1:
                new_board[move.src_rank, move.src_file] = 4 * \
                    self.player_turn

        new_board[move.dst_rank,
                  move.dst_file] = new_board[move.src_rank, move.src_file]
        new_board[move.src_rank, move.src_file] = 0
        new_player_turn = self.player_turn * -1
        return State(new_board, new_player_turn, win)

    def encode(self) -> np.ndarray:
        temp = self.board.copy()
        if self.player_turn == -1:
            # Flip the board and multiply by -1 to change the perspective
            temp = np.flip(temp, axis=(0, 1)) * -1
        return temp

    def is_terminal(self) -> bool:
        return self.win != 0

    def __hash__(self) -> int:
        return hash((self.board.tostring(), self.player_turn))

    def get_hash(self) -> int:
        return self.__hash__()

    def square(self, rank, file) -> np.int8:
        return self.board[rank][file]
