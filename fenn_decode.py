# fenn notation piece decoder

def fenn_char(color, type):
    if color == 'White':
        if type == 'Pawn':
            return 'P'
        elif type == 'Knight':
            return 'N'
        elif type == 'Bishop':
            return 'B'
        elif type == 'Rook':
            return 'R'
        elif type == 'Queen':
            return 'Q'
        elif type == 'King':
            return 'K'
        else:
            return ' '
    else:
        if type == 'Pawn':
            return 'p'
        elif type == 'Knight':
            return 'n'
        elif type == 'Bishop':
            return 'b'
        elif type == 'Rook':
            return 'r'
        elif type == 'Queen':
            return 'q'
        elif type == 'King':
            return 'k'
        else:
            return ' '