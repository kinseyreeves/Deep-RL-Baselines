import gym
import gym_scalable
import random
import numpy as np
import time
config = { "mapfile" : "maps/map_3x3.txt", "normalize_state" : True, "randomize_start": True, "num_goals":1, "capture_reward":False}
env = gym.make('n-maze-v0',config = config)

state = env.reset()
i = 0

goal = env.grid.goal

print(env.observation_space)
print(env.action_space)

while True:
    
    i += 1
    env.render()
    start = time.time()
    action = env.action_space.sample()
    print(action)

    action_size = env.action_space.n

    print(state.shape)

    state, reward, done, _ = env.step(action)
    print(f"{state}, {reward}, {done}")

    end = time.time()
    print("step time : " + str(end - start))
    if(done):
        #a = input()
        state = env.reset()
    a = input()

