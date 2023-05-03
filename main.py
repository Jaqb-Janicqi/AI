from board import Board
from gui import Gui


# initialise chess board
board_size = 6
board = Board(board_size)
# board.fenn_decode('//2K/1qkrn//')

# initialise gui
gui = Gui(board)
