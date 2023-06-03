import numpy as np
import copy
import math
import res_net as net
import torch
import time
from tqdm import trange
from board import Game, State


class Node:
    def __init__(self, state, args, parent=None, action_taken=None, prior=0) -> None:
        self.args = args
        self.state: State = state
        self.parent: Node = parent  # type: ignore
        self.action_taken: int = action_taken   # type: ignore
        self.children = []
        self.visit_count = 0
        self.value = 0
        self.prior: float = prior

    def get_score(self, child):
        if child.visit_count == 0:
            return 0
        else:
            q = 1 - ((child.value / child.visit_count) + 1) / 2
            return q + self.args['C'] * math.sqrt(self.visit_count / (child.visit_count + 1)) * child.prior

    def is_fully_expanded(self):
        return len(self.children) > 0

    def select(self):
        best_child: Node = None  # type: ignore
        best_score = -np.inf
        score_table = np.zeros(len(self.children))
        for i, child in enumerate(self.children):
            score_table[i] = self.get_score(child)
            if score_table[i] > best_score:
                best_child = child
                best_score = score_table[i]
        if np.all(score_table == score_table[0]):
            return self.select_random()
        return best_child

    def select_random(self):
        return np.random.choice(self.children)

    def expand(self, actions, probs, game):
        for i in range(len(actions)):
            next_state = game.get_next_state(self.state, actions[i])

            if next_state is False: # catch illegal moves
                game.save_to_fenn('fenn.txt', self.state.board)
                action = game.action_space.decode(actions[i])
                print(f'Illegal move: {action}')
                exit()
            
            self.children.append(
                Node(next_state, self.args, self, actions[i], probs[i])
            )

    def backpropagate(self, value):
        self.visit_count += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(-value)

@torch.no_grad()
class MCTS_alphaZero:
    def __init__(self, game, args, model: net.ResNet, execution_times) -> None:
        self.game: Game = game
        self.args = args
        self.root: Node = None # type: ignore
        self.model = model
        self.execution_times = execution_times

    def clear_tree(self, node = None):
        if node is None:
            node = self.root
        for child in node.children:
            child.value = 0
            child.visit_count = 0
            self.clear_tree(child)

    def search(self, state, oponent_action=None):
        # try to reuse the tree when possible
        # if tree does not exist, initialize with current game state
        if oponent_action is None or self.root is None:
            self.root = Node(state, self.args)
        else:
            # find branch corresponding to opponent's action and make it root of the tree
            found = False
            for child in self.root.children:
                if child.action_taken == oponent_action:
                    self.root = child
                    self.root.parent = None
                    found = True
                    break
            if not found:
                self.root = Node(state, self.args)
            else:
                self.clear_tree()

        # for _ in trange(self.args['num_searches'], ncols=100, desc='Tree search'):
        for _ in range(self.args['num_searches']):
            node = self.root
            while node.is_fully_expanded():
                node = node.select()

            value = node.state.value()

            if value == 0:
                policy, value = self.model(net.get_tensor_state(node.state.encode()))
                policy = net.get_policy(policy)

                moves = node.state.get_legal_moves()
                move_probs = np.zeros(len(moves), dtype=np.float32)
                move_ids = np.zeros(len(moves), dtype=np.uint32)

                for position, move in enumerate(moves):
                    encoded_move_id = self.game.action_space.encode(move)
                    move_probs[position] = policy[encoded_move_id]
                    move_ids[position] = encoded_move_id

                move_probs = move_probs / np.sum(move_probs)
                value = net.get_value(value)
                node.expand(move_ids, move_probs, self.game)

            node.backpropagate(value)

        action_probability = np.zeros(self.game.action_space.action_space_size, dtype=np.float32)
        for child in self.root.children:
            action_probability[child.action_taken] = child.visit_count
        action_probability = action_probability / np.sum(action_probability)
        return action_probability
