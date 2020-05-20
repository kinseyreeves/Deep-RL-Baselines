import gym
import numpy as np
from gym_scalable.envs.n_joints import NJointArm
from stable_baselines.ddpg import NormalActionNoise
from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
from stable_baselines import DDPG

env = gym.make('n-joints-v0', config={"extra_joints": 1, "extra_state": False})


# the noise objects for DDPG
n_actions = env.action_space.shape[-1]
param_noise = None
#action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=float(0.5) * np.ones(n_actions))
action_noise = NormalActionNoise(0, 0.5)
model = DDPG(MlpPolicy, env, verbose=1, param_noise=param_noise, action_noise=action_noise)
model.learn(total_timesteps=50000)
model.save("nj")

del model # remove to demonstrate saving and loading

model = DDPG.load("nj")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
    if (dones):
        env.reset()