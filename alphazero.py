import mcts_alphazero as mcts
import torch
import numpy as np
import copy
from tqdm import trange

class AlphaZero:
    def __init__(self, game, optimizer, model, args):
        self.game = game
        self.optimizer = optimizer
        self.model = model
        self.args = args
        self.action_space = game.action_space
        self.mcts = mcts.MCTS_alphaZero(game, args, model)

    def train(self, num_iterations):
        x = 0
        return x

    def self_play(self):
        memory = []
        self.game.setup()
        state = copy.deepcopy(self.game)
        player = 'White'

        while state.win_state is 'None':
            action_probs = self.mcts.search(state)
            memory.append([state, action_probs, state.player_turn])
            action = np.random.choice(len(action_probs), p=action_probs)
            state = state.get_next_state(state, action)
        
        return_memory = []
        for mem_state, mem_action_probs, mem_player in memory:
            value = 1 if mem_player == player else -1
            encoded_state = self.game.encode_state(mem_state)
            return_memory.append([encoded_state, mem_action_probs, value])

        return return_memory

    def learn(self):
        for iteration in range(self.args['num_iterations']):
            memory = []

            for self_play_iteration in range(self.args['num_self_play_iterations']):
                memory.extend(self.self_play())

            self.model.train()
            for epoch in trange(self.args['num_epochs']):
                self.train(memory)

            torch.save(self.model.state_dict(), f'model_{iteration}.pt')
            torch.save(self.optimizer.state_dict(), f'optimizer_{iteration}.pt')