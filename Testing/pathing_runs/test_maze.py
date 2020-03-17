import gym
import gym_scalable
import random
import numpy as np
import time

env = gym.make('n-maze-v0', mapfile = "maps/map_5x5.txt", full_state = False, normalize_state = False)

state = env.reset()
i = 0

goal = env.gridmap.goal

while True:
    
    i += 1
    env.render()
    action_ = env.gridmap.get_astar_action(state, env.gridmap.goal)

    action_size = env.action_space.n
    action = np.zeros(action_size)

    action[env.action_space.sample()] = 1
    state, reward, done, _ = env.step(action_)

    if(done):
        env.reset()
