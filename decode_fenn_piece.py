# fenn notation piece decoder

def char_from_type(color, piece_type):
    if color == 'White':
        if piece_type == 'Pawn':
            return 'P'
        if piece_type == 'Knight':
            return 'N'
        if piece_type == 'Bishop':
            return 'B'
        if piece_type == 'Rook':
            return 'R'
        if piece_type == 'Queen':
            return 'Q'
        if piece_type == 'King':
            return 'K'
        return ' '

    if piece_type == 'Pawn':
        return 'p'
    if piece_type == 'Knight':
        return 'n'
    if piece_type == 'Bishop':
        return 'b'
    if piece_type == 'Rook':
        return 'r'
    if piece_type == 'Queen':
        return 'q'
    if piece_type == 'King':
        return 'k'
    return ' '


def type_from_char(char):
    if char.isupper():
        color = 'White'
    else:
        color = 'Black'
        char = char.upper()

    if char == 'P':
        return (color, 'Pawn')
    if char == 'N':
        return (color, 'Knight')
    if char == 'B':
        return (color, 'Bishop')
    if char == 'R':
        return (color, 'Rook')
    if char == 'Q':
        return (color, 'Queen')
    if char == 'K':
        return (color, 'King')
    return ('', '')
