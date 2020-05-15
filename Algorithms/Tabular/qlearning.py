import gym
import numpy as np
import random

"""
Q-Learning, watkins 1991 or as in Sutton and Bartos Reinforcement Learning
"""

env = gym.make("Taxi-v3")

s = env.reset()

steps = 1000


class Q_table:

    def __init__(self, state_size, action_size):
        """
        Q table of size states x actions
        """
        self.vals = np.ones((state_size, action_size))

    def update_qval(self, state, action, val):
        self.vals[state][action] = val

    def get_action(self, state):
        return np.argmax(self.vals[state])

    def get_qval(self, state, action):
        return self.vals[state][action]


def QLearning(env, steps, epsilon, lr, discount):
    state_size = env.observation_space.n
    action_size = env.action_space.n

    Q = Q_table(state_size, action_size)
    state = env.reset()
    action = Q.get_action(state)
    i = 0
    while i < steps:
        r = random.uniform(0, 1)
        if (r < epsilon):
            action = env.action_space.sample()
        else:
            action = Q.get_action(state)

        state_n, reward, done, info = env.step(action)
        # Q(s',a*)
        next_qval = Q.get_qval(state_n, Q.get_action(state_n))

        # Q(s,a) = Q(s,a) + alpha * (r + gamma * Q(s',a*) - Q(s,a))
        new_qval = (1 - lr) * Q.get_qval(state, action) + lr * (reward + discount * next_qval)

        Q.update_qval(state, action, new_qval)

        state = state_n

        i += 1

        if (done):
            state = env.reset()
    return Q


def eval(env, qt):
    print("Evaluating")
    s = env.reset()
    i = 0
    rewards = []
    while i < 10:

        action = qt.get_action(s)
        s, reward, done, info = env.step(action)
        rewards.append(reward)
        input()
        env.render()
        if (done):
            i += 1
            print(np.average(np.array(rewards)))
            env.reset()
            rewards = []


# qt = QLearning(env, 100, 0.1, 0.3, 0.99)
# eval(env, qt)


# qt = QLearning(env, 1000, 0.1, 0.3, 0.99)
# eval(env, qt)

# qt = QLearning(env, 10000, 0.1, 0.3, 0.99)
# eval(env, qt)


qt = QLearning(env, 100000, 0.1, 0.3, 0.99)
eval(env, qt)