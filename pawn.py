from piece import Piece
from move import Move


class Pawn(Piece):
    def __init__(self, color, file, rank):  # color, type, file, rank
        super().__init__(color, 'Pawn', file, rank)

    def generate_moves(self, board):
        self.moves = []
        direction = 1 if self.color == 'White' else -1
        if not board.is_occupied((self.file, self.rank + direction)):
            move = Move(self, self.file, self.rank +
                        direction, None, None, None, None)
            self.moves.append(move)
        if board.is_in_bounds((self.file + 1, self.rank + direction)):
            if board.is_occupied((self.file + 1, self.rank + direction)) and not \
                    board.is_occupied_by_same_color((self.file + 1, self.rank + direction), self.color):
                move = Move(self, self.file + 1, self.rank +
                            direction, None, None, None, None)
                self.moves.append(move)
        if board.is_in_bounds((self.file - 1, self.rank + direction)):
            if board.is_occupied((self.file - 1, self.rank + direction)) and not \
                    board.is_occupied_by_same_color((self.file - 1, self.rank + direction), self.color):
                move = Move(self, self.file - 1, self.rank +
                            direction, None, None, None, None)
                self.moves.append(move)
