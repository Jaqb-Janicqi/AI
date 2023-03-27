class Move:
    def __init__(self, piece, dest_file, dest_rank, castle_piece, castle_dest_rank, castle_dest_file, promote):
        self.__piece = piece
        self.__dest_file = dest_file
        self.__dest_rank = dest_rank
        self.__castle_piece = castle_piece
        self.__castle_dest_rank = castle_dest_rank
        self.__castle_dest_file = castle_dest_file
        self.__promote = promote

    @property
    def piece(self):
        return self.__piece

    @property
    def dest_file(self):
        return self.__dest_file

    @property
    def dest_rank(self):
        return self.__dest_rank
    
    @property
    def castle_piece(self):
        return self.__castle_piece
    
    @property
    def castle_dest_rank(self):
        return self.__castle_dest_rank
    
    @property
    def castle_dest_file(self):
        return self.__castle_dest_file
    
    @property
    def promote(self):
        return self.__promote
