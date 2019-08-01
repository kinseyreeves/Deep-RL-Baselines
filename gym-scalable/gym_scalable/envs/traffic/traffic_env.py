
import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random
import time
from gym_scalable.envs import utils
import numpy as np

#NOTE THIS MUST BE SQUARE, AND MULTIPLE OF 10
S_WIDTH = 200   

B_LEN = 10

EW_ROADS = 1
NS_ROADS = 1

class TrafficEnv(gym.Env):
    
    '''
    Basic single chaser single evader environment
    Env agent controls the evader, which moves at a fixed speed
    with action 1 | 0, to change the angle.
    
    Chaser always moves towards the evader.
    '''

    def __init__(self):
        self.screen = None

        for i in range(0,EW_ROADS):
            


        self.lr_roads = []
        
        #observation space = [self.x, self.y, enemy.x, enemy.y]
        #self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        ...

    def set_state(self):
        ...
    
    def reset(self):
        ...

    def render(self):
        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_WIDTH))
            self.screen.fill((255,255,255))
            pygame.init()
        self.screen.fill((255,255,255))
        pygame.display.update()


class Car:
    
    def __init__(self):
        ...

    def render():
        ...


class Intersection():

    def __init__(self, road1, road2):
        ...

class Road():
    '''
    Road class

    No road really starts and ends, just for simplicity
    '''
    def __init__(self, start_pos, end_pos):
        self.track = []
        self.cars = []

    def render():
        ...

        
