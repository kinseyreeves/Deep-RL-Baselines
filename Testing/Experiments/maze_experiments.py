import numpy as np
import gym
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet_v2 import FullyConnectedNetwork
from gym.spaces import Discrete, Box
from gym_scalable.envs.grid.chaser_evader_env import GridEvaderEnv
from gym_scalable.envs.grid.maze_env import MazeEnv

import ray
from ray import tune
from ray.rllib.utils import try_import_tf
from ray.tune import grid_search
from ray.rllib.agents import ppo, ddpg, a3c, dqn
import gym
import os
import sys
print(os.getcwd())
from ray import tune
from ray.tune.registry import register_env
import argparse
from gym_scalable.envs.grid.maps import map_loader
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()


parser = argparse.ArgumentParser(description='Maze experiment runner')
parser.add_argument('--steps', type=int, default = 200)
parser.add_argument('--rl', type=str, default = "PPO")
parser.add_argument('--1reward', dest='reward', action='store_true')
parser.add_argument('--name', type = str, default = 'test_run')
parser.add_argument('--num_goals', type = int, default = 3)
parser.add_argument('--random_goals', dest='random_goals', action='store_true', default = False)
parser.add_argument('--random_start', dest='random_start', action='store_true', default = False)
args = parser.parse_args()


logdir = "~/ray_results/maze"

a = os.getcwd() + "/maps/map_3x3.txt"

map_sizes = [3,5,8]

def tune_runner(trainer, mapfile, name, mapsize):
    global map_sizes
    global args

    if mapsize not in map_sizes:
        return

    if(args.num_goals):
        goals = args.num_goals
    else:
        goals = mapsize
    tune.run(trainer,
             config={"env": MazeEnv,
                     "num_workers":0,
                     "num_envs_per_worker": 1,
                     "env_config": {"mapfile": os.getcwd() + mapfile,
                                    "encoded_state": True,
                                    "randomize_start":args.random_start,
                                    "num_goals": goals,
                                    "randomize_goal": args.random_goals,
                                    "capture_reward":args.reward}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{name}")


# ################################################### #
# # -----------------##Training##-------------------- #
# # ################################################# #
def get_trainer(args):
    trainer = None
    if(args.rl == 'DQN'):
        trainer = dqn.DQNTrainer
    elif(args.rl == 'A3C'):
        trainer = a3c.A3CTrainer
    elif(args.rl == 'PPO'):
        trainer = ppo.PPOTrainer
    else:
        print("please enter valid trainer")
        exit(0)
    return trainer

name = args.rl
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = get_trainer(args)
goals = 3

mapfile = map_loader.get_3x3_map()
mapsize = 3

tune_runner(trainer, mapfile, name, mapsize)

mapfile = map_loader.get_5x5_map()
mapsize = 5

tune_runner(trainer, mapfile, name, mapsize)

mapfile = map_loader.get_8x8_map()
mapsize = 8

tune_runner(trainer, mapfile, name, mapsize)

