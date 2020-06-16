import argparse
import os

import rllib_trainers
from gym_scalable.envs.grid.maps import map_loader
from gym_scalable.envs.grid.maze_env import MazeEnv
from pympler.tracker import SummaryTracker
from runners import *
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


# ################################################### #
# # -----------------##Training##-------------------- #
# # ################################################# #


mapfile = map_loader.get_size_map(args.map_size)
print("here")

name = args.rl
trainer = rllib_trainers.get_trainer(name)

if (args.tune_search):
    if args.rl == "PPO":
        print("running PPO exp")
        PPO_tune_runner(trainer, mapfile, name, args.map_size, args)
    elif args.rl == "DQN":
        print("running DQN exp")
        _DQN_tune_runner(trainer, mapfile, name, args.map_size, args)
    elif args.rl=="A2C":
        A2C_tune_runner(trainer,mapfile,name,args.map_size,args)
    else:
        tune_runner(trainer, mapfile, name, args.map_size, args)
else:
    if (args.curriculum):
        print("curriculum running")
        curriculum_tune_runner(trainer, mapfile, name, args.map_size, args)
    else:
        if args.rl == "PPO":
            print("running PPO exp")
            PPO_maze_runner(trainer, mapfile, name, args.map_size, args)
        elif args.rl == "DQN":
            print("running DQN exp")
            DQN_maze_runner(trainer, mapfile, name, args.map_size, args)
        else:
            A2C_maze_runner(trainer, mapfile, name, args.map_size, args)
