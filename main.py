from board import Board
from gui import Gui
from mcts import MCTS


# initialise chess board
board_size = 6
chess = Board(board_size)

args = { 
    'num_searches': 200, # 200
    'C': 1.41
}
mcts = MCTS(chess, args)

# initialise gui and mcts
gui = Gui(chess, mcts)