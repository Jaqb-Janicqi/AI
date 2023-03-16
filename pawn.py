from piece import Piece

class Pawn(Piece):
    def __init__(self, color): # color, type, file, rank
        super().__init__(color, 'Pawn')
