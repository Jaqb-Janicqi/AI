import numpy as np


class Move:
    def __init__(self, src_rank: np.uint8, src_file: np.uint8,
                 dst_rank: np.uint8, dst_file: np.uint8):
        self.src_rank: np.uint8 = src_rank
        self.src_file: np.uint8 = src_file
        self.dst_rank: np.uint8 = dst_rank
        self.dst_file: np.uint8 = dst_file

    def __hash__(self):
        return hash((self.src_rank, self.src_file, self.dst_rank, self.dst_file))

    def __str__(self) -> str:
        return f'{self.src_rank}{self.src_file}{self.dst_rank}{self.dst_file}'
