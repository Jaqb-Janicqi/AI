from piece import Piece
from move import Move


class Pawn(Piece):
    def __init__(self, color, file, rank):  # color, type, file, rank
        super().__init__(color, 'Pawn', file, rank)

    def generate_moves(self, board):
        self.moves = []
        direction = 1 if self.color == 'White' else -1
        if self.is_in_bounds(self.file, self.rank + direction, board[0].size):
            dest_square = board[self.rank + direction][self.file]
            if dest_square == 0:
                move = Move(self.file, self.rank, self.file, self.rank + direction, self.fenn)
                self.moves.append(move)
        if self.is_in_bounds(self.file + 1, self.rank + direction, board[0].size): 
            dest_square = board[self.rank + direction][self.file + 1]
            if dest_square != 0 and dest_square.color != self.color:
                move = Move(self.file, self.rank, self.file + 1, self.rank + direction, self.fenn)
                self.moves.append(move)
        if self.is_in_bounds(self.file - 1, self.rank + direction, board[0].size):
            dest_square = board[self.rank + direction][self.file - 1]
            if dest_square != 0 and dest_square.color != self.color:
                move = Move(self.file, self.rank, self.file - 1, self.rank + direction, self.fenn)
                self.moves.append(move)
