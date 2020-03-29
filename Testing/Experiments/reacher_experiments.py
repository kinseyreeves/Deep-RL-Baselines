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


logdir = "~/ray_results/maze"


# def tune_runner(trainer, name):
#     tune.run(trainer,
#              config={"env": NJointArm, "output" : logdir, "env_config": {"extra_joints": 3, "full_state": False, "normalize_state": True}},
#              checkpoint_freq=10, checkpoint_at_end=True, stop={"timesteps_total": total_steps},
#              name=f"nj-{name}")
#
#
#
# ###PPO RUNS
# tune_runner(ddpg.DDPGTrainer, "PPO")
total_steps = 1000000

joints = 1
tune.run(PPOTrainer, config={"env": NJointArm, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-PPO")

joints = 2
tune.run(PPOTrainer, config={"env": NJointArm, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-PPO")

joints = 4
tune.run(PPOTrainer, config={"env": NJointArm, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-PPO")

###DDPG RUNS
#
joints = 1
tune.run(DDPGTrainer, config={"env": NJointArm, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-DDPG")

joints = 2
tune.run(DDPGTrainer, config={"env": NJointArm, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-DDPG")

joints = 4
tune.run(DDPGTrainer, config={"env": NJointArm, "num_gpus":1, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-DDPG")











