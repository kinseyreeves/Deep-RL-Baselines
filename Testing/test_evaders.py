import gym
import gym_scalable
import random
import numpy as np


env = gym.make('n-evaders-v0')
i=0

print(env.observation_space)
print(env.action_space.n)

env.reset()

while True:
    i+=1
    env.render()
    env.step(1)
    print("here")
