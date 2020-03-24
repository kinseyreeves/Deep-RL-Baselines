'''
Evader environment
Single agent

Author : Kinsey Reeves
Goal:
    evade the chaser as long as possible
    Chaser uses A* with some level of randomness

Map is made up of:
X - boundary
O - walkable tile
S - start tile
G - goal tile

'''

import pygame
import math
import random
import time
import gym
import os
import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding
from gym_scalable.envs import utils
from gym_scalable.envs.pathing.grid import *
from gym_scalable.envs.pathing.grid_entity import *

S_WIDTH = 500

# minimum chaser/evader angle change
DTHETA = 0.2

EVADER_SPEED = 6
MAX_SCORE = 200

CAUGHT_DIST = 10

INT_ACTION = True

mapfile = "out_big.txt"


class GridEvaderEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''

    def __init__(self,
                 config={"mapfile": "map_5x5.txt", "RL_evader": True, "full_state": False, "normalize_state": True}):
        self.screen = None
        # Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.Discrete(5)

        # TODO should we normalize or use int vals?
        high = np.array([1, 1, 1, 1])
        low = np.array([0, 0, 0, 0])

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.centre_x = round(S_WIDTH / 2)
        self.centre_y = round(S_WIDTH / 2)
        self.steps = 0
        self.reward = 0
        self.done = False

        # TODO Set Defaults for config:
        self.normalize_state = config["normalize_state"]
        self.grid = GridMap(config["mapfile"], S_WIDTH)
        self.grid.set_render_goals(False)
        self.RL_evader = config["RL_evader"]

        # Initialize Entities
        if (self.RL_evader):
            self.evader = Entity(self.grid.goal[0], self.grid.goal[1], self.grid)
            self.chaser = AStarChaser(self.grid.start[0], self.grid.start[1], self.grid)
            self.controlled_entity = self.evader
            self.chaser.set_chasing(self.evader)
            self.ai_entity = self.chaser
        else:
            self.chaser = Entity(self.grid.goal[0], self.grid.goal[1], self.grid)
            self.evader = AStarEvader(self.grid.start[0], self.grid.start[1], self.grid)
            self.controlled_entity = self.chaser
            self.evader.set_evading(self.chaser)
            self.ai_entity = self.evader

        self.entities = [self.evader, self.chaser]
        self.state = self.reset()

    def step(self, action):

        # If the action is an arr or 1-hot vector
        if INT_ACTION:
            z_arr = np.zeros(self.action_space.n)
            z_arr[action] = 1
            action = z_arr

        # if the evader is RL controlled, update with the action
        # Otherwise chaser updates with the action
        if (self.RL_evader):
            # Reward is 1 for each step NOT caught
            self.controlled_entity.update(action)
            # self.chaser.update_auto()
            self.reward = 1
        else:
            self.controlled_entity.update(action)
            # self.evader.update_auto()
            self.reward = 0

        self.steps += 1
        self.set_state()

        if self.steps >= MAX_SCORE:
            self.done = True
            return np.array(self.state), self.reward, self.done, {}

        if self.chaser.get_pos() == self.evader.get_pos():
            self.done = True

            if (self.RL_evader):
                self.reward = -1
            else:
                self.reward = 1

        self.ai_entity.update_auto()

        return np.array(self.state), self.reward, self.done, {}

    def set_state(self):

        if self.normalize_state:
            self.state = [utils.normalize(self.evader.x, 0, self.grid.size),
                          utils.normalize(self.evader.y, 0, self.grid.size),
                          utils.normalize(self.chaser.x, 0, self.grid.size),
                          utils.normalize(self.chaser.y, 0, self.grid.size)]
        else:
            self.state = [self.evader.x, self.evader.y, self.chaser.x, self.chaser.y]

    def reset(self):

        self.reward = 0
        self.steps = 0
        self.done = False
        self.set_state()

        # reset positions
        self.evader.set_pos(self.grid.start)
        self.chaser.set_pos(self.grid.goal)

        return np.array(self.state)

    def render(self, mode='human', close=False):

        if (self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.init()
        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        for e in self.entities:
            e.render(self.screen, self.grid.block_width, self.grid.block_height)

        # self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)

        # time.sleep(0.1)
        pygame.display.update()
