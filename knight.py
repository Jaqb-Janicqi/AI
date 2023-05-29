from piece import Piece
from move import Move


class Knight(Piece):
    def __init__(self, color, file, rank):  # color, type, file, rank
        super().__init__(color, 'Knight', file, rank)

    def generate_moves(self, board):
        self.moves = []
        for file_dir, rank_dir in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                   (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            dest_rank, dest_file = self.rank + rank_dir, self.file + file_dir
            if self.is_in_bounds(dest_rank, dest_file, board[0].size):
                if board[dest_rank][dest_file] != 0 and board[dest_rank][dest_file].color == self.color:
                    pass
                else:
                    move = Move(self.file, self.rank, dest_file, dest_rank, self.fenn)
                    self.moves.append(move)
