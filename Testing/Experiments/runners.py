import rllib_trainers
from gym_scalable.envs.grid.maps import map_loader
from gym_scalable.envs.grid.maze_env import MazeEnv
from pympler.tracker import SummaryTracker
from ray import tune
from ray.tune import grid_search

def get_env_config(mapfile, args, goals):
    config = {"mapfile": mapfile,
              "state_encoding": args.encoding,
              "randomize_start": args.random_start,
              "num_goals": goals,
              "randomize_goal": args.random_goals,
              "capture_reward": args.reward,
              "curriculum": args.curriculum,
              "curriculum_eps": args.curriculum_eps}
    return config

def tune_runner_changing_nn(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,
                     # "num_workers":4,
                     # "num_envs_per_worker": 1,
                     # 'lr' : grid_search([0.0001, 0.001, 0.01]),
                     # 'lr': grid_search([0.0001]),

                     'model': {
                         # 'fcnet_hiddens': grid_search([[128, 128], [256,256]])
                         'fcnet_hiddens': [256, 256],
                     },
                     "env_config": {"mapfile": mapfile,
                                    "state_encoding": args.encoding,
                                    "randomize_start": args.random_start,
                                    "num_goals": goals,
                                    "randomize_goal": args.random_goals,
                                    "capture_reward": args.reward,
                                    "curriculum": args.curriculum,
                                    "curriculum_eps": args.curriculum_eps}},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


# def DQN_tune_runner(trainer, mapfile, name, mapsize, args):
#     print()
#     if (args.num_goals):
#         goals = args.num_goals
#     else:
#         goals = mapsize
#         tune.run(trainer,
#             config={"env": MazeEnv,

#                     'lr': grid_search([0.0001, 0.001, 0.01]),
#                     'dueling': grid_search([True, False]),
#                     'prioritized_replay': grid_search([True, False]),

#                     'noisy': grid_search([True, False]),
#                     'buffer_size': grid_search([1000, 5000, 20000]),
#                     'model': {
#                         'fcnet_hiddens': grid_search([[128, 128], [256, 256]])
#                     },
#                     "env_config": get_env_config(mapfile, args, goals)},
#             checkpoint_freq=10, checkpoint_at_end=True,
#             stop={"timesteps_total": args.steps},
#             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")

def _DQN_tune_runner(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,
                    'dueling': grid_search([True, False]),
                    'prioritized_replay': grid_search([True, False]),
                    'buffer_size': grid_search([5000, 50000]),

                     'model': {
                         'fcnet_hiddens': grid_search([[256], [256, 256]])
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


def PPO_tune_runner(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,
                     # "num_workers":4,
                     # "num_envs_per_worker": 1,
                     "use_critic": grid_search([True, False]),
                     "clip_param": grid_search([0.1, 0.3, 0.5]),
                     "kl_target": grid_search([0.005, 0.01]),

                     # 'lr' : grid_search([0.0001, 0.001, 0.01]),
                     # 'lr': grid_search([0.0001]),
                     'model': {
                         'fcnet_hiddens': grid_search([[128, 128], [256, 256], [512, 512]])
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")

def A2C_tune_runner(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,
                     # "num_workers":4,
                     # "num_envs_per_worker": 1,
                     "use_critic": grid_search([True, False]),
                     "use_gae": grid_search([True, False]),
                     "grad_clip": grid_search([0.005, 0.01]),

                     # 'lr' : grid_search([0.0001, 0.001, 0.01]),
                     # 'lr': grid_search([0.0001]),
                     'model': {
                         'fcnet_hiddens': grid_search([[256], [256, 256]])
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


def DQN_runner(trainer, mapfile, name, mapsize, args):
    """
    DQN runner with good parameters
    :param trainer:
    :param mapfile:
    :param name:
    :param mapsize:
    :param args:
    :return:
    """
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,

                     'dueling': True,
                     'prioritized_replay': True,
                     'buffer_size': 50000,
                     'model': {
                         'fcnet_hiddens': grid_search([256])
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


def PPO_runner(trainer, mapfile, name, mapsize, args):
    """
    PPO runner with good parameters
    :param trainer:
    :param mapfile:
    :param name:
    :param mapsize:
    :param args:
    :return:
    """
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,

                     "use_critic": True,
                     "clip_param": 0.5,
                     "kl_target": 0.01,

                     'model': {
                         'fcnet_hiddens': [256, 256]
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


def A2C_runner(trainer, mapfile, name, mapsize, args):
    """
    A2C runner with good parameters
    :param trainer:
    :param mapfile:
    :param name:
    :param mapsize:
    :param args:
    :return:
    """
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,

                     "use_critic": False,
                     "use_gae" : False,
                     "grad_clip":0.005,
                     'model': {
                         'fcnet_hiddens': [256, 256]
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")



def tune_runner(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,

                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


def curriculum_tune_runner(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
         config={"env": MazeEnv,
                 "num_workers":0,
                 "env_config": {"mapfile": mapfile,
                      "state_encoding": args.encoding,
                      "randomize_start": args.random_start,
                      "num_goals": goals,
                      "randomize_goal": args.random_goals,
                      "capture_reward": args.reward,
                      "curriculum": args.curriculum,
                      "curriculum_eps": args.curriculum_eps}
                 },
         checkpoint_freq=10, checkpoint_at_end=True,
         # stop={"timesteps_total": args.steps},
         name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}-{args.curriculum_eps}")