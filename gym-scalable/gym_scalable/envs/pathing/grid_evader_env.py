'''
Evader environment
Single agent

Author : Kinsey Reeves
Goal:
    evade the chaser as long as possible

Map is made up of:
X - boundary
O - walkable tile
S - start tile
G - goal tile

'''

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random
import time
from gym_scalable.envs import utils
import numpy as np
import os
import math
from gym_scalable.envs.pathing.grid import *

S_WIDTH = 500

# minimum chaser/evader angle change
DTHETA = 0.2

EVADER_SPEED = 6
MAX_SCORE = 200

CAUGHT_DIST = 10

mapfile = "out_big.txt"


class GridEvaderEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''

    def __init__(self, mapfile=None, full_state = False, normalize_state = True):
        self.screen = None
        # Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.Discrete(4)

        # TODO should we normalize or use int vals?
        high = np.array([1, 1, 1, 1, 1])
        low = np.array([0, 0, 0, 0, 0])

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self.centre_x = round(S_WIDTH / 2)
        self.centre_y = round(S_WIDTH / 2)
        self.steps = 0
        self.reward = 0
        self.done = False
        self.normalize_state = False
        self.gridmap = GridMap(mapfile, S_WIDTH)

        self.entity = Entity(self.gridmap.start[0], self.gridmap.start[1], self.gridmap)
        print(f"Env starting entity at {self.gridmap.start[0]} {self.gridmap.start[1]}")

        self.state = self.reset()

        # observation space = [self.x, self.y, enemy.x, enemy.y]
        # self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        self.entity.update(action)

        self.steps += 1
        self.reward = 0

        self.set_state()

        if self.entity.x == self.gridmap.goal[0] and self.entity.y == self.gridmap.goal[1]:
            self.reset()
            self.reward = 1
            self.done = True

        if (self.steps >= MAX_SCORE):
            self.done = True
            return np.array(self.state), self.reward, self.done, {}

        return np.array(self.state), self.reward, self.done, {}


    def set_state(self):
        if(self.normalize_state):
            self.state = [utils.normalize(self.entity.x, 0, self.gridmap.size),
                          utils.normalize(self.entity.y, 0, self.gridmap.size)]
        else:
            self.state = [self.entity.x, self.entity.y]

    def reset(self):
        self.entity.x = self.gridmap.start[0]
        self.entity.y = self.gridmap.start[1]

        self.reward = 0
        self.steps = 0
        self.done = False
        self.set_state()

        return np.array(self.state)

    def render(self, mode='human', close=False):

        # If screen isnt initiated, initiate it, fill it white
        if (self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.init()
        self.screen.fill((255, 255, 255))

        self.gridmap.render(self.screen)
        self.entity.render(self.screen, self.gridmap.block_width, self.gridmap.block_height)

        time.sleep(0.1)
        pygame.display.update()


def out_of_bounds(pos):
    x, y = pos
    if x < 0 or x > S_WIDTH or y < 0 or y > S_WIDTH:
        return True
    return False




