import gym
import gym_scalable
import random
import numpy as np
import time
import os
from gym_scalable.envs.pathing.multi_chaser_evader_env import GridChaserVsEvaderEnv

print(os.getcwd())
env = GridChaserVsEvaderEnv(config= {"mapfile" : "maps/map_8x8.txt", "RL_evader":False, "full_state" : False, "normalize_state" : True})

state = env.reset()
i = 0
goal = env.grid.goal

while True:
    i += 1
    env.render()

    action1 = env.action_space.sample()
    action2 = env.action_space.sample()

    state, reward, done, _ = env.step({"evader":action1, "chaser":action2})

    # print(f"state :  {state}")
    # print(f"reward : {reward}")
    # print(f"done : {done}")

    #print(env.normalize_state)
    if(done):
        env.reset()
    input()
    #time.sleep(0.3)
