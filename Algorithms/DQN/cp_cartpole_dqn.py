'''
Cartpole DQN
Author : Kinsey Reeves

Based on Deepminds Deep Q Learning paper
implements :
    - Replay memory use to train in sampled minibatches
    - Periodic updating of target Q network from the training network
'''


import random
from collections import deque

import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


import time




#number of experiences of (s, a, r, s') in memory
MEMORY_SIZE = 1000000
BATCH_SIZE = 20

TRAINING_EPISODES = 1000

LEARNING_RATE = 0.001

MAX_EP_STEPS = 8000

EPSILON_MAX = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

#Number of episodes until we copy our target network to our 
TARGET_UPDATE_EPISODES = 30

#Whether to use interval target updates
TNET_UPDATE = False

Training = False

SAVING = True




GAMMA = 0.95

MODEL_FILENAME = "model_file.h5"

class ReplayMemory:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        buffer_size = len(self.buffer)
        index = np.random.choice(np.arange(buffer_size),
                                size = batch_size,
                                replace = False)

        return [self.buffer[i] for i in index]

class DQN:
    '''
    Deep Q network, Containing a target q network and training q network
    TODO
        Change the network size, find out optimal size for this 
        sort of problem
    '''
    def __init__(self,observation_space,action_space,replay_memory,epsilon):
        self.observation_space = observation_space
        self.action_space = action_space
        self.memory = replay_memory
        self.epsilon = epsilon

        #Generate the target and Q networks.
        self.Q_network = self.generate_model()
        #self.target_Q_network = self.generate_model()
        

    def generate_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(24,input_shape=(self.observation_space,),activation=tf.nn.relu),
            tf.keras.layers.Dense(24, activation=tf.nn.relu),
            tf.keras.layers.Dense(self.action_space, activation=keras.activations.linear)
            ])
        model.compile(optimizer=tf.keras.optimizers.Adam(LEARNING_RATE), 
              loss="mse",
              metrics=['accuracy'])

        return model

    def get_action(self, state):
        
        if Training and np.random.rand() < self.epsilon:
            return random.randrange(self.action_space)
        
        return np.argmax(self.Q_network.predict(state)[0])

    def learn(self):
        
        #If the memory isn't sufficiently initialized, return
        if(len(self.memory.buffer)<BATCH_SIZE):
            return
        
        batch = self.memory.sample(BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            
            
            new_q = reward
            if not terminal:
                new_q = (reward + GAMMA * np.amax(self.Q_network.predict(state_next)[0]))

            start = time.time()
            
            q_vals = self.Q_network.predict(state)
            q_vals[0][action] = new_q
            
            start = time.time()
            self.Q_network.fit(state, q_vals, verbose=0)
            #print("fit : " + str(time.time() - start))

        #print(self.epsilon)
        self.epsilon *= EPSILON_DECAY
        self.epsilon = max(EPSILON_MIN, self.epsilon)
        #print(self.epsilon)

    def copy_network(self):
        '''
        Copies from the Q network to the target network.
        '''
        #if(TNET_UPDATE):
            #self.target_Q_network = tf.keras.models.clone_model(self.Q_network)

    def save(self):
        if(SAVING):
            self.Q_network.save(MODEL_FILENAME)


def train_DQN():
    '''
    Main training loop
    '''
    env = gym.make("CartPole-v1")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    #print(observation_space, action_space)
    memory = ReplayMemory(MEMORY_SIZE)
    dqn = DQN(observation_space, action_space, memory,EPSILON_MAX)

    
    with tf.Session() as sess:
        episode=0

        #Loop for each episode
        while True:
            #print("New Episode")
            state = env.reset()
            state = np.reshape(state, [1, observation_space])

            episode+=1

            if(episode % TARGET_UPDATE_EPISODES==0):
                print("copying network")
                dqn.copy_network()

            if(episode%20==0 and episode >1):
                dqn.save()
                print("saving model")
            
            
            for step in range(MAX_EP_STEPS):
                #Step environment and save to memory
                #Loop for each step in the environment
                #At each step we then sample from our memory and train
                #from our batches.
                
                action = dqn.get_action(state)

                #Environment step
                state_next, reward, terminal, info = env.step(action)

                reward = reward if not terminal else -reward

                state_next = np.reshape(state_next, [1, observation_space])

                memory.add((state,action,reward,state_next,terminal))
                state = state_next

                if(terminal):
                    print("Failed : steps upright" + str(step))
                    break

                #Learn from our minibatches
                dqn.learn()


def test():
    '''
    Function to test the algorithm. Set hyperparameter TRAINING = False
    '''
    env = gym.make("CartPole-v0")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n

    model = keras.models.load_model(MODEL_FILENAME)
    print("Loaded model")

    observation_space = env.observation_space.shape[0]
    episode = 0

    while True:
        #print("New Episode")
        state = env.reset()
        #print(state)
        state = np.reshape(state, [1, observation_space])
        episode+=1
        while True:
            action = np.argmax(model.predict(state)[0])
            #print(action)
            state_next, reward, terminal, info = env.step(action)
            env.render()

            state_next = np.reshape(state_next, [1, observation_space])
            state = state_next

            if terminal:
                break
        

if(Training):
    train_DQN()
else:
    test()
    
