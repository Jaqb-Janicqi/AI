from piece import Piece

class Knight(Piece):
    def __init__(self, color, file, rank): # color, type, file, rank
        super().__init__(color, 'Knight', file, rank)
        self.__range = (1,1,0) # (file, rank, diagonal)
