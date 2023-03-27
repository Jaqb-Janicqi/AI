from piece import Piece

class Pawn(Piece):
    def __init__(self, color, file, rank): # color, type, file, rank
        super().__init__(color, 'Pawn', file, rank)
        self.__sliding = True
        self.__range = (1,0,1) # (file, rank, diagonal)

    def generate_moves(self, board):
        direction = 1 if self.color == 'white' else -1
        for i in range(1, self.range[0] + 1):
            if board[self.file][self.rank + i * direction] is None:
                yield (self.file, self.rank + i * direction)
            else:
                break