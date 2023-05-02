class Move:
    def __init__(self, piece, dest_file, dest_rank, castle_piece, castle_dest_rank, castle_dest_file, promote):
        self.piece = piece
        self.dest_file = dest_file
        self.dest_rank = dest_rank
        self.castle_piece = castle_piece
        self.castle_dest_rank = castle_dest_rank
        self.castle_dest_file = castle_dest_file
        self.promote = promote
