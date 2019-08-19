# Another CE implementation without keras

import gym
import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable
from collections import namedtuple

EpisodeStep = namedtuple('EpisodeStep', field_names=['observation', 'action'])
Episode = namedtuple('Episode', field_names=['reward', 'steps'])

PERCENTILE = 50
EPISODE_N = 50

class Model(nn.Module):

    def __init__(self):

        super().__init__()
        input_size = 4
        output_size = 1

        self.inp = nn.Linear(input_size, 64)

        self.hc1 = nn.Linear(64, output_size)
        self.relu1 = nn.ReLU()
        self.sm = nn.Softmax()


    def forward(self, x):
        x = self.inp(x)
        x = self.relu1(x)
        x = self.hc1(x)
        x = self.sm(x)
        return x

    def get_action(self, state):
        return self.forward(state)


def run_episode(env, network, render=False):
    '''
    Runs a single episode and returns the steps taken and the
    reward as an Episode tuple

    '''
    total_reward = 0
    ep_steps = []

    state = env.reset()

    terminal = False

    while not terminal:
        if (render):
            env.render()

        x_input = Variable(torch.FloatTensor(state))
        action = network.forward(x_input)
        print(action)
        #exit(0)
        next_state, reward, is_terminal, _ = env.step(action)
        exit(0)
        total_reward += reward
        ep_steps.append(EpisodeStep(observation=state, action=action))
        terminal = is_terminal

        state = next_state

    return Episode(steps=ep_steps, reward=total_reward)

def cull_episodes(batch):
    '''
    Culls the episodes which fall below the reward boundary
    inputs a batch of Episodes(steps, actions)
    returns a list of states and actions above the reward boundary
    '''
    rewards = [ep.reward for ep in batch]
    reward_bound = np.percentile(rewards, PERCENTILE)

    train_states = []
    train_actions = []

    # print(rewards)

    reward_mean = float(np.mean(rewards))
    for episode in batch:
        # if the episodes rewad is less than the perctile,
        # skip it
        if episode.reward < reward_bound:
            continue

        train_states.extend([step.observation for step in episode.steps])
        train_actions.extend([step.action for step in episode.steps])

    return train_states, train_actions, reward_mean


def run():
    env = gym.make("CartPole-v1")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n

    net = Model()

    optimizer = torch.optim.Adam(net.parameters(), lr = 0.01)

    rw_mean = 0
    while True and rw_mean < 400:
        all_eps = []
        for _ in range(EPISODE_N):
            new_ep = run_episode(env, net)
            all_eps.append(new_ep)

        states, actions, rw_mean = cull_episodes(all_eps)

        print(states)

        print(f"training.. mean reward: {rw_mean}")
    state = env.reset()


    while True:
        env.render()
        action = net.get_action(state)

        next_state, reward, terminal, _ = env.step(action)

        if terminal:
            env.reset()

        state = next_state

run()