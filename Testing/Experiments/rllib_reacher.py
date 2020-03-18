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


def generate_trainer(joints):

    #trainer = ppo.PPOTrainer(env=NJointArm, config={"env_config": {"extra_joints": joints, "extra_state": False}})
    #
    trainer = ddpg.DDPGTrainer(env=NJointArm, config={"env_config": {"extra_joints": joints, "extra_state": False}})

    #trainer = a3c.A3CTrainer(env=NJointArm, config={"env_config": {"extra_joints": joints, "extra_state": False}})

    return trainer

def run_trainer(trainer, out_file):
    i = 0
    while i < 100:
        stats = trainer.train()
        avg_ep_reward = stats['episode_reward_mean']
        print(f"Epx10 : {i}, average reward : {avg_ep_reward}")
        if (i % 10 == 0):
            print("SAVED CHECKPOINT")
            trainer.save()
        i += 1

if __name__ == "__main__":
    # Can also register the env creator function explicitly with:
    # register_env("corridor", lambda config: SimpleCorridor(config))
    joints = 1
    ray.init()
    for joints in [1]:
        f = open(f"{joints}_joints.csv", "w")
        trainer = generate_trainer(joints)
        run_trainer(trainer, f)








