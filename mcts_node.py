import math

import numpy as np

from state import State


class Node:
    def __init__(self, state: State, parent=None, action_taken=None, prior=0) -> None:
        self.state: State = state
        self.parent: Node = parent
        self.action_taken: int = action_taken
        self.children: list[Node] = []
        self.visit_count: np.uint16 = np.uint16(0)
        self.value: np.float16 = np.float16(0)
        self.prior: np.float16 = np.float16(prior)

    def get_value(self, child: 'Node') -> np.float16:
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value / child.visit_count) + 1) / 2
        return q_value + 2 * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def backpropagate(self, value) -> None:
        self.visit_count += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(-value)

    def is_expanded(self) -> bool:
        return len(self.children) > 0

    def select(self) -> 'Node':
        return max(self.children, key=self.get_value)

    def expand(self, actions, probs, move_ids) -> None:
        for i in range(len(actions)):
            next_state = self.state.next_state(actions[i])
            self.children.append(
                Node(next_state, self, move_ids[i], probs[i]))

    def __hash__(self) -> int:
        return hash(self.state.board, self.state.player_turn)
