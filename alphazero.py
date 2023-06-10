import mcts_alphazero_keep_branches as mcts
import torch
import torch.nn.functional as F
import numpy as np
import random
from tqdm import trange, tqdm

class AlphaZero:
    def __init__(self, game, optimizer, model, args, execution_times):
        self.game = game
        self.optimizer = optimizer
        self.model = model
        self.args = args
        self.action_space = game.action_space
        self.mcts = mcts.MCTS_alpha_zero(game, args, model, execution_times)
        self.max_game_length = args['max_game_length']

    def train(self, training_data):
        random.shuffle(training_data)
        for batch_index in range(0, len(training_data), self.args['batch_size']):
            if batch_index == len(training_data) - 1: # list[x:x] = []
                break

            batch = training_data[batch_index:min(len(training_data) - 1, batch_index + self.args['batch_size'])]
            state, policy_targets, value_targets = zip(*batch)
            
            state, policy_targets, value_targets = \
                np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)
            
            state = torch.tensor(state, dtype=torch.float32)
            policy_targets = torch.tensor(policy_targets, dtype=torch.float32)
            value_targets = torch.tensor(value_targets, dtype=torch.float32)
            
            out_policy, out_value = self.model(state)
            
            policy_loss = F.cross_entropy(out_policy, policy_targets)
            value_loss = F.mse_loss(out_value, value_targets)
            loss = policy_loss + value_loss
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def self_play(self):
        memory = []
        self.game.setup()
        state = self.game.state.copy()
        player = 'White'

        pbar = tqdm(ncols=100, desc='Self play moves', leave=False)
        moves = 0
        prev_action = None
        while state.win_state == '':
            action_probs = self.mcts.search(state, prev_action)
            memory.append([state, action_probs, state.player_turn])
            action = np.random.choice(len(action_probs), p=action_probs)
            state = self.game.get_next_state(state, action)

            pbar.update(1)
            moves += 1
            prev_action = action
            if moves > self.max_game_length:
                break
        
        return_memory = []
        for mem_state, mem_action_probs, mem_player in memory:
            if mem_state.win_state == '':
                value = 0
            elif mem_player == player:
                value = 1
            else:
                value = -1

            encoded_state = mem_state.encode()
            return_memory.append([encoded_state, mem_action_probs, value])

        return return_memory

    def learn(self):
        for iteration in trange(self.args['num_iterations'], ncols=100, desc='Learning iteration', leave=False):
            memory = []

            self.model.eval()
            for self_play_iteration in trange(self.args['num_self_play_iterations'], ncols=100, desc='Self play iteration', leave=False):
                memory.extend(self.self_play())
            
            self.model.train()
            for epoch in trange(self.args['num_epochs'], ncols=100, desc='Epoch', leave=False):
                self.train(memory)

            if (iteration + 1) % self.args['save_interval'] == 0:
                torch.save(self.model.state_dict(), f'models/model_{iteration}.pt')
                torch.save(self.optimizer.state_dict(), f'models/optimizer_{iteration}.pt')
        
        if self.args['num_iterations'] % self.args['save_interval'] != 0:
            torch.save(self.model.state_dict(), f'models/model_{self.args["num_iterations"]}.pt')
            torch.save(self.optimizer.state_dict(), f'models/optimizer_{self.args["num_iterations"]}.pt')