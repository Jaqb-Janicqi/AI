from piece import Piece
from move import Move


class Knight(Piece):
    def __init__(self, color, file, rank):  # color, type, file, rank
        super().__init__(color, 'Knight', file, rank)

    def generate_moves(self, board):
        self.moves = []
        for file_dir, rank_dir in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                   (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            if board.is_in_bounds((self.file + file_dir, self.rank + rank_dir)):
                if not board.is_occupied_by_same_color(
                        (self.file + file_dir, self.rank + rank_dir), self.color):
                    move = Move(self, self.file + file_dir,
                                self.rank + rank_dir, None, None, None, None)
                    self.moves.append(move)
