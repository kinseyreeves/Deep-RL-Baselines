"""

Single evader (RL controlled) with single chaser (A* controlled) experiments
Kinsey Reeves
"""

import os

from ray.rllib.agents import ppo, a3c, dqn

print(os.getcwd())
from ray import tune
from gym_scalable.envs.grid.multi_chaser_evader_env import GridChaserVsEvaderEnv
import sys

total_steps = int(sys.argv[1])
EXP_NAME = "ChaserVsEvader"
action_space = GridChaserVsEvaderEnv.action_space
obs_space = GridChaserVsEvaderEnv.observation_space


def tune_runner(trainer, mapfile, total_steps, name, mapsize):
    print(mapfile)
    tune.run(trainer,
             config={"env": GridChaserVsEvaderEnv,
                     "multiagent": {
                         "chaser": (None, obs_space, action_space, {"gamma": 0.99}),
                         "evader": (None, obs_space, action_space, {"gamma": 0.99})
                     },
                     "env_config": {"mapfile": os.getcwd() + mapfile,
                                    "full_state": False,
                                    "normalize_state": True,
                                    "randomize_start": True,
                                    "randomize_goal": True}
                     },
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": total_steps},
             name=f"{EXP_NAME}-{mapsize}x{mapsize}-{name}")


## ##################################################### #
## # -----------------##PPO##--------------------------- #
## # ################################################### #
name = "PPO"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = ppo.PPOTrainer

tune_runner(trainer, mapfile, total_steps, name, mapsize)

mapfile = "/maps/map_5x5.txt"
mapsize = 5

tune_runner(trainer, mapfile, total_steps, name, mapsize)

mapfile = "/maps/map_8x8.txt"
mapsize = 8

tune_runner(trainer, mapfile, total_steps, name, mapsize)

## ################################################### #
## -----------------##DQN##--------------------------- #
## ################################################### #
name = "DQN"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = dqn.DQNTrainer

tune_runner(trainer, mapfile, total_steps, name, mapsize)

mapfile = "/maps/map_5x5.txt"
mapsize = 5

tune_runner(trainer, mapfile, total_steps, name, mapsize)

mapfile = "/maps/map_8x8.txt"
mapsize = 8

tune_runner(trainer, mapfile, total_steps, name, mapsize)

## ################################################### #
## -----------------##A3C##--------------------------- #
## ################################################### #

name = "A3C"
mapfile = "/maps/map_3x3.txt"
mapsize = 3
trainer = a3c.A3CTrainer

tune_runner(trainer, mapfile, total_steps, name, mapsize)

mapfile = "/maps/map_5x5.txt"
mapsize = 5

tune_runner(trainer, mapfile, total_steps, name, mapsize)

mapfile = "/maps/map_8x8.txt"
mapsize = 8

tune_runner(trainer, mapfile, total_steps, name, mapsize)
