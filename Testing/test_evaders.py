import gym
import gym_scalable
import random
import numpy as np


env = gym.make('n-evaders-v0')
i=0



print(env.observation_space)
print(env.action_space.n)
print(env.action_space.sample())

env.reset()

while True:
    i+=1
    env.render()
    action = env.action_space.sample()
    print("evader action ", action)
    env.step(action)
    #action = env.action_space.sample()
