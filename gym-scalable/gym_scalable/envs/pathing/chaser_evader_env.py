'''
Evader or Chaser environment
Single agent

Author : Kinsey Reeves
Goal:
    evade the chaser as long as possible
    Chaser uses A* with some level of randomness

Map is made up of:
These are easily editable in the map file
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

MAX_STEPS = 200

INT_ACTION = True

mapfile = "out_big.txt"


class GridEvaderEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''

    def __init__(self, config):
        self.screen = None
        # Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.Discrete(5)

        # TODO should we normalize or use int vals ?
        high = np.array([1, 1, 1, 1])
        low = np.array([0, 0, 0, 0])

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.centre_x = round(S_WIDTH / 2)
        self.centre_y = round(S_WIDTH / 2)
        self.steps = 0
        self.reward = 0
        self.done = False

        if "mapfile" in config:
            self.map_file = config["mapfile"]
        else:
            print("Error : Please enter a mapfile")
            exit(1)

        # TODO Set Defaults for config:
        self.normalize_state = config["normalize_state"] if "normalize_state" in config else True

        self.RL_evader = config["RL_evader"] if "RL_evader" in config else True
        self.randomize_goal = config["randomize_goal"] if "randomize_goal" in config else False
        self.randomize_start = config["randomize_start"] if "randomize_start" in config else False
        self.slowdown_step = config["slowdown_step"] if "slowdown_step" in config else False

        self.grid = GridMap(self.map_file, S_WIDTH)
        self.grid.set_render_goals(False)

        # Initialize Entities
        if self.RL_evader:
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

        if self.slowdown_step:
            time.sleep(0.3)

        if self.steps >= MAX_STEPS:
            self.done = True
            return np.array(self.state), self.reward, self.done, {}

        # If the action is an arr or 1-hot vector
        if INT_ACTION:
            z_arr = np.zeros(self.action_space.n)
            z_arr[action] = 1
            action = z_arr

        # Set reward whether RL is the evader or chaser
        if self.RL_evader:
            self.reward = 1
        else:
            self.reward = 0

        self.check_done()
        self.controlled_entity.update(action)
        self.check_done()
        self.ai_entity.update_auto()

        self.grid.set_util_text(f"Steps : {self.steps}")

        self.steps += 1
        self.set_state()

        return np.array(self.state), self.reward, self.done, {}

    def check_done(self):
        if self.chaser.get_pos() == self.evader.get_pos():
            self.done = True
            if self.RL_evader:
                self.reward = -1
            else:
                self.reward = 1

    def set_state(self):

        if self.normalize_state:
            self.state = [utils.normalize(self.evader.x, 0, self.grid.size),
                          utils.normalize(self.evader.y, 0, self.grid.size),
                          utils.normalize(self.chaser.x, 0, self.grid.size),
                          utils.normalize(self.chaser.y, 0, self.grid.size)]
        else:
            self.state = [self.evader.x, self.evader.y, self.chaser.x, self.chaser.y]

    def reset(self):
        if (self.slowdown_step):
            time.sleep(0.2)

        self.reward = 0
        self.steps = 0
        self.done = False
        self.set_state()

        if self.randomize_goal:
            self.grid.set_random_goal_spawn()
        if self.randomize_start:
            self.grid.set_random_start()

        # Reset positions
        self.evader.set_pos(self.grid.start)
        self.chaser.set_pos(self.grid.goal)

        return np.array(self.state)

    def render(self, mode='human', close=False):

        if self.screen is None:
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.init()
            pygame.display.set_caption('RL Chaser Evader Environment')

            for e in self.entities:
                e.render_setup(self.screen)

            self.controlled_entity.set_text("R")

            if self.RL_evader:
                self.ai_entity.set_text("C")
            else:
                self.ai_entity.set_text("E")

        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        for e in self.entities:
            e.render(self.screen, self.grid.block_width, self.grid.block_height)

        # self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)

        # time.sleep(0.1)
        pygame.display.update()
