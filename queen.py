from piece import Piece

class Queen(Piece):
    def __init__(self, color): # color, type, file, rank
        super().__init__(color, 'Queen')
