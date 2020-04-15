
"""

Single evader (RL controlled) with single chaser (A* controlled) experiments
Kinsey Reeves
"""
import sys

from ray.rllib.agents import ppo, ddpg, a3c, dqn
import gym
import os
print(os.getcwd())
from ray import tune
from ray.tune.registry import register_env
from gym_scalable.envs.grid.chaser_evader_env import GridEvaderEnv
import argparse

parser = argparse.ArgumentParser(description='ChaserEvaser experiment runner')
parser.add_argument('--steps', type=int, default = 5000)
parser.add_argument('--1reward', dest='reward', action='store_true')
parser.add_argument('--name', type = str, default = 'ChaserEvaser')
parser.add_argument('--num_goals', type = int, default = 3)


parser.add_argument('--rl_evader', dest='rl_evader', action='store_true', default = False)
parser.add_argument('--random_goals', dest='random_goals', action='store_true', default = False)
parser.add_argument('--random_start', dest='random_start', action='store_true', default = False)
parser.add_argument('--encode_state', dest='encode_state', action='store_true', default = False)

args = parser.parse_args()

def tune_runner(trainer, mapfile, name, mapsize):
    print(mapfile)
    tune.run(trainer,
             config={"env": GridEvaderEnv,
                     "env_config": {"mapfile": os.getcwd() + mapfile,
                                      "RL_evader":args.rl_evader,
                                      "encode_state":args.encode_state,
                                      "randomize_start":args.random_start,
                                      "randomize_goal": args.random_goals}},
                     checkpoint_freq=10,
                     checkpoint_at_end=True,
                     stop={"timesteps_total": args.steps},

                 name=f"{args.name}-{mapsize}x{mapsize}-{name}")

# ##################################################### #
# # -----------------##PPO##--------------------------- #
# # ################################################### #
name = "PPO"
mapfile = "/maps/map_3x3.txt"
mapsize = 3

trainer = ppo.PPOTrainer

tune_runner(trainer, mapfile, name, mapsize)

mapfile = "/maps/map_5x5.txt"
mapsize = 5

del(trainer)
trainer = ppo.PPOTrainer

tune_runner(trainer, mapfile, name, mapsize)

mapfile = "/maps/map_8x8.txt"
mapsize = 8

del(trainer)
trainer = ppo.PPOTrainer

tune_runner(trainer, mapfile, name, mapsize)

## ################################################### #
## -----------------##DQN##--------------------------- #
## ################################################### #
name = "DQN"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = dqn.DQNTrainer

tune_runner(trainer, mapfile, name, mapsize)

del(trainer)
trainer = dqn.DQNTrainer

mapfile = "/maps/map_5x5.txt"
mapsize = 5

tune_runner(trainer, mapfile, name, mapsize)

del(trainer)
trainer = dqn.DQNTrainer

mapfile = "/maps/map_8x8.txt"
mapsize = 8

tune_runner(trainer, mapfile, name, mapsize)
del(trainer)

## ################################################### #
## -----------------##A3C##--------------------------- #
## ################################################### #

name = "A3C"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = a3c.A3CTrainer

tune_runner(trainer, mapfile, name, mapsize)
del(trainer)
trainer = a3c.A3CTrainer


mapfile = "/maps/map_5x5.txt"
mapsize = 5

tune_runner(trainer, mapfile, name, mapsize)
del(trainer)
trainer = a3c.A3CTrainer

mapfile = "/maps/map_8x8.txt"
mapsize = 8
tune_runner(trainer, mapfile, name, mapsize)
del(trainer)


