import numpy as np
import copy
import math
import res_net as net
import torch


class Node:
    def __init__(self, state, args, parent=None, action_taken=None, prior=0) -> None:
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.children = []
        self.visit_count = 0
        self.value = 0
        self.prior = prior

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
        avg = np.sum(score_table) / len(score_table)
        if best_score == avg:
            best_child = self.select_random()
        best_child.state.generate_moves(best_child.state)
        return best_child

    def select_random(self):
        return np.random.choice(self.children)

    def expand(self, policy):
        for action, prob in enumerate(policy):
            if prob > 0:
                self.children.append(
                    Node(self.state.get_next_state(self.state, action), self.args, self, action, prob)
                )

    def backpropagate(self, value):
        self.visit_count += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(-value)

@torch.no_grad()
class MCTS_alphaZero:
    def __init__(self, game, args, model: net.ResNet, action_space) -> None:
        self.game = game
        self.args = args
        self.root = None
        self.model = model
        self.action_space = action_space
        self.action_space_size = len(action_space)

    def search(self, state):
        self.root = Node(state, self.args)
        self.root.state.generate_moves(self.root.state)

        for _ in range(self.args['num_searches']):
            node = self.root
            while node.is_fully_expanded():
                node = node.select()

            value = node.state.get_value(node.state)

            if not node.state.is_terminal(node.state):
                # policy, value = net.get_tensor_state(node.state.encode_state(node.state))
                policy, value = self.model(net.get_tensor_state(node.state.encode_state(node.state)))
                policy = net.get_policy(policy)
                legal_policy = np.zeros(self.action_space_size)
                for move in node.state.moves:
                    encoded_move_id = node.state.encode_to_action_space(move)
                    legal_policy[encoded_move_id] = policy[encoded_move_id]
                legal_policy = legal_policy / np.sum(legal_policy)
                value = net.get_value(value)
                # valid_moves = node.state.moves
                node.expand(legal_policy)

            node.backpropagate(value)   # type: ignore

        action_probability = np.zeros(len(self.root.children))
        for i, child in enumerate(self.root.children):
            action_probability[i] = child.visit_count
        action_probability = action_probability / np.sum(action_probability)
        actions = []
        for child in self.root.children:
            actions.append(child.action_taken)
        return action_probability, actions
