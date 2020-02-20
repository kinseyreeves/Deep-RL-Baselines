import gym
import gym_scalable
import random
import numpy as np

env = gym.make('n-maze-v0')
i = 0

while True:
    i += 1
    env.render()
    # action_size = env.action_space.n

    # action = np.zeros(action_size)
    # action[0] = 1
    # action[env.action_space.sample()] = 1
    # print(action)
    # for i in range
    env.step(1)
    # a = input()
    # print("step")


