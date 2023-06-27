from multiprocessing import Manager

from move import Move


class ActionSpace:
    '''Represents the action space of a game.'''

    def __init__(self, board_size: int):
        self.action_space = dict()
        self.id_map = dict()
        self.hash_map = dict()
        self.calculate(board_size)
        self.action_space_size = len(self.action_space)

    def get(self, key: int) -> Move:
        '''Returns the Move object associated with the given key (hash).'''
        return self.action_space[key]

    def get_by_id(self, id: int) -> Move:
        '''Returns the Move object associated with the given id.'''
        return self.action_space[self.hash_map[id]]

    def add(self, id: int, obj: Move) -> None:
        '''Adds a Move object to the action space.'''
        key = obj.__hash__()
        self.action_space[key] = obj
        self.id_map[key] = id
        self.hash_map[id] = key

    def get_id_of_move(self, obj: Move) -> int:
        '''Returns the id of the given Move object.'''
        hash_val = obj.__hash__()
        return self.id_map[hash_val]

    def get_id_of_hash(self, hash_val: int) -> int:
        '''Returns the id of the given hash.'''
        return self.id_map[hash_val]

    def calculate(self, board_size) -> None:
        '''Calculates all possible moves for a given board size.'''
        id = 0
        for src_rank in range(board_size):
            for src_file in range(board_size):
                for dst_rank in range(board_size):
                    for dst_file in range(board_size):
                        self.add(
                            id, Move(src_rank, src_file, dst_rank, dst_file))
                        id += 1

    @property
    def size(self) -> int:
        '''Returns the size of the action space.'''
        return self.action_space_size
