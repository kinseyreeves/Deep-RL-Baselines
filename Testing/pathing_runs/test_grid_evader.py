import gym
import gym_scalable
import random
import numpy as np
import time
import os

print(os.getcwd())
env = gym.make('n-grid_evaders-v0', config= {"mapfile" : "maps/map_5x5.txt", "full_state" : False, "normalize_state" : True})

state = env.reset()
i = 0
goal = env.gridmap.goal

while True:
    i += 1
    env.render()

    action_ = np.zeros(env.action_space.n)
    action_[env.action_space.sample()] = 1

    action_size = env.action_space.n
    action = np.zeros(action_size)

    action[env.action_space.sample()] = 1
    state, reward, done, _ = env.step(action_)
    print(f"state :  {state}")
    print(f"reward : {reward}" )
    print(f"done : {done}")
    print(env.normalize_state)
    if(done):
        env.reset()

    #time.sleep(0.1)