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


def get_dist(order, coords_list):
    dist = 0
    for i in range(0, len(order) - 1):
        pos = order[i]
        next_pos = order[i + 1]
        dist += env.grid.get_astar_distance(coords_list[pos], coords_list[next_pos])
    return dist

def best_dist(order, coords_list):
    """
    Gets the best possible path distance given the TSP order
    """

    dist_for = 0
    dist_back = 0
    order_for, order_back = None, None
    # print(order)
    for x, pos in enumerate(order):
        if pos == 0:

            order_for = np.concatenate((order[x:], order[:x]))
            order_back = np.concatenate(([order_for[0]], order_for[1:][::-1]))
            # print(order_for)
            # print(order_back)
            dist_for = get_dist(order_for, coords_list)
            dist_back = get_dist(order_back, coords_list)

    if dist_for < dist_back:
        return order_for, dist_for
    return order_back, dist_back

def get_tsp_dist(env):
    #entity_pos = env.entity.get_pos()
    coords_list, dist_list = env.grid.get_dist_list(env.entity.get_pos())

    fitness_coords = mlrose.TravellingSales(coords=coords_list)
    fitness_dists = mlrose.TravellingSales(distances=dist_list)

    problem_fit = mlrose.TSPOpt(length=len(coords_list), fitness_fn=fitness_dists, maximize=False)

    best_state, best_fitness = mlrose.genetic_alg(problem_fit)


    best_states, dist = best_dist(best_state, coords_list)
    print("best_path")

    print(best_states)
    dist = 0
    for i in range(0, len(best_states) - 1):
        pos = best_states[i]
        next_pos = best_states[i + 1]
        print((coords_list[pos],coords_list[next_pos]))

        d = env.grid.get_astar_distance(coords_list[pos], coords_list[next_pos])
        print(d)
        dist += d


    for s in best_states:
        print(coords_list[s])

    print(f"distance: {dist}")

    return dist



i = 0
while i < 100000:

    i += 1
    env.render()
    start = time.time()
    action = env.action_space.sample()
    # print(action)

    action_size = env.action_space.n

    print(get_tsp_dist(env))


    state, reward, done, _ = env.step(action)
    # print(f"{state}, {reward}, {done}")

    end = time.time()
    # print("step time : " + str(end - start))
    input()
    if (done):
        # a = input()
        state = env.reset()
    # a = input()

tracker.print_diff()
