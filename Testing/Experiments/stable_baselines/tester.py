import gym
import tensorflow as tf

from gym_scalable.envs.n_joints import NJointArm
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = gym.make('n-joints-v0', config={"extra_joints":1})
# Optional: PPO2 requires a vectorized environment to run
# the env is now wrapped automatically when passing it to the constructor
env = DummyVecEnv([lambda: env])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=100000)

obs = env.reset()
for i in range(100000):
    action, _states = model.predict(obs)
    env.render()
    obs, rewards, dones, info = env.step(action)
    if(dones):
        env.reset()