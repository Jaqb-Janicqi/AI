from piece import Piece
from move import Move

class King(Piece):
    def __init__(self, color, file, rank): # color, type, file, rank
        super().__init__(color, 'King', file, rank)
        self.can_castle = True

    def moved(self):
        self.can_castle = False

    def generate_moves(self, board):
        self.moves = []
        self.generate_horizontal_vertical_moves(board, 1)
        self.generate_diagonal_moves(board, 1)
