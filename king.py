from piece import Piece

class King(Piece):
    def __init__(self, color): # color, type, file, rank
        super().__init__(color, 'King')
        self.can_castle = True
        self.move_set.append(0,1) # file, rank
        self.move_set.append(0,-1)
        self.move_set.append(1,0)
        self.move_set.append(-1,0)
        self.move_set.append(1,1)
        self.move_set.append(1,-1)
        self.move_set.append(-1,1)
        self.move_set.append(-1,-1)
