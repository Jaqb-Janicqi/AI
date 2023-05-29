class Move:
    def __init__(self, source_file: int, source_rank: int, dest_file: int, dest_rank: int, piece_char: str = 'None'):
        self.source_file: int = source_file
        self.source_rank: int = source_rank
        self.dest_file: int = dest_file
        self.dest_rank: int = dest_rank
        self.piece_char: str = piece_char

    def __str__(self):
        return f'piece: {self.piece_char}, source: {self.source_file}, {self.source_rank}, dest: {self.dest_file}, {self.dest_rank}'