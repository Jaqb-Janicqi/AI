from board import Game, ActionSpace
from gui import Gui
from mcts_alphazero import MCTS_alphaZero
from mcts import MCTS
import res_net as net
import time
from alphazero import AlphaZero
import torch

# initialise chess board
chess = Game(6)

use_alphazero = True
if use_alphazero:
    args = { 
        'num_searches': 50, # 200
        'C': 2,
        'num_iterations': 4,
        'num_self_play_iterations': 10,
        'num_epochs': 4
    }
    model = net.ResNet(chess, chess.size**2, chess.size**3)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    mcts = MCTS_alphaZero(chess, args, model)
    alphazero = AlphaZero(chess, optimizer, model, args)
    alphazero.learn()
    # mcts.search(chess)
else:
    args = { 
        'num_searches': 50, # 200
        'C': 1.41
    }
    mcts = MCTS(chess, args)

gui = Gui(chess, mcts)