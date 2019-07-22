import gym
import gym_scalable
import random
import numpy as np


env = gym.make('n-joints-v0')
i=0

print(env.observation_space)
print(env.action_space)
print(env.action_space.sample())
print(env.action_space.n)

while True:
    i+=1
    env.render()
    action_size = env.action_space.n

    action = np.zeros(action_size)
    action[0] = 1
    #action[env.action_space.sample()] = 1
    print(action)
    #for i in range
    state, reward, done, _ = env.step(action)
    print(reward)
    print(state)
    a = input()
    if(i%500==0 or done):
        env.reset()


