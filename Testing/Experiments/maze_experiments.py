import numpy as np
import gym
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet_v2 import FullyConnectedNetwork
from gym.spaces import Discrete, Box
from gym_scalable.envs.pathing.chaser_evader_env import GridEvaderEnv
from gym_scalable.envs.pathing.maze_env import MazeEnv

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

from pympler.tracker import SummaryTracker

tracker = SummaryTracker()


logdir = "~/ray_results/maze"
total_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

a = os.getcwd() + "/maps/map_3x3.txt"


def tune_runner(trainer, mapfile, total_steps, name, mapsize, goals):
    print(mapfile)
    tune.run(trainer,
             config={"env": MazeEnv,
                     "num_workers":1,
                     "env_config": {"mapfile": os.getcwd() + mapfile,
                                    "normalize_state": True,
                                    "randomize_start":True,
                                    "randomize_goal": True,
                                    "num_goals": goals,
                                    "capture_reward":False}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": total_steps},
             name=f"maze-{mapsize}x{mapsize}-{name}")


# ################################################### #
# # -----------------##PPO##--------------------------- #
# # ################################################### #
name = "PPO"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = ppo.PPOTrainer
goals = 3
tracker.print_diff()
tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

mapfile = "/maps/map_5x5.txt"
mapsize = 5
tracker.print_diff()
tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

mapfile = "/maps/map_8x8.txt"
mapsize = 8
tracker.print_diff()
tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)
del(trainer)
tracker.print_diff()
# ################################################### #
# -----------------##DQN##--------------------------- #
# ################################################### #
name = "DQN"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = dqn.DQNTrainer

tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

mapfile = "/maps/map_5x5.txt"
mapsize = 5
tracker.print_diff()
tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

mapfile = "/maps/map_8x8.txt"
mapsize = 8

tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)
del(trainer)
tracker.print_diff()
################################################### #
###-----------------##A3C##------------------------ #
################################################### #

name = "A3C"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = a3c.A3CTrainer

tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

mapfile = "/maps/map_5x5.txt"
mapsize = 5

tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

mapfile = "/maps/map_8x8.txt"
mapsize = 8

tune_runner(trainer, mapfile, total_steps, name, mapsize, goals)

del(trainer)

tracker.print_diff()