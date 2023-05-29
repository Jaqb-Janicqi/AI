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
train_alphazero = True
load_model = False
execution_times = False


# temp -> inf: explore, temp -> 0: exploit, temp -> 1: no change
# changes to temperature are exponential
args_fast = { 
    'num_searches': 50,                         # 200
    'C': 2,                                     # 2  const!
    'num_iterations': 2,                        # 16
    'num_self_play_iterations': 2,              # 128
    'num_epochs': 2,                            # 16
    'batch_size': 32,                           # 32
    'temperature': 1.25,                        # 1.25
}

args_slow = { 
    'num_searches': 100,                         # 200
    'C': 2,                                     # 2  const!
    'num_iterations': 8,                       # 16
    'num_self_play_iterations': 32,            # 128
    'num_epochs': 16,                           # 16
    'batch_size': 32,                           # 32
    'temperature': 1.05,                        # 1.25
}
args = args_slow

# model size = board_size^3 / scaler
hidden_scaler = 3
residual_scaler = 1.5

model = net.ResNet(chess, int((chess.size**3)/residual_scaler), int((chess.size**3)/hidden_scaler))
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
mcts = MCTS_alphaZero(chess, args, model, execution_times)

if train_alphazero:
    alphazero = AlphaZero(chess, optimizer, model, args, execution_times)
    tic = time.perf_counter()
    alphazero.learn()
    toc = time.perf_counter()
    print(f'Training took {toc - tic:0.4f} seconds')
if load_model:
    model.load_state_dict(torch.load(f'models/model_{args["num_iterations"] - 1}.pt'))

gui = Gui(chess, mcts)