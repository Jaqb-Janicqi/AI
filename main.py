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

# env
train_alphazero = False
load_model = True
execution_times = False

args = { 
    'num_searches': 50,            # 200
    'C': 2,                        # 2  const!
    'num_iterations': 3,           # 16
    'num_self_play_iterations': 2, # 160
    'num_epochs': 4,               # 16
    'batch_size': 32,              # 32
}

model = net.ResNet(chess, chess.size**2, chess.size**3)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
mcts = MCTS_alphaZero(chess, args, model, execution_times)

if train_alphazero:
    alphazero = AlphaZero(chess, optimizer, model, args, execution_times)
    alphazero.learn()
if load_model:
    model.load_state_dict(torch.load(f'models/model_{args["num_iterations"] - 1}.pt'))

gui = Gui(chess, mcts)