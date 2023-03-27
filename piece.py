from decode_fenn_piece import char_from_type
from move import Move

class Piece:
    def __init__(self, color, type, file, rank):
        self.__color = color
        self.__type = type
        self.__file = file
        self.__rank = rank
        self.__sliding = False
        self.__diagonal = False
        self.__can_promote = False
        self.__can_castle = False
        self.__range = (0,0,0) # (file, rank, diagonal), negative values are unlimited
        self.__fenn = char_from_type(color, type)
        self.__id = self.assign_id()
        self.__moves = []

    def assign_id(self):
        # assign a unique id to each piece
        # this is not implemented in particular pieces to ease id management
        if self.__type == 'Pawn':
            return 1
        elif self.__type == 'Knight':
            return 2
        elif self.__type == "Rook":
            return 3
        elif self.__type == "Queen":
            return 4
        elif self.__type == "King":
            return 5
        else:
            return 0

    def __str__(self):
        # return f"{self.color} {self.type}, value: {self.value}"
        return f"{self.__fenn}"
    
    def moved(self): 
        # this function is called on every move one makes
        # will be implemented by pieces that have conditional moves like castlig
        pass

    def bound_move(self, file, rank, board_size):
        # check if move is within bounds of the board and if not correct it
        if file < 0:
            file = 0
        elif file >= board_size:
            file = board_size - 1
        if rank < 0:
            rank = 0
        elif rank >= board_size:
            rank = board_size - 1
        return file, rank

    def generate_moves(self, board):
        # implemented for specific pieces
        pass

    def generate_sliding_move(self, board):
        file_left, rank = self.bound_move(self.file - self.__range[0], self.rank, board.size)
        file_right, rank = self.bound_move(self.file + self.__range[0], self.rank, board.size)
        for file in range(file_left, file_right + 1):
            if board.is_occupied_by_color(file, rank, self.color):
                yield Move(self, file, rank, None, None, None, None)
            else:
                break

    def generate_diagonal_moves(self, board): # this does not work becouse of bound_move
        file_left, rank_up = self.bound_move(self.file - self.__range[2], self.rank + self.__range[2], board.size)
        file_right, rank_down = self.bound_move(self.file + self.__range[2], self.rank - self.__range[2], board.size)
        for i in range(file_left, file_right + 1):
            file = ra
                if board.is_occupied_by_color(file, rank, self.color):
                    yield Move(self, file, rank, None, None, None, None)
                else:
                    break

    @property
    def range(self):
        return self.__range
    
    @property
    def can_castle(self):
        return self.__can_castle
    
    @property
    def sliding(self):
        return self.__sliding
    
    @property
    def diagonal(self):
        return self.__diagonal
    
    @property
    def can_promote(self):
        return self.__can_promote
    
    @property
    def color(self):
        return self.__color
    
    @property
    def type(self):
        return self.__type
    
    @property
    def file(self):
        return self.__file
    
    @property
    def rank(self):
        return self.__rank
    
    @property
    def fenn(self):
        return self.__fenn
    
    @property
    def id(self):
        return self.__id
    
    @property
    def moves(self):
        return self.__moves