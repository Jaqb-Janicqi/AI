import numpy as np
from tqdm.auto import trange

import res_net as ResNet
from actionspace import ActionSpace
from game import Game
from mcts_node import Node
from move import Move
from state import State


class MCTS:
    def __init__(self, args: dict, action_space: ActionSpace,
                 res_net: ResNet, game: Game) -> None:
        self.args: dict = args
        self.root: Node = None
        self.action_space: ActionSpace = action_space
        self.res_net: ResNet = res_net
        self.game: Game = game

    def search(self, state: State) -> None:
        self.root = Node(state)
        self.root.state.legal_moves = self.game.generate_moves(
            self.root.state.board, self.root.state.player_turn)

        for _ in trange(self.args['mcts']['num_searches'], desc="MCTS", ncols=100,
                        leave=False, disable=not self.args['mcts']['exec_times']):
            node = self.root
            while node.is_expanded():
                node = node.select()
            value = node.state.win * node.state.player_turn

            if not node.state.is_terminal():
                policy, value = self.res_net(
                    ResNet.get_tensor_state(node.state.encode()))
                policy = ResNet.get_policy(policy)

                if len(node.state.legal_moves) == 0:
                    node.state.legal_moves = self.game.generate_moves(
                        node.state.board, node.state.player_turn)
                    if len(node.state.legal_moves) == 0:
                        print(node.state.board)
                        exit()

                move_probs = np.zeros(
                    len(node.state.legal_moves), dtype=np.float32)
                move_ids = np.zeros(
                    len(node.state.legal_moves), dtype=np.uint16)
                moves = np.zeros(len(node.state.legal_moves), dtype=Move)
                for i, key in enumerate(node.state.legal_moves):
                    move_id = self.action_space.get_id_of_hash(key)
                    move_ids[i] = move_id
                    move_probs[i] = policy[move_id]
                    moves[i] = self.action_space.get(key)

                move_probs = np.power(
                    move_probs, 1 / self.args['mcts']['temperature'])
                move_probs = move_probs / np.sum(move_probs)
                value = ResNet.get_value(value)

                node.expand(moves, move_probs, move_ids)

            node.backpropagate(value)

        action_probability = np.zeros(self.action_space.size, dtype=np.float16)
        for child in self.root.children:
            action_probability[child.action_taken] = child.visit_count
        action_probability = action_probability / np.sum(action_probability)
        return action_probability, self.root.value
