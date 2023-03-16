from fenn_decode import fenn_char

class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.fenn = fenn_char(color, type)
        self.id = self.assign_id()
        self.value = self.__assign_value()        

    def assign_id(self):
        if self.type == 'Pawn':
            return 1
        elif self.type == 'Knight':
            return 2
        elif self.type == "Rook":
            return 3
        elif self.type == "Queen":
            return 4
        elif self.type == "King":
            return 5
        else:
            return 0

    def __assign_value(self):
        if self.type == 'Pawn':
            return 1
        elif self.type == 'Knight':
            return 3
        elif self.type == "Rook":
            return 5
        elif self.type == "Queen":
            return 9
        elif self.type == "King":
            return 255
        else:
            return 0

    def __str__(self):
        # return f"{self.color} {self.type}, value: {self.value}"
        return f"{self.fenn}"