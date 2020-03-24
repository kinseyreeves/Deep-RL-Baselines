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


#trainer = ddpg.DDPGTrainer(env=MazeEnv(), config={"env_config": {"extra_joints": 1, "extra_state": False}})

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








