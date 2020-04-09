import gym
import gym_scalable
import random
import numpy as np
import time
import os
import mlrose
print(os.getcwd())
from pympler.tracker import SummaryTracker

tracker = SummaryTracker()

config = {"mapfile": "/home/krer/Documents/Deep-RL-Baselines/gym-scalable/gym_scalable/envs/pathing/mazes/map_3x3.txt",
          "normalize_state": True, "randomize_start": True, "num_goals": 3,
          "capture_reward": False}
env = gym.make('n-maze-v0', config=config)

state = env.reset()


goal = env.grid.goal


entity_pos = env.entity.get_pos()
coords_list , dist_list = env.grid.get_dist_list(env.entity.get_pos())

print(dist_list)
print(coords_list)
fitness_coords = mlrose.TravellingSales(coords = coords_list)
fitness_dists = mlrose.TravellingSales(distances = dist_list)

problem_fit = mlrose.TSPOpt(length = len(coords_list), fitness_fn = fitness_coords, maximize=False)

best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2,
                                              max_attempts = 100, random_state = 2)



def full_dist(coords_list, order):
    dist = 0
    print(order)
    for x,pos in enumerate(order):
        if(pos==0):
            order_for = np.concatenate((order[x:],order[:x]))
            print(order_for)
            
            order_back = np.concatenate(([order_for[0]],order_for[1:][::-1]))

            print(order_back)
            print(order_for)


            break

    for i in range(0, len(order)-1):
        pos = order[i]
        next_pos = order[i+1]
        dist+= env.grid.get_astar_distance(coords_list[pos],coords_list[next_pos])
    return dist

print("best path")
for idx in best_state:
    print(coords_list[idx])
print(full_dist(coords_list, best_state))


i = 0
while i < 100000:
    input()
    i += 1
    env.render()
    start = time.time()
    action = env.action_space.sample()
    # print(action)

    action_size = env.action_space.n

    # print(state.shape)

    state, reward, done, _ = env.step(action)
    # print(f"{state}, {reward}, {done}")

    end = time.time()
    # print("step time : " + str(end - start))
    if (done):
        # a = input()
        state = env.reset()
    # a = input()

tracker.print_diff()

