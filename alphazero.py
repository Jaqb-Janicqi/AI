import mcts_alphazero as mcts
import torch
import torch.nn.functional as F
import numpy as np
import random
from tqdm import trange

class AlphaZero:
    def __init__(self, game, optimizer, model, args, execution_times):
        self.game = game
        self.optimizer = optimizer
        self.model = model
        self.args = args
        self.action_space = game.action_space
        self.mcts = mcts.MCTS_alphaZero(game, args, model, execution_times)

    def train(self, training_data):
        random.shuffle(training_data)
        for batch_index in range(0, len(training_data), self.args['batch_size']):
            batch = training_data[batch_index:min(len(training_data) - 1, batch_index + self.args['batch_size'])]
            state, policy_target, value_target = zip(*batch)
            state, policy_target, value_target = np.array(state), np.array(policy_target), np.array(value_target).reshape(-1, 1)
            state = torch.tensor(state, dtype=torch.float32)
            policy_target = torch.tensor(policy_target, dtype=torch.float32)
            value_target = torch.tensor(value_target, dtype=torch.float32)

            out_policy, out_value = self.model(state)
            policy_loss = F.cross_entropy(out_policy, policy_target)
            value_loss = F.mse_loss(out_value, value_target)
            loss = policy_loss + value_loss

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def self_play(self):
        memory = []
        self.game.setup()
        state = self.game.state.copy()
        player = 'White'

        while state.win_state == 'None':
            action_probs = self.mcts.search(state)
            memory.append([state, action_probs, state.player_turn])
            temp_action_probs = action_probs ** (1 / self.args['temperature'])
            action = np.random.choice(len(action_probs), p=temp_action_probs)
            state = self.game.get_next_state(state, action)
        
        return_memory = []
        for mem_state, mem_action_probs, mem_player in memory:
            value = 1 if mem_player == player else -1
            encoded_state = mem_state.encode()
            return_memory.append([encoded_state, mem_action_probs, value])

        return return_memory

    def learn(self):
        for iteration in trange(self.args['num_iterations'], ncols=100, desc='Learning iteration'):
            memory = []

            self.model.eval()
            for self_play_iteration in trange(self.args['num_self_play_iterations'], ncols=100, desc='Self play iteration'):
                memory.extend(self.self_play())
            
            self.model.train()
            for epoch in trange(self.args['num_epochs'], ncols=100, desc='Epoch'):
                self.train(memory)

            torch.save(self.model.state_dict(), f'models/model_{iteration}.pt')
            torch.save(self.optimizer.state_dict(), f'models/optimizer_{iteration}.pt')