from decode_fenn_piece import char_from_type
from move import Move


class Piece:
    def __init__(self, color, piece_type, file, rank):
        self.color = color
        self.piece_type = piece_type
        self.file = file
        self.rank = rank
        self.can_promote = False
        self.can_castle = False
        self.fenn = char_from_type(color, piece_type)
        self.id = self.assign_id()
        self.moves = []

    def assign_id(self):
        # assign a unique id to each piece
        # this is not implemented in particular pieces to ease id management
        if self.piece_type == 'Pawn':
            return 1
        elif self.piece_type == 'Knight':
            return 2
        elif self.piece_type == "Rook":
            return 3
        elif self.piece_type == "Queen":
            return 4
        elif self.piece_type == "King":
            return 5
        else:
            return 0

    def generate_horizontal_vertical_moves(self, board, move_range):
        start_file, start_rank = self.bound_move(
            self.file - move_range, self.rank - move_range, board.size)
        end_file, end_rank = self.bound_move(
            self.file + move_range, self.rank + move_range, board.size)

        for file_tuple, rank_tuple in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            file, rank = self.file + file_tuple, self.rank + rank_tuple
            while start_file <= file <= end_file and start_rank <= rank <= end_rank:
                if board.is_occupied_by_same_color((file, rank), self.color):
                    break
                move = Move(self.file, self.rank, file, rank)
                self.moves.append(move)
                if board.is_occupied((file, rank)):
                    break
                file += file_tuple
                rank += rank_tuple

    def generate_diagonal_moves(self, board, move_range):
        start_file, start_rank = self.bound_move(
            self.file - move_range, self.rank - move_range, board.size)
        end_file, end_rank = self.bound_move(
            self.file + move_range, self.rank + move_range, board.size)

        for file_dir, rank_dir in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            file, rank = self.file + file_dir, self.rank + rank_dir
            while start_file <= file <= end_file and start_rank <= rank <= end_rank:
                if board.is_occupied_by_same_color((file, rank), self.color):
                    break
                move = Move(self.file, self.rank, file, rank)
                self.moves.append(move)
                if board.is_occupied((file, rank)):
                    break
                file += file_dir
                rank += rank_dir

    def __str__(self):
        # return f"{self.color} {self.type}, value: {self.value}"
        return f"{self.fenn}"

    def moved(self):
        # this function is called on every move one makes
        # will be implemented by pieces that have conditional moves like castlig
        pass

    def bound_move(self, file, rank, board_size):
        # check if move range is within bounds of the board and if not correct it
        file = max(0, min(file, board_size - 1))
        rank = max(0, min(rank, board_size - 1))
        return file, rank

    def generate_moves(self, board):
        # implemented for specific pieces
        pass
