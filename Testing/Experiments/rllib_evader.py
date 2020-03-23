import numpy as np
import gym
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet_v2 import FullyConnectedNetwork
from gym.spaces import Discrete, Box
from gym_scalable.envs.pathing.chaser_evader_env import GridEvaderEnv

import ray
from ray import tune
from ray.rllib.utils import try_import_tf
from ray.tune import grid_search
from ray.rllib.agents import ppo, ddpg, a3c, dqn
import gym
import os
print(os.getcwd())

#
# def generate_trainer():
#     #trainer = dqn.DQNTrainer(env = GridEvaderEnv, config = {"env_config": {"mapfile" : "map_5x5.txt", "full_state":False, "normalize_state":True}})
#
#     #trainer = ppo.PPOTrainer(env=GridEvaderEnv, config={"env_config": {"mapfile" : "map_5x5.txt", "full_state":False, "normalize_state":True}})
#
#     #trainer = ddpg.DDPGTrainer(env=GridEvaderEnv, config={"env_config": {"mapfile" : "map_5x5.txt", "full_state":False, "normalize_state":True}})
#
#     #trainer = a3c.A3CTrainer(env=GridEvaderEnv, config={"env_config": {"mapfile" : "map_5x5.txt", "full_state":False, "normalize_state":True}})
#
#     return trainer
#
# def run_trainer(trainer, out_file):
#     i = 0
#     while i < 100:
#         stats = trainer.train()
#         print(stats)
#         print(stats['episode_len_mean'])
#         avg_ep_reward = stats['episode_reward_mean']
#         print(f"Epx10 : {i}, average reward : {avg_ep_reward}")
#         if (i % 10 == 0):
#             print("SAVED CHECKPOINT")
#             trainer.save()
#         i += 1
#
# if __name__ == "__main__":
#     # Can also register the env creator function explicitly with:
#     # register_env("corridor", lambda config: SimpleCorridor(config))
#     joints = 1
#     ray.init()
#     for joints in [1]:
#         f = open(f"{joints}_joints.csv", "w")
#         trainer = generate_trainer()
#         run_trainer(trainer, f)
#

###PPO RUNS
joints = 1
tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": 2000000}, name=f"{joints}-Joint-PPO")

joints = 2
tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": 2000000}, name=f"{joints}-Joint-PPO")

joints = 4
tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": 2000000}, name=f"{joints}-Joint-PPO")

###DDPG RUNS
#
joints = 1
tune.run(DDPGTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": 2000000}, name=f"{joints}-Joint-PPO")

joints = 2
tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": 2000000}, name=f"{joints}-Joint-PPO")

joints = 4
tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": 2000000}, name=f"{joints}-Joint-PPO")










