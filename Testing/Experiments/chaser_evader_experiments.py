
"""

Single evader (RL controlled) with single chaser (A* controlled) experiments
Kinsey Reeves
"""
import sys

from ray.rllib.agents import ppo, ddpg, dqn, a3c
import gym
import os
print(os.getcwd())
from ray import tune
from ray.tune.registry import register_env
from gym_scalable.envs.grid.chaser_evader_env import ChaserEvaderEnv
from gym_scalable.envs.grid.maps import map_loader
import rllib_trainers
from ray.tune import register_trainable, grid_search, run_experiments
import argparse

parser = argparse.ArgumentParser(description='ChaserEvaser experiment runner')
parser.add_argument('--steps', type=int, default = 200)
parser.add_argument('--1reward', dest='reward', action='store_true')
parser.add_argument('--name', type = str, default = 'ChaserEvaser')
parser.add_argument('--num_goals', type = int, default = 3)

parser.add_argument('--rl', type=str, default = "PPO")
parser.add_argument('--rl_evader', dest='rl_evader', action='store_true', default = False)
parser.add_argument('--random_goals', dest='random_goals', action='store_true', default = False)
parser.add_argument('--random_start', dest='random_start', action='store_true', default = False)
parser.add_argument('--encode_state', dest='encode_state', action='store_true', default = False)
parser.add_argument('--curriculum', dest='curriculum', action='store_true', default = False)
parser.add_argument('--curriculum_eps', type=int, default = 100)


args = parser.parse_args()

map_sizes = [3,5,8]

def tune_runner(trainer, mapfile, name, mapsize):
    print(mapfile)

    if mapsize not in map_sizes:
        return

    tune.run(trainer,
             config={"env": ChaserEvaderEnv,
                     'lr': grid_search([0.0001]),
                     'model': {
                         # 'fcnet_hiddens': grid_search([[128, 128], [256,256]])
                         'fcnet_hiddens': [256, 256],
                     },
                     "env_config": {"mapfile": mapfile,
                                      "RL_evader":args.rl_evader,
                                      "nw_encoded_state":True,
                                      "randomize_start":args.random_start,
                                      "randomize_goal": args.random_goals,
                                      "curriculum": args.curriculum,
                                      "curriculum_eps": args.curriculum_eps
                                    }},
                     checkpoint_freq=10,
                     checkpoint_at_end=True,
                     stop={"timesteps_total": args.steps},

                 name=f"{args.name}-{mapsize}x{mapsize}-{name}")


# ##################################################### #
# # -----------------##Training##---------------------- #
# # ################################################### #
name = args.rl
trainer = rllib_trainers.get_trainer(name)

mapfile = map_loader.get_3x3_map()
mapsize = 3

tune_runner(trainer, mapfile, name, mapsize)

mapfile = map_loader.get_5x5_map()
mapsize = 5

tune_runner(trainer, mapfile, name, mapsize)

mapfile = map_loader.get_8x8_map()
mapsize = 8

tune_runner(trainer, mapfile, name, mapsize)

