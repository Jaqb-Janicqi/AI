from piece import Piece

class King(Piece):
    def __init__(self, color, file, rank): # color, type, file, rank
        super().__init__(color, 'King', file, rank)
        self.__can_castle = True

    def moved(self):
        self.__can_castle = False

    # def get_moves(self, board):
    #     self.moves = []
    #     for file in range(self.file - 1, self.file + 1):
    #         for rank in range(self.rank - 1, self.rank + 1):
    #             if board.is_valid_move((file, rank), self.color) and not board.is_attacked((file, rank), self.color):
    #                 self.moves.append((file, rank))

    #     if self.can_castle:
    #         # check if king can castle
    #         # check if rooks can castle
    #         # check if squares between king and rook are empty
    #         # check if king and rook are not in check
    #         # check if king does not pass through a square that is attacked by an enemy piece
    #         pass # TODO