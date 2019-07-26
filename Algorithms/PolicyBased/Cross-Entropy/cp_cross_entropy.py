'''
Cartpole Cross Entropy
Author : Kinsey Reeves

Cross entropy deep RL algorithm.
implements :
    - Neural network with one hidden layer
    - 
    - Periodic updating of target Q network from the training network
'''

import gym
import numpy as np
import tensorflow as tf

from collections import namedtuple

HIDDEN_SIZE = 64
EPISODE_N = 16

PERCENTILE = 70

EPOCH_N = 30

#When to stop training and play
TRAINING_MAX = 400

EpisodeStep = namedtuple('EpisodeStep', field_names=['observation', 'action'])
Episode = namedtuple('Episode', field_names=['reward', 'steps'])

class Model:

    def __init__(self, observation_size, action_size):
        self.model=tf.keras.Sequential([
            tf.keras.layers.Dense(HIDDEN_SIZE, activation = 'relu', input_dim = observation_size),
            tf.keras.layers.Dense(action_size, activation = 'softmax')
        ])
        self.model.compile(optimizer=tf.train.AdamOptimizer(),
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

    def get_action(self, state):
        action_probabilities = self.model.predict(np.asarray([state]), verbose=0)
        print("ap")
        print(action_probabilities)
        action = np.random.choice(len(action_probabilities[0]), p=action_probabilities[0])
        print(action)
        return action

    def train(self, train_observations, train_actions):
        self.model.fit(train_observations, train_actions, epochs=EPOCH_N, verbose=0)

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

        action = network.get_action(state)
        next_state, reward, is_terminal, _ = env.step(action)
        total_reward += reward
        ep_steps.append(EpisodeStep(observation = state, action = action))
        terminal = is_terminal

        state = next_state
    
    print(total_reward)

    return Episode(steps = ep_steps, reward = total_reward)

def cull_episodes(batch):
    '''
    Culls the episodes which fall below the reward boundary
    inputs a batch of Episodes(steps, actions)
    returns a list of states and actions above the reward boundary
    '''
    rewards = [ep.reward for ep in batch]
    reward_bound = np.percentile(rewards,PERCENTILE)

    train_states = []
    train_actions = []

    print(rewards)
    
    reward_mean = float(np.mean(rewards))
    for episode in batch:
        #if the episodes rewad is less than the perctile,
        #skip it
        if episode.reward < reward_bound:
            continue

        train_states.extend([step.observation for step in episode.steps])
        train_actions.extend([step.action for step in episode.steps])

    return train_states, train_actions, reward_mean

def run():

    env = gym.make("CartPole-v1")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n

    network = Model(observation_space, action_space)
    rw_mean = 0
    while True and rw_mean < 400:
        all_eps = []
        for _ in range(EPISODE_N):
            new_ep = run_episode(env,network)
            all_eps.append(new_ep)
        
        states, actions, rw_mean = cull_episodes(all_eps)

        network.train(np.asarray(states), np.asarray(actions))

        print(f"training.. reward: {rw_mean}")
    
    state = env.reset()

    while True:
        env.render()
        action = network.get_action(state)
        
        next_state, reward, terminal, _ = env.step(action)

        if(terminal):
            env.reset()

        state = next_state
            

run()

