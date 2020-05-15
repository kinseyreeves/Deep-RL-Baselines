import argparse
import os

import rllib_trainers
from gym_scalable.envs.grid.maps import map_loader
from gym_scalable.envs.grid.maze_env import MazeEnv
from pympler.tracker import SummaryTracker
from ray import tune

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
parser.add_argument('--1reward', dest='reward', action='store_true')
parser.add_argument('--name', type=str, default='test_run')
parser.add_argument('--num_goals', type=int, default=3)
parser.add_argument('--random_goals', dest='random_goals', action='store_true', default=False)
parser.add_argument('--random_start', dest='random_start', action='store_true', default=False)

parser.add_argument('--curriculum', dest='curriculum', action='store_true', default=False)
parser.add_argument('--curriculum_eps', type=int, default=100)

parser.add_argument('--encoding', type=str, default="pos")
parser.add_argument('--map_size', type=int)

args = parser.parse_args()
encoding = None

logdir = "~/ray_results/maze"

a = os.getcwd() + "/maps/map_3x3.txt"

def tune_runner(trainer, mapfile, name, mapsize):
    global args

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
             #stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{goals}goals-{name}-{args.encoding}")


# ################################################### #
# # -----------------##Training##-------------------- #
# # ################################################# #

mapfile = map_loader.get_size_map(args.map_size)

name = args.rl
trainer = rllib_trainers.get_trainer(name)

tune_runner(trainer, mapfile, name, args.map_size)
