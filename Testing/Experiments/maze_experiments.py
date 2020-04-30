
from gym_scalable.envs.grid.maze_env import MazeEnv

from ray.rllib.agents import ppo, ddpg, a3c, dqn
import os
from ray import tune
import argparse
from gym_scalable.envs.grid.maps import map_loader
from pympler.tracker import SummaryTracker
import rllib_trainers
tracker = SummaryTracker()


#Things to tune
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
                     #"num_workers":0,
                     "num_envs_per_worker": 1,
                     "env_config": {"mapfile": mapfile,
                                    "nw_encoded_state": True,
                                    "randomize_start":args.random_start,
                                    "num_goals": goals,
                                    "randomize_goal": args.random_goals,
                                    "capture_reward":args.reward}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": args.steps},
             name=f"{args.name}_maze-{mapsize}x{mapsize}-{name}")


# ################################################### #
# # -----------------##Training##-------------------- #
# # ################################################# #


name = args.rl
trainer = rllib_trainers.get_trainer(name)
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

