if __name__ == '__main__':
    from actionspace import ActionSpace
    from alphazero import AlphaZero
    from game import Game
    from gui import Gui

    env = {
        'train': True,
        'retrain': False,  # use if network architecture is changed
    }
    res_net = {
        'num_blocks': 24,
        'num_layers': 12
    }
    mcts_args = {
        'num_searches': 1000,
        'temperature': 100,
        'exec_times': False,
    }
    alphazero_training_args = {
        'num_training_iterations': 64,
        'game_bucket_size': 12,
        'num_epochs': 4000,
        'early_stopping': 100,
        'train_test_ratio': 0.6,  # train = 1 - ratio, test = ratio
        'gd_threshold': 0.5,
        'batch_size': 64,
        'temperature': 1000,
        'weight_decay': 0.001,
        'learning_rate': 0.001,
        'max_game_length': 200,
        'num_processes': 4,
    }
    alphaplay_args = {
        'num_searches': 200,
        'temperature': 1,
        'exec_times': True,
    }
    cache_args = {
        'max_mcts_cache_size_gb': 8,  # mcts cashe is unique to each process
        'max_state_cache_size_gb': 4,  # state cache is shared between processes
    }
    game_args = {
        'board_size': 6,
    }
    args = {
        'env': env,
        'res_net': res_net,
        'mcts': mcts_args,
        'training': alphazero_training_args,
        'alphaplay': alphaplay_args,
        'cache': cache_args,
        'game': game_args,
    }
    actionspace = ActionSpace(args['game']['board_size'])
    alphazero = AlphaZero(actionspace, args)
    if env['train']:
        if not env['retrain']:
            alphazero.load_newest_model()
        alphazero.learn()
    game = Game()
    Gui(alphazero, args['game']['board_size'],
        game, actionspace, debug_mode=False)
