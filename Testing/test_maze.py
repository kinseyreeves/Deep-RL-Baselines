import gym
import gym_scalable
import random
import numpy as np
import time

env = gym.make('n-maze-v0', full_state = False, normalize_state = False)
state = env.reset()
i = 0
print(env.gridmap)
goal = env.gridmap.goal

print(   )

while True:
    i += 1
    env.render()
    action = env.get_astar_action(state)

    # action_size = env.action_space.n
    # action = np.zeros(action_size)
    #action[0] = 1

    # action[env.action_space.sample()] = 1
    state, reward, done, _ = env.step(action)

    if(done):
        env.reset()

    #
    print("current pos")
    print(state)
    #
    # print("next move:")
    # print(next)

    print(action)
    time.sleep(1)