import gym
import gym_scalable
import random
import numpy as np

env = gym.make('n-joints-v0',  config = {"extra_joints": 1, "extra_state": False})
i = 0

# print(env.action_space)
# print(env.observation_space.shape)
# print(env.action_space.shape)
#
#
# print(type(env.action_space))
# print(type(env.observation_space))
# state = env.reset()
#
# input()
# print("shape : " , env.observation_space.shape[0])

while True:
    i += 1
    env.render()
    action_size = env.action_space.shape[0]
    #print(action_size)
    #exit(0)
    # print(action_size)
    # print(env.action_space)
    action = env.action_space.sample()

    #print(action)
    #action[1] = 0
    # print(action)
    # for i in range
    state, reward, done, _ = env.step(action)
    print(state)
    for val in state:
        if(val>1 or val < -1):
            print("bad")
            input()
    # print(i)
    # print("reward : ", reward)
    # print(state)
    if (done):
        print("done")
        #a = input()
        env.reset()

        env.render()
