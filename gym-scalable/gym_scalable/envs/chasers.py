
import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random

import numpy as np

S_WIDTH = 500
S_HEIGHT = 480


class Chasers(gym.Env):
    '''
    N-Chasers M-Evaders problem.
    For simplicity we will start with 1 chaser and 1 simple evader.
    The evader will have evade by going towards a distance maximising
    position.

        Action space:
            N-Chasers * 3
                Turn clockw, anticw, and dont turn
        
        Observation space:
            Position of self, position of all chasers
    '''
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.screen = None
        #Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.MultiDiscrete((N_CHASERS)*[3])
        #self.observation_space = spaces.
        
        self.centre_x = round(S_WIDTH/2)
        self.centre_y = round(S_HEIGHT/2)

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

class Mover:
    
    def __init__(x, y):
        ...
    def render():
        ...

    def collides(enemy):
        ...

class Chaser(Mover):
    ...

class Evader(Mover):
    ...

