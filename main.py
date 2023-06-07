from board import Game, ActionSpace
from gui import Gui
from mcts_alphazero import MCTS_alphaZero
# from mcts_alphazero_keep_branches import MCTS_alphaZero
import res_net as net
import time
from alphazero import AlphaZero
import torch
torch.manual_seed(0)

# initialise chess board
chess = Game(6)

# env
train_alphazero = False
load_model = False
execution_times = False
fast = True


# temp -> inf: explore, temp -> 0: exploit, temp -> 1: no change
# changes to temperature are exponential
args = { 
    'num_searches': 5,                          # 200
    'C': 2,                                     # 2  const!
    'num_iterations': 32,                        # 16
    'num_self_play_iterations': 64,              # 128
    'num_epochs': 4,                            # 16
    'batch_size': 32,                           # 32
    'temperature': 1000,                        # 1.25
    'weight_decay': 0.01,                       # 0.0001
    'learning_rate': 0.1,                       # 0.001
    'momentum': 0.9                             # 0.9
}

# model size = board_size^3 / scaler
hidden_scaler = 3
residual_scaler = 1

model = net.ResNet(chess, int((chess.size**3)/residual_scaler), int((chess.size**3)/hidden_scaler))
optimizer = torch.optim.Adam(model.parameters(), lr= args['learning_rate'], weight_decay= args['weight_decay'], amsgrad=True)
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