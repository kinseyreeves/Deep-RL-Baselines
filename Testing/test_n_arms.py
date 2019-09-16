import gym
import gym_scalable
import random
import numpy as np

env = gym.make('n-joints-v0')
i = 0


print(env.action_space)
print(env.action_space.sample())
print(env.action_space.shape[0])

print("shape : " , env.observation_space.shape[0])

while True:
    i += 1
    env.render()
    action_size = env.action_space.shape[0]
    #print(action_size)
    #exit(0)
    # print(action_size)
    # print(env.action_space)
    action = env.action_space.sample()

    #print(env.action_space.sample())
    #a = input()
    print(action)
    #action[1] = 0
    # print(action)
    # for i in range
    state, reward, done, _ = env.step(action)
    #print(reward)
    #print(state)
    #a = input()
    # print(reward)
    # print(state)
    # a = input()
    print("reward : ", reward)
    # print(state)
    if (done):
        print("done")
        a = input()
        env.reset()

        env.render()
