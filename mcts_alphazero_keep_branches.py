import numpy as np
import copy
import math
import res_net as net
import torch
import time
from tqdm import tqdm, trange
from board import Game, State


class Node:
    def __init__(self, args, depth=0, parent=None, action_taken=None, prior=0, state=None) -> None:
        self.args = args
        self.state: State = state # type: ignore
        self.parent: Node = parent  # type: ignore
        self.action_taken: int = action_taken   # type: ignore
        self.children = []
        self.visit_count = 0
        self.value = 0
        self.prior: float = prior
        self.depth: int = depth

    def get_score(self, child):
        if child.visit_count == 0:
                q_value = 0
        else:
                q_value = 1 - ((child.value / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

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
            self.children.append(
                Node(self.args, self.depth + 1, self, actions[i], probs[i])
            )

    def backpropagate(self, value):
        self.visit_count += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(-value)


class MCTS_alpha_zero:
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
            child.depth = node.depth + 1
            self.clear_tree(child)

    def search(self, state, oponent_action=None):
        # try to reuse the tree when possible
        # if tree does not exist, initialize with current game state
        if oponent_action is None or self.root is None:
            self.root = Node(self.args, state=state)
        else:
            # find branch corresponding to opponent's action and make it root of the tree
            found = False
            for child in self.root.children:
                if child.action_taken == oponent_action:
                    self.root = child
                    self.root.parent = None
                    self.root.depth = 0
                    found = True
                    break
            if not found:
                self.root = Node(self.args, state=state)
            else:
                self.clear_tree()

        depth_indicator = tqdm(ncols=100, desc='Current depth', leave=False, bar_format='{desc}')
        for _ in trange(self.args['num_searches'], desc="MCTS", ncols=100, leave=False):
            node = self.root
            while node.is_fully_expanded():
                node = node.select()
            
            if node.parent is not None:
                node.state = self.game.get_next_state(node.parent.state, node.action_taken)

            value = node.state.value()
            depth_indicator.set_description(f"Current depth: {node.depth}")

            if value == 0:
                policy, value = self.model(net.get_tensor_state(node.state.encode()))
                policy = net.get_policy(policy)

                if np.max(policy) == 1:
                    raise Exception("Model is overfitted")

                moves = node.state.get_legal_moves()
                move_probs = np.zeros(len(moves), dtype=np.float32)
                move_ids = np.zeros(len(moves), dtype=np.uint32)

                for position, move in enumerate(moves):
                    encoded_move_id = self.game.action_space.encode(move)
                    move_probs[position] = policy[encoded_move_id]
                    move_ids[position] = encoded_move_id
                
                move_probs = np.power(move_probs, 1 / self.args['temperature'])
                move_probs = move_probs / np.sum(move_probs)
                value = net.get_value(value)

                if node.depth < self.args['depth_limit']:
                    node.expand(move_ids, move_probs, self.game)

            node.backpropagate(value)

        action_probability = np.zeros(self.game.action_space.action_space_size, dtype=np.float32)
        for child in self.root.children:
            action_probability[child.action_taken] = child.visit_count
        action_probability = action_probability / np.sum(action_probability)
        return action_probability
