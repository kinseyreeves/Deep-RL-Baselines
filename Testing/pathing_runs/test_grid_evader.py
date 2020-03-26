import gym
import gym_scalable
import random
import numpy as np
import time
import os

print(os.getcwd())
env = gym.make('n-grid_evaders-v0', config= {"mapfile" : "maps/map_8x8.txt", "randomize_start":False, "randomize_goal" : True, "RL_evader":True, "full_state" : False, "normalize_state" : True})

state = env.reset()
i = 0
goal = env.grid.goal

while True:
    i += 1
    env.render()

    #action_ = np.zeros(env.action_space.n)

    #print(action_)
    action_size = env.action_space.n
    #action = np.zeros(action_size)

    #action[env.action_space.sample()] = 1

    #action_ = env.grid.get_astar_action((env.controlled_entity.x, env.controlled_entity.y), (env.evader.x, env.evader.y))
    #print(env.controlled_entity.pos)
    #print(env.evader.pos)
    #path = env.grid.astar_path(*env.controlled_entity.pos, *env.evader.pos)
    #print(path)
    #print(action_)
    #action_ = np.nonzero(action_)[0][0]
    # print(action_)
    # action = 1
    action_ = env.action_space.sample()
    state, reward, done, _ = env.step(action_)
    print(f"state :  {state}")
    print(f"reward : {reward}" )
    print(f"done : {done}")

    #print(env.normalize_state)
    if(done):
        env.reset()
    #input()
    time.sleep(0.5)
