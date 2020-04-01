import gym
import gym_scalable
import random
import numpy as np
import time
config = { "mapfile" : "maps/map_5x5.txt", "normalize_state" : True, "randomize_start": True, "num_goals":3}
env = gym.make('n-maze-v0',config = config)

state = env.reset()
i = 0

goal = env.grid.goal


while True:
    
    i += 1
    env.render()
    start = time.time()
    action = env.action_space.sample()

    action_size = env.action_space.n
    #action = np.zeros(action_size)
    # print(action)
    # print(action_)
    #action[env.action_space.sample()] = 1

    state, reward, done, _ = env.step(action)
    print((state,reward,done))
    end = time.time()
    print("step time : " + str(end - start))
    if(done):
        a = input()
        env.reset()
    a = input()

