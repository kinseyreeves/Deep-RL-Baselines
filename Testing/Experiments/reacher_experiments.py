import numpy as np
import gym
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet_v2 import FullyConnectedNetwork
from gym.spaces import Discrete, Box
from gym_scalable.envs.n_joints import NJointArm

import ray
from ray import tune
from ray.rllib.utils import try_import_tf
from ray.tune import grid_search
from ray.rllib.agents import ppo, ddpg, a3c, dqn
import gym
from ray import tune
from ray.tune.registry import register_env
from gym_scalable.envs.n_joints import NJointArm
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.ddpg import DDPGTrainer
import sys

def nj_runner(trainer, name, nj):
    tune.run(trainer,
             config={"env": NJointArm, "env_config": {"extra_joints": nj, "full_state": False, "normalize_state": True}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": total_steps},
             name=f"{nj}-joints-{name}")

def ddpg_nj_runner(trainer, name, nj):
    tune.run(trainer,
             config={"env": NJointArm,
                     "buffer_size": 5000,
                     "smooth_target_policy":True,
                     #"exploration_config":{"type":"GaussianNoise"},
                     #"timesteps_per_iteration": 1000,
                     "exploration_should_anneal": True,
                     #"exploration_noise_type": "gaussian",
                     "env_config": {"extra_joints": nj, "full_state": False, "normalize_state": True}},
             checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": total_steps},
             name=f"{nj}-joints-{name}",)
###DDPG RUNS
total_steps = int(sys.argv[1])
trainer = DDPGTrainer
name = "DDPG"
joints = 1
ddpg_nj_runner(trainer, name, joints)
joints = 2
ddpg_nj_runner(trainer, name, joints)
joints = 4
ddpg_nj_runner(trainer, name, joints)
del(trainer)

#
# ###PPO RUNS
# tune_runner(ddpg.DDPGTrainer, "PPO")
name = "PPO"

trainer = PPOTrainer
joints = 1
nj_runner(trainer, name, joints)
joints = 2
nj_runner(trainer, name, joints)
joints = 4
nj_runner(trainer, name, joints)

del(trainer)









