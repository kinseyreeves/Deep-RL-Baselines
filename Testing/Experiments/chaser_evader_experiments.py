"""

Single evader (RL controlled) with single chaser (A* controlled) experiments
Kinsey Reeves
"""

import os

print(os.getcwd())
from ray import tune
from gym_scalable.envs.grid.chaser_evader_env import ChaserEvaderEnv
from gym_scalable.envs.grid.maps import map_loader
import rllib_trainers
from ray.tune import grid_search
from runners import *
import argparse

parser = argparse.ArgumentParser(description='ChaserEvaser experiment runner')
parser.add_argument('--steps', type=int, default=200)
parser.add_argument('--1reward', dest='reward', action='store_true')
parser.add_argument('--name', type=str, default='ChaserEvaser')
parser.add_argument('--num_goals', type=int, default=3)

parser.add_argument('--rl', type=str, default="PPO")
parser.add_argument('--rl_evader', dest='rl_evader', action='store_true', default=False)
parser.add_argument('--random_goals', dest='random_goals', action='store_true', default=False)
parser.add_argument('--random_start', dest='random_start', action='store_true', default=False)
parser.add_argument('--curriculum', dest='curriculum', action='store_true', default=False)
parser.add_argument('--curriculum_eps', type=int, default=100)
parser.add_argument('--encoding', type=str, default="st")
parser.add_argument('--map_size', type=int, default=5)

args = parser.parse_args()


# ##################################################### #
# # -----------------##Training##---------------------- #
# # ################################################### #
name = args.rl
trainer = rllib_trainers.get_trainer(name)
mapfile = map_loader.get_size_map(args.map_size)


if args.rl == "PPO":
    print("running PPO exp")
    PPO_ch_ev_runner(trainer, mapfile, name, args.map_size, args)
elif args.rl == "DQN":
    print("running DQN exp")
    DQN_ch_ev_runner(trainer, mapfile, name, args.map_size, args)
else:
    A2C_ch_ev_runner(trainer, mapfile, name, args.map_size, args)

