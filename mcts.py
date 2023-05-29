import numpy as np
import copy
import math
import time


class Node:
    def __init__(self, state, args, current_depth, parent=None, action_taken=None) -> None:
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.children = []
        self.depth = current_depth
        self.visit_count = 0
        self.value = 0

    def get_score(self, parent):
        q = 1 - ((self.value / self.visit_count) + 1) / 2
        return q + self.args['C'] * math.sqrt(math.log(self.visit_count) / parent.visit_count)

    def is_fully_expanded(self):
        return len(self.state.moves) == 0 and len(self.children) > 0

    def select(self):
        best_child: Node = None  # type: ignore
        best_score = -np.inf
        score_table = np.zeros(len(self.children))
        for i, child in enumerate(self.children):
            score_table[i] = child.get_score(self)
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

    def expand(self):
        if self.state.is_terminal(self.state) is False:
            action = np.random.choice(self.state.moves)
            self.state.moves.remove(action)
            child = Node(copy.deepcopy(self.state), self.args,
                         self.depth + 1, self, action)
            if not child.parent:
                raise Exception("Parent is None")
            self.children.append(child)
            return child
        else:
            raise Exception("Cannot expand terminal node")

    def simulate(self):
        self.state.push(self.action_taken)

    def backpropagate(self, value):
        self.visit_count += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(-value)  # (value)


class MCTS:
    def __init__(self, game, args) -> None:
        self.game = game
        self.args = args
        self.root = None

    def search(self, state):
        self.root = Node(state, self.args, 0)
        self.root.state.moves = self.root.state.get_legal_moves(self.root.state)

        for _ in range(self.args['num_searches']):
            node = self.root
            while node.is_fully_expanded():
                tic = time.perf_counter()
                node = node.select()
                toc = time.perf_counter()
                # print(f"Select took {toc - tic:0.4f} seconds")
            
            if not node.state.is_terminal(node.state):

                tic = time.perf_counter()
                node = node.expand()
                toc = time.perf_counter()
                # print(f"Expand took {toc - tic:0.4f} seconds")

                tic = time.perf_counter()
                node.simulate()
                toc = time.perf_counter()
                # print(f"Simulate took {toc - tic:0.4f} seconds")
            
            value = node.state.get_value(node.state)

            tic = time.perf_counter()
            node.backpropagate(value)
            toc = time.perf_counter()
            # print(f"Backpropagate took {toc - tic:0.4f} seconds")

        action_probability = np.zeros(len(self.root.children))
        for i, child in enumerate(self.root.children):
            action_probability[i] = child.visit_count
        action_probability = action_probability / np.sum(action_probability)
        actions = []
        for child in self.root.children:
            actions.append(child.action_taken)
        return action_probability, actions
