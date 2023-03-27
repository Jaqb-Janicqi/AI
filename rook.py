from piece import Piece

class Rook(Piece):
    def __init__(self, color, file, rank): # color, type, file, rank
        super().__init__(color, 'Rook', file, rank)
        self.__can_castle = True
        self.__sliding = True
        self.__range = (2,2,0) # (file, rank, diagonal)

    def moved(self):
        self.__can_castle = False