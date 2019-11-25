from collections import deque
import numpy as np
import random
import gym

class ReplayMemory:
    def __init__(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.is_terminals = []

    def clear_memory(self):
        del self.actions[:]
        del self.states[:]
        del self.logprobs[:]
        del self.rewards[:]
        del self.is_terminals[:]

    def sample(self, batch_size = 128):
        idx = random.randint(0,len(self.actions)-batch_size)
        return self.states[idx:idx+batch_size],\
               self.actions[idx:idx+batch_size],\
               self.logprobs[idx:idx+batch_size],\
               self.rewards[idx:idx+batch_size],\
               self.is_terminals[idx:idx+batch_size]

