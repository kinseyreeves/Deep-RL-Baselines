import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random

import numpy as np

S_WIDTH = 500
S_HEIGHT = 480

N_EVADERS = 1


class Evader():
    
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.screen = None
        #Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.MultiDiscrete((N_EVADERS)*[3])
        #self.observation_space = spaces.
        
        self.centre_x = round(S_WIDTH/2)
        self.centre_y = round(S_HEIGHT/2)

        #observation space = [self.x, self.y, enemy.x, enemy.y]
        self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        '''
       
        '''
        ...
        #return np.array(state), reward, done, {}



    def reset(self):
        ...


    def render(self, mode='human', close=False):

        #If screen isnt initiated, initiate it, fill it white
        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
            self.screen.fill((255,255,255))
            pygame.init()
        self.screen.fill((255,255,255))

        pygame.display.update()


    def reset_objective(self):
        '''
        Initialises the objective
        '''
        ...


class Evader:

    def __init__(x, y):
        self.x = x
        self.y = y
