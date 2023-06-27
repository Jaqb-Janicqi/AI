import copy
import multiprocessing as mp
import os
import random
from multiprocessing import Manager, Process
from time import sleep

import numpy as np
import torch
import torch.nn.functional as F
from matplotlib import pyplot as plt
from tqdm.auto import tqdm, trange

from actionspace import ActionSpace
from game import Game
from mcts import MCTS
from res_net import ResNet


class AlphaZero:
    def __init__(self, action_space, args):
        self.args: dict = args
        self.action_space: ActionSpace = action_space
        self.game = Game()
        self.model = ResNet(
            self.args['game']['board_size'] * self.args['game']['board_size'],
            self.action_space.size,
            self.args['res_net']['num_blocks'],
            self.args['res_net']['num_layers']
        )
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=args['training']['learning_rate'],
                                          weight_decay=args['training']['weight_decay'], amsgrad=True)
        self.mcts = None
        self.model_num = None

    def load_newest_model(self):
        if os.listdir("models"):
            model_files = [file for file in os.listdir(
                "models") if file.startswith("model_")]
            highest_model_num = max(
                [int(file.split("_")[1].split(".")[0]) for file in model_files])
            self.model_num = highest_model_num

            # Load the model with the highest model number
            self.model.load_state_dict(torch.load(
                f"models/model_{self.model_num}.pt"))
            self.optimizer.load_state_dict(torch.load(
                f"models/optimizer_{self.model_num}.pt"))

    def set_alphaplay(self):
        self.args['mcts']['num_searches'] = self.args['alphaplay']['num_searches']
        self.args['mcts']['temperature'] = self.args['alphaplay']['temperature']
        self.args['mcts']['exec_times'] = self.args['alphaplay']['exec_times']
        max_cache_size = self.args['cache']['max_mcts_cache_size_gb']
        self.load_newest_model()
        self.mcts = MCTS(self.args, self.action_space, self.model, self.game)

    def predict(self, state):
        if self.mcts is None:
            self.set_alphaplay()
        action_probs, val = self.mcts.search(state)
        action = np.argmax(action_probs)
        return self.action_space.get_by_id(action)

    def make_batches(self, data, batch_size):
        batches = []
        for batch_index in range(0, len(data), batch_size):
            if batch_index == len(data) - 1:  # list[x:x] = []
                break
            batch = data[batch_index:min(
                len(data) - 1, batch_index + self.args['training']['batch_size'])]
            state, policy_targets, value_targets = zip(*batch)
            state, policy_targets, value_targets = \
                np.array(state), np.array(policy_targets), np.array(
                    value_targets).reshape(-1, 1)

            state = torch.tensor(state, dtype=torch.float32).unsqueeze(1)
            policy_targets = torch.tensor(policy_targets, dtype=torch.float32)
            value_targets = torch.tensor(value_targets, dtype=torch.float32)

            batch = (state, policy_targets, value_targets)
            batches.append(batch)
        return batches

    def calculate_loss(self, batch):
        state, policy_targets, value_targets = batch
        out_policy, out_value = self.model(state)

        policy_loss = F.cross_entropy(out_policy, policy_targets)
        value_loss = F.mse_loss(out_value, value_targets)
        loss = policy_loss + value_loss
        return loss

    def train(self, data):
        num_epochs = self.args['training']['num_epochs']
        stop_target = self.args['training']['early_stopping']
        random.shuffle(data)
        len_data = len(data)
        train_data = data[:int(
            len_data * self.args['training']['train_test_ratio'])]
        test_data = data[int(
            len_data * self.args['training']['train_test_ratio']):]
        train_batches = self.make_batches(
            train_data, self.args['training']['batch_size'])
        test_batches = self.make_batches(
            test_data, self.args['training']['batch_size'])
        best_loss = np.inf
        epochs_without_improvement = 0
        loss_history = []

        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Best Validation Loss')
        plt.title('Training')

        gradient_pbar = tqdm(total=100, ncols=100,
                             desc='Gradient', leave=False, position=2)

        for epoch in trange(num_epochs, ncols=100, desc='Epochs', leave=False, position=1):
            if epochs_without_improvement >= stop_target:
                break

            self.model.train()
            for batch in train_batches:
                loss = self.calculate_loss(batch)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            self.model.eval()
            with torch.no_grad():
                loss = 0
                for batch in test_batches:
                    loss += self.calculate_loss(batch)
                loss /= len(test_batches)
                loss_history.append(loss)
                if loss < best_loss:
                    best_loss = loss
                    epochs_without_improvement = 0
                else:
                    epochs_without_improvement += 1

            gradient_norm = torch.nn.utils.clip_grad_norm_(
                self.model.parameters(), float('inf'))
            gradient_pbar.set_description(
                f'Gradient: {gradient_norm.item():.2f}')
            if gradient_norm < self.args['training']['gd_threshold']:
                gradient_pbar.write(
                    f'Gradient stop met: {gradient_norm.item():.2f}')
                plt.close()
                return

            plt.plot(loss_history, 'b-')
            plt.draw()
            plt.pause(0.00001)

        plt.close()

    def self_play(self, state, mcts, queue, process_id):
        memory = []
        for _ in trange(self.args['training']['max_game_length'], ncols=100,
                        desc=f'Game {process_id}', leave=False, position=process_id+3):
            action_probs, node_value = mcts.search(state)
            memory.append([state, action_probs, node_value])
            action_id = np.random.choice(len(action_probs), p=action_probs)
            action = self.action_space.get_by_id(action_id)
            state = state.next_state(action)
            if state.is_terminal():
                break

        return_memory = []
        for mem_state, mem_action_probs, node_value in memory:
            encoded_state = mem_state.encode()
            return_memory.append(
                [encoded_state, mem_action_probs, node_value])
        queue.put(return_memory)

    def learn(self):
        games_finished = 0
        games_started = 0
        num_processes = min(self.args['training']
                            ['num_processes'], mp.cpu_count())
        bucket_size = self.args['training']['game_bucket_size']
        num_training_games = self.args['training']['num_training_iterations'] * \
            self.args['training']['game_bucket_size']
        default_state = self.game.load_default(self.args['game']['board_size'])

        processes = [False for i in range(num_processes)]
        manager = Manager()
        game_bucket = manager.Queue()
        tqdm._instances.clear()
        games_played_pbar = tqdm(
            total=num_training_games, ncols=100, desc='Games played', position=0, leave=False)
        bucket_size_pbar = tqdm(
            total=bucket_size, ncols=100, desc='Game buffer', position=1, leave=False)

        while games_finished < num_training_games:
            for i in range(num_processes):
                if not processes[i] and games_started < num_training_games:
                    model = copy.deepcopy(self.model).eval()
                    game = copy.deepcopy(self.game)
                    args = copy.deepcopy(self.args)
                    action_space = copy.deepcopy(self.action_space)
                    mcts = MCTS(args, action_space, model, game)
                    state = copy.deepcopy(default_state)
                    p = Process(target=self.self_play, args=(
                        state, mcts, game_bucket, i))
                    processes[i] = p
                    p.start()
                    games_started += 1

            for p in processes:
                if p and not p.is_alive():
                    games_finished += 1
                    games_played_pbar.update(1)
                    bucket_size_pbar.update(1)
                    processes[processes.index(p)] = False

            if game_bucket.qsize() >= bucket_size:
                bucket_size_pbar.reset()
                memory = []
                while not game_bucket.empty():
                    game_data = game_bucket.get()
                    memory.extend(game_data)
                self.train(memory)

                if self.model_num is not None:
                    self.model_num += 1
                else:
                    self.model_num = 0
                torch.save(self.model.state_dict(),
                           f'models/model_{self.model_num}.pt')
                torch.save(self.optimizer.state_dict(),
                           f'models/optimizer_{self.model_num}.pt')
            sleep(1)
