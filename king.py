from piece import Piece

class King(Piece):
    def __init__(self, color): # color, type, file, rank
        super().__init__(color, 'King')