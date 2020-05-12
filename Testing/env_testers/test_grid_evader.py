import gym
import gym_scalable
from gym_scalable.envs.grid.maps import map_loader
import random
import numpy as np
import time
import os
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()

print(os.getcwd())
env = gym.make('n-grid_evaders-v0', config= {"mapfile" : map_loader.get_5x5_map(), "randomize_start":True, "randomize_goal":True, "curriculum" : True, "RL_evader":False})


state = env.reset()
i = 0
goal = env.grid.goal

print(env.observation_space)

while i < 100000:
    #input()
    i += 1
    env.render()
    s = env.reset()
    print(s)
    #print(env.controlled_entity.get_randomness())


    continue
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
    # print(env.grid.start)
    # print(env.grid.goal)
    # print(f"state :  {state}")


    action_ = env.action_space.sample()
   # print(action_)
    state, reward, done, _ = env.step(action_)
    #print(f"{state}  {reward}")

    #print(env.normalize_state)
    if(done):
        env.reset()

    input()
    time.sleep(0.2)

tracker.print_diff()