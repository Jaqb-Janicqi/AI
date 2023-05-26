from board import Board
from gui import Gui
from mcts_alphazero import MCTS_alphaZero
from mcts import MCTS
import res_net as net
import time

# initialise chess board
board_size = 6
chess = Board(board_size)
# measure time
tic = time.time()
action_space = chess.calculate_action_space()
toc = time.time()
print('Time to calculate action space: ', toc - tic)
chess.action_space_size = len(action_space)
chess.action_space = action_space
chess.setup()

model = net.ResNet(chess, chess.action_space_size, chess.size**2)



alphazero = True
if alphazero:
    args = { 
    'num_searches': 10, # 200
    'C': 2
    }
    mcts = MCTS_alphaZero(chess, args, model, action_space)
    # mcts.search(chess)
else:
    args = { 
    'num_searches': 200, # 200
    'C': 1.41
    }
    mcts = MCTS(chess, args)
gui = Gui(chess, mcts)

# gui = Gui(chess, mcts)