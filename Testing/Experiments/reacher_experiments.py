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


# def generate_trainer(joints):
#
#     #trainer = ppo.PPOTrainer(env=NJointArm, config={"env_config": {"extra_joints": joints, "extra_state": False}})
#     #
#     trainer = ddpg.DDPGTrainer(env=NJointArm, config={"env_config": {"extra_joints": joints, "extra_state": False}})
#
#     #trainer = a3c.A3CTrainer(env=NJointArm, config={"env_config": {"extra_joints": joints, "extra_state": False}})
#
#     return trainer


# def run_trainer(trainer, out_file):
#     i = 0
#     while i < 100:
#         stats = trainer.train()
#         avg_ep_reward = stats['episode_reward_mean']
#         print(f"Epx10 : {i}, average reward : {avg_ep_reward}")
#         print(stats)
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
#         trainer = generate_trainer(joints)
#         run_trainer(trainer, f)



register_env("n-joints-v0", lambda _: NJointArm())
# register_env("n-joints-2-v0", lambda _: NJointArm(config = {"extra_joints": 2, "extra_state": False}))
# register_env("n-joints-4-v0", lambda _: NJointArm(config = {"extra_joints": 4, "extra_state": False}))
# register_env("n-joints-8-v0", lambda _: NJointArm(config = {"extra_joints": 8, "extra_state": False}))
#

total_steps = 1000000

#trainer = ddpg.DDPGTrainer(env=NJointArm, config={"env_config": {"extra_joints": 1, "extra_state": False}})

# ###PPO RUNS
# joints = 1
# tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
#          checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-PPO")
#
# joints = 2
# tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
#          checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-PPO")
#
# joints = 4
# tune.run(PPOTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
#          checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-PPO")
#
# ###DDPG RUNS
# #
# joints = 1
# tune.run(DDPGTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
#          checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-DDPG")
#
# joints = 2
# tune.run(DDPGTrainer, config={"env": "n-joints-v0", "env_config": {"extra_joints": joints, "extra_state": False}},
#          checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-DDPG")

joints = 4
tune.run(DDPGTrainer, config={"env": "n-joints-v0", "num_gpus":1, "env_config": {"extra_joints": joints, "extra_state": False}},
         checkpoint_freq=10, checkpoint_at_end=True, stop = {"timesteps_total": total_steps}, name=f"{joints}-Joint-DDPG")











