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
    #print("evader action ", action)
    state, reward, done, _ = env.step(action)



    if(done):
        print("finished ep, reward : {1} ", reward, state)
        
        env.reset()

    #action = env.action_space.sample()
