from piece import Piece

class Queen(Piece):
    def __init__(self, color, file, rank): # color, type, file, rank
        super().__init__(color, 'Queen', file, rank)
        self.__sliding = True
        self.__diagonal = True
        self.__range = (-1,-1,-1) # (file, rank, diagonal)
