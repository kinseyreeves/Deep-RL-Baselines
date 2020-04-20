import gym
import gym_scalable
import random
import numpy as np
import time
import os
from pympler.tracker import SummaryTracker
from gym_scalable.envs.grid.maps import map_loader

tracker = SummaryTracker()

print(os.getcwd())
env = gym.make('n-grid_evaders-v0', config= {"mapfile" : map_loader.get_5x5_map(),
                                             "encoded_state":True,
                                             "randomize_start":True,
                                             "randomize_goal" : True,
                                             "RL_evader":False,
                                             "full_state" : False,
                                             "normalize_state" : True}
               )

state = env.reset()
i = 0
goal = env.grid.goal

print(env.observation_space)
total = 0
steps = 0
step_totals = []

while total<10000:

    #input()
    i += 1
    env.render()

    action_size = env.action_space.n

    action_ = env.grid.get_astar_action((env.controlled_entity.x, env.controlled_entity.y), (env.evader.x, env.evader.y))

    action_ = np.nonzero(action_)[0][0]
    steps+=1
    state, reward, done, _ = env.step(action_)
    time.sleep(0.1)
    if done:
        step_totals.append(steps)
        steps = 0
        total+=1
        env.reset()

print(step_totals)
output = np.average(step_totals)
print(f"On average, the A* chaser takes {output} steps to reach the evader")



#tracker.print_diff()