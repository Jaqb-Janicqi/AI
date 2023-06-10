from board import Game, ActionSpace
from gui import Gui
# from mcts_alphazero import MCTS_alpha_zero
from mcts_alphazero_keep_branches import MCTS_alpha_zero
import res_net as net
import time
from alphazero import AlphaZero
import torch

# initialise chess board
chess = Game(6)

# env
train_alphazero = True
load_model = True
execution_times = False

# temp -> inf: explore, temp -> 0: exploit, temp -> 1: no change
# changes to temperature are exponential
args = { 
    'num_searches': 1600,                       # 1600
    'C': 2,                                     # 2  const!
    'num_iterations': 2,                        # 16
    'num_self_play_iterations': 4,             # 128
    'num_epochs': 2,                            # 16
    'batch_size': 16,                           # 32
    'temperature': 100,                         # 100
    'weight_decay': 0.01,                       # 0.0001
    'learning_rate': 0.2,                      # 0.001
    'momentum': 0.9,                            # 0.9
    'save_interval': 1,                         # 2
    'max_game_length': 200,                     # 250
    'depth_limit': 12,                          # 20
}

num_residual_blocks = 16
num_hidden_layers = 64

model = net.ResNet(chess, num_residual_blocks, num_hidden_layers)
optimizer = torch.optim.Adam(
    model.parameters(),
    lr= args['learning_rate'],
    weight_decay= args['weight_decay'],
    amsgrad=True
    )
mcts = MCTS_alpha_zero(chess, args, model, execution_times)

if train_alphazero:
    alphazero = AlphaZero(chess, optimizer, model, args, execution_times)
    tic = time.perf_counter()
    alphazero.learn()
    toc = time.perf_counter()
    print(f'Training took {toc - tic:0.4f} seconds')
if load_model:
    model.load_state_dict(torch.load(f'models/model_{args["num_iterations"] - 1}.pt'))

gui = Gui(chess, mcts)