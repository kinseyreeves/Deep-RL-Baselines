import gym
import numpy as np
import random
from gym_scalable.envs.grid.maps import map_loader
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

"""
Q-Learning, watkins 1991 or as in Sutton and Bartos Reinforcement Learning
"""


class Q_table:

    def __init__(self, state_size, action_size):
        """
        Q table of size states x actions
        """
        self.vals = defaultdict()
        self.action_size = action_size

    def update_qval(self, state, action, val):
        state = tuple(state)
        if state in self.vals:
            self.vals[state][action] = val
        else:
            self.vals[state] = np.zeros(self.action_size)

    def get_action(self, state):
        return np.argmax(self.vals[state])

    def get_qval(self, state, action):
        return self.vals[state][action]

class Q_Dict:

    def __init__(self, state_size, action_size):
        """
        Q table of size states x actions
        """
        self.vals = defaultdict()
        self.action_size = action_size
        self.state_size = state_size

    def update_qval(self, state, action, val):
        state = self.convert_state(state)
        if state in self.vals:
            self.vals[state][action] = val

    def get_action(self, state):
        state = self.convert_state(state)
        if state in self.vals:
            return np.argmax(self.vals[state])
        else:
            self.vals[state] = np.ones(self.action_size)
            return np.argmax(self.vals[state])

    def get_qval(self, state, action):
        state = self.convert_state(state)
        if state in self.vals:
            return self.vals[state][action]
        else:
            self.vals[state] = np.ones(self.action_size)
            return self.vals[state][action]

    def convert_state(self, lst):
        return tuple([int(x) for x in lst])
res_df = pd.DataFrame()

def QLearning(env, episodes, epsilon, lr=0.1, discount=0.99, eps_decay=0.9999):
    """
    Q learning implementation with Qtable
    :param env:
    :param steps:
    :param epsilon:
    :param lr:
    :param discount:
    :param eps_decay:
    :return:
    """
    global res_df
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    Q = Q_Dict(state_size, action_size)
    state = env.reset()

    i = 0
    ep_steps = 0
    ep_lens = []
    while i < episodes:
        #print((i, epsilon))
        epsilon*=eps_decay
        epsilon = max(0.1, epsilon)
        r = random.uniform(0, 1)
        if r < epsilon:
            action = env.action_space.sample()
        else:
            action = Q.get_action(state)

        state_n, reward, done, info = env.step(action)

        # Q(s',a*)
        next_qval = Q.get_qval(state_n, Q.get_action(state_n))

        # Q(s,a) = Q(s,a) + alpha * (r + gamma * Q(s',a*) - Q(s,a))
        #new_qval = (1 - lr) * Q.get_qval(state, action) + lr * (reward + discount * next_qval)
        new_qval = Q.get_qval(state, action) + lr * (reward + discount * next_qval - Q.get_qval(state, action))

        if done:
            i+=1
            ep_lens.append(ep_steps)

            ep_steps = 0
            state = env.reset()
            continue

        Q.update_qval(state, action, new_qval)

        state = state_n

        ep_steps += 1



    res_df[str(env.grid.size)] = ep_lens
    return Q


def eval(env, qt):
    print("Evaluating")
    s = env.reset()
    i = 0
    rewards = []
    while i < 10000:
        env.render()
        action = qt.get_action(s)
        s, reward, done, info = env.step(action)
        rewards.append(reward)
        print(s)
        input()

        if (done):
            i += 1
            #print(np.average(np.array(rewards)))
            env.reset()
            rewards = []

        if(i%1000==0):
            ...
            #print(np.average(np.array(rewards)))


# qt = QLearning(env, 100, 0.1, 0.3, 0.99)
# eval(env, qt)

# qt = QLearning(env, 1000, 0.1, 0.3, 0.99)
# eval(env, qt)

# qt = QLearning(env, 10000, 0.1, 0.3, 0.99)
# eval(env, qt)

config = {"mapfile": map_loader.get_size_map(2), "randomize_start": False, "randomize_goal": False, "curriculum": False, "num_goals": 1,
          "capture_reward": True, "state_encoding": "pos"}
env = gym.make('n-maze-v0', config=config)

qt = QLearning(env, 1000, 0.1)
print(dict(qt.vals))
print("done size 3")
eval(env, qt)
exit(0)
input()

config["mapfile"] = map_loader.get_4x4_map()
env = gym.make('n-maze-v0', config=config)
qt = QLearning(env, 10000, 0.2, 0.1, 0.99)
print("done size 4")

config["mapfile"] = map_loader.get_5x5_map()
env = gym.make('n-maze-v0', config=config)
qt = QLearning(env, 10000, 0.2, 0.1, 0.99)
print("done size 5")

config["mapfile"] = map_loader.get_6x6_map()
env = gym.make('n-maze-v0', config=config)
qt = QLearning(env, 10000, 0.2, 0.1, 0.99)
print("done size 6")

config["mapfile"] = map_loader.get_7x7_map()
env = gym.make('n-maze-v0', config=config)
qt = QLearning(env, 10000, 0.2, 0.1, 0.99)
print("done size 8")

config["mapfile"] = map_loader.get_7x7_map()
env = gym.make('n-maze-v0', config=config)
qt = QLearning(env, 10000, 0.2, 0.1, 0.99)



res_df.to_csv("tabular_results.csv")