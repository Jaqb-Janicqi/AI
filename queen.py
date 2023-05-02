from piece import Piece


class Queen(Piece):
    def __init__(self, color, file, rank):  # color, type, file, rank
        super().__init__(color, 'Queen', file, rank)

    def generate_moves(self, board):
        self.moves = []
        self.generate_horizontal_vertical_moves(board, 999)
        self.generate_diagonal_moves(board, 999)
