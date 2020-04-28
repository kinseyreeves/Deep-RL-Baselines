import gym
import gym_scalable
import random
import numpy as np
import time
from gym_scalable.envs.grid.maps import map_loader

from pympler.tracker import SummaryTracker

tracker = SummaryTracker()


config = { "mapfile" : map_loader.get_5x5_map(), "nw_encoded_state" : True, "randomize_start": True,"curriculum": True, "num_goals":3, "capture_reward":True}
env = gym.make('n-maze-v0',config = config)

state = env.reset()
i = 0

print(env.observation_space)
print(env.action_space)

while i < 100000:

    i += 1
    #env.render()
    start = time.time()
    action = env.action_space.sample()

    action_size = env.action_space.n
    env.render()
    a = input()
    env.reset()
    continue
    #print(env.grid.encode())
    #print(env.grid.get_encoding_shape())
    if(len(state)!=8):
        print(state)
        input()
    state, reward, done, _ = env.step(action)
    #print(f"{state}, {reward}, {done}")
    if(done):
        print(f"finished {i}")

    end = time.time()
    #print("step time : " + str(end - start))
    if(done):
        #a = input()
        state = env.reset()
    #time.sleep(0.1)
    a = input()

tracker.print_diff()

