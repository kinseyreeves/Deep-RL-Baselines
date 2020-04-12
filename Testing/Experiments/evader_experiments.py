

"""

Single evader (RL controlled) with single chaser (A* controlled) experiments
Kinsey Reeves
"""

from ray.rllib.agents import ppo, ddpg, a3c, dqn
import gym
import os
print(os.getcwd())
from ray import tune
from ray.tune.registry import register_env
from gym_scalable.envs.pathing.chaser_evader_env import GridEvaderEnv
import sys

total_steps = int(sys.argv[1])
def tune_runner(trainer, mapfile, total_steps, name, mapsize):
    print(mapfile)
    tune.run(trainer,
             config={"env": GridEvaderEnv, "env_config": {"mapfile": os.getcwd() + mapfile, "RL_evader":True,
                                                                       "full_state": False, "normalize_state": True,
                                                                       "randomize_start":True, "randomize_goal": True}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": total_steps},
             name=f"evader-{mapsize}x{mapsize}-{name}")


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
del(trainer)

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
del(trainer)


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
del(trainer)


