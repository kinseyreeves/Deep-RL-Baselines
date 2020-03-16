import gym
import gym_scalable
import random
import numpy as np
import time

env = gym.make('n-maze-v0', mapfile = "out_big.txt", full_state = False, normalize_state = False)

state = env.reset()
i = 0
print(env.gridmap)
goal = env.gridmap.goal


while True:
    i += 1
    env.render()
    action_ = env.gridmap.get_astar_action(state, env.gridmap.goal)
    print(action_)

    action_size = env.action_space.n
    action = np.zeros(action_size)
    #action[0] = 1

    action[env.action_space.sample()] = 1
    state, reward, done, _ = env.step(action_)

    if(done):
        env.reset()


    #time.sleep(0.1)