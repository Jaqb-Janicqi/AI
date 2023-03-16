# fenn notation piece decoder

def char_from_type(color, type):
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
        
def type_from_char(char):
    if char.isupper():
        color = 'White'
    else:
        color = 'Black'
        char = char.upper()

    if char == 'P':
        return (color, 'Pawn')
    elif char == 'N':
        return (color, 'Knight')
    elif char == 'B':
        return (color, 'Bishop')
    elif char == 'R':
        return (color, 'Rook')
    elif char == 'Q':
        return (color, 'Queen')
    elif char == 'K':
        return (color, 'King')
    else:
        return ('', '')