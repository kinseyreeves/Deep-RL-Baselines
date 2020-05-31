import argparse
import os

import rllib_trainers
from gym_scalable.envs.grid.maps import map_loader
from gym_scalable.envs.grid.maze_env import MazeEnv
from pympler.tracker import SummaryTracker
from ray import tune
from ray.tune import grid_search

tracker = SummaryTracker()

# Things to tune
"""
learning rate
gamma
clip param in ppo
lambda
train batch size
sgd minibatch size
num sgd iter
"""

parser = argparse.ArgumentParser(description='Maze experiment runner')
parser.add_argument('--steps', type=int, default=200)
parser.add_argument('--rl', type=str, default="PPO")
parser.add_argument('--1reward', dest='reward', action='store_true', default = False)
parser.add_argument('--name', type=str, default='test_run')
parser.add_argument('--num_goals', type=int, default=3)
parser.add_argument('--random_goals', dest='random_goals', action='store_true', default=False)
parser.add_argument('--random_start', dest='random_start', action='store_true', default=False)

parser.add_argument('--tune_search', dest='tune_search', action='store_true', default=False)

parser.add_argument('--curriculum', dest='curriculum', action='store_true', default=False)
parser.add_argument('--curriculum_eps', type=int, default=100)

parser.add_argument('--encoding', type=str, default="st")
parser.add_argument('--map_size', type=int, default=5)

args = parser.parse_args()
encoding = None

logdir = "~/ray_results/maze"


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
                     'lr': grid_search([0.0001, 0.001, 0.01]),
                    'dueling': grid_search([True, False]),
                    'prioritized_replay': grid_search([True, False]),

                    'noisy': grid_search([True, False]),
                    'buffer_size': grid_search([1000, 5000, 20000]),

                     'model': {
                         'fcnet_hiddens': grid_search([[128, 128], [256, 256], [512, 512]])
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")

def DQN_runner(trainer, mapfile, name, mapsize, args):
    if (args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,

                     'lr': grid_search([0.0001, 0.001, 0.01]),
                     'dueling': False,
                     'prioritized_replay': True,

                     'noisy': grid_search([True, False]),
                     'buffer_size': grid_search([1000, 5000, 20000]),
                     'model': {
                         'fcnet_hiddens': grid_search([[128, 128], [256, 256]])
                     },
                     "env_config": get_env_config(mapfile, args, goals)},
             checkpoint_freq=10, checkpoint_at_end=True,
             # stop={"timesteps_total": args.steps},
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


def PPO_runner(trainer, mapfile, name, mapsize, args):
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
                      "curriculum_eps": grid_search([50, 100, 200, 500])}
                 },
         checkpoint_freq=10, checkpoint_at_end=True,
         # stop={"timesteps_total": args.steps},
         name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


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

# ################################################### #
# # -----------------##Training##-------------------- #
# # ################################################# #


mapfile = map_loader.get_size_map(args.map_size)

name = args.rl
trainer = rllib_trainers.get_trainer(name)

if (args.tune_search):
    if args.rl == "PPO":
        print("running PPO exp")
        PPO_tune_runner(trainer, mapfile, name, args.map_size, args)
    elif args.rl == "DQN":
        print("running DQN exp")
        _DQN_tune_runner(trainer, mapfile, name, args.map_size, args)
    else:
        tune_runner(trainer, mapfile, name, args.map_size, args)
else:
    if (args.curriculum):
        curriculum_tune_runner(trainer, map, name, args.map_size, args)
    else:
        if args.rl == "PPO":
            print("running PPO exp")
            PPO_runner(trainer, mapfile, name, args.map_size, args)
        elif args.rl == "DQN":
            print("running DQN exp")
            tune_runner(trainer, mapfile, name, args.map_size, args)
        else:
            tune_runner(trainer, mapfile, name, args.map_size, args)
