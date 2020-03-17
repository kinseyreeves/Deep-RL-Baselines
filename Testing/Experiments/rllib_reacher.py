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


if __name__ == "__main__":
    # Can also register the env creator function explicitly with:
    # register_env("corridor", lambda config: SimpleCorridor(config))
    ray.init()

    tune.run(
        "PPO",
        stop={
            "timesteps_total": 10000,
        },
        config={
            "env": NJointArm,  # or "corridor" if registered above
            "model": {
                "custom_model": "my_model",
            },
            "vf_share_layers": True,
            "lr": grid_search([1e-2, 1e-4, 1e-6]),  # try different lrs
            "num_workers": 1,  # parallelism
            "env_config": {
                "extra_joints": 2,
                "extra_state" : False
            },
        },
    )