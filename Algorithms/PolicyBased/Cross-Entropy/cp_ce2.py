# Another CE implementation without keras
'''
Cartpole Cross Entropy
Author : Kinsey Reeves

Cross entropy deep RL algorithm.
implements :
    - Neural network with one hidden layer (pytorch)
    -
    - Periodic updating of target Q network from the training network
'''

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

    def __init__(self, input_size, output_size):

        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, output_size)
        )

    def forward(self, x):

        return self.net(x)

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
    sm = nn.Softmax(dim=1)
    while not terminal:
        if (render):
            env.render()

        x_input = Variable(torch.FloatTensor([state]))
        action = network.forward(x_input)
        act_probs_v = sm(action)
        act_probs = act_probs_v.data.numpy()[0]

        action = np.random.choice(len(act_probs), p = act_probs)

        next_state, reward, is_terminal, _ = env.step(action)

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

    net = Model(observation_space, action_space)

    optimizer = torch.optim.Adam(net.parameters(), lr = 0.01)
    loss = nn.CrossEntropyLoss()
    rw_mean = 0
    while True and rw_mean < 400:
        all_eps = []
        for _ in range(EPISODE_N):
            new_ep = run_episode(env, net)
            all_eps.append(new_ep)

        train_states, train_actions, rw_mean = cull_episodes(all_eps)
        train_states = torch.FloatTensor(train_states)
        train_actions = torch.LongTensor(train_actions)

        pred_actions = net.forward(train_states)

        loss_v = loss(pred_actions,train_actions)
        loss_v.backward()
        optimizer.step()
        print(rw_mean)
        optimizer.zero_grad()
        #action_scores = net.forward(train_states)
        #print(action_scores)
        #exit(0)


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