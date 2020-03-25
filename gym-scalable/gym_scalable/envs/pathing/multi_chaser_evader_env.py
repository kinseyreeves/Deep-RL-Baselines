'''
Evader vs Chaser Environment
Multi agent

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
from ray.rllib.env import MultiAgentEnv

S_WIDTH = 500

# minimum chaser/evader angle change
DTHETA = 0.2

MAX_STEPS = 200

INT_ACTION = True

mapfile = "out_big.txt"


class GridChaserVsEvaderEnv(MultiAgentEnv):
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
        self.reward = {"chaser":0, "evader": 0}
        self.done = False

        if "mapfile" in config:
            self.map_file = config["mapfile"]
        else:
            print("Error : Please enter a mapfile")
            exit(1)

        # TODO Set Defaults for config:
        self.normalize_state = config["normalize_state"]

        self.randomize_goal = config["randomize_goal"] if "randomize_goal" in config else False
        self.randomize_start = config["randomize_start"] if "randomize_start" in config else False

        self.grid = GridMap(self.map_file, S_WIDTH)
        self.grid.set_render_goals(False)

        # Initialize Entities

        self.evader = Entity(self.grid.goal[0], self.grid.goal[1], self.grid)
        self.chaser = Entity(self.grid.start[0], self.grid.start[1], self.grid)

        self.evader.set_sub_text("Evader")
        self.chaser.set_sub_text("Chaser")

        self.entities = [self.evader, self.chaser]
        self.state = self.reset()

    def step(self, action):
        """
        Step takes a dictionary of actions passed in from the RL agents
        e.g.
        {
            "chaser" : 1,
            "evader" : 2
        }
        :param actions:
        :return:
        """
        chaser_action = utils.convert_1hot_action(action["chaser"], self.action_space.n)
        evader_action = utils.convert_1hot_action(action["evader"], self.action_space.n)
        print(chaser_action)
        # TODO should the AI update first?
        self.chaser.update(chaser_action)

        self.steps += 1
        self.set_state()
        self.reward["evader"] = 1
        self.reward["evader"] = 0

        if self.steps >= MAX_STEPS:
            self.done = True
            return np.array(self.state), self.reward, self.done, {}

        if self.chaser.get_pos() == self.evader.get_pos():
            self.done = True
            self.reward["chaser"] = 1
            self.reward["evader"] = -1

        self.evader.update(evader_action)

        return np.array(self.state), self.reward, self.done, {}

    def set_state(self):

        if self.normalize_state:
            state = [utils.normalize(self.evader.x, 0, self.grid.size),
                          utils.normalize(self.evader.y, 0, self.grid.size),
                          utils.normalize(self.chaser.x, 0, self.grid.size),
                          utils.normalize(self.chaser.y, 0, self.grid.size)]
            self.state = {"evader": state, "chaser": state}
        else:
            state = [self.evader.x, self.evader.y, self.chaser.x, self.chaser.y]
            self.state = {"evader": state, "chaser": state}

    def reset(self):

        self.reward = {"chaser":0, "evader": 0}
        self.steps = 0
        self.done = False
        self.set_state()

        if self.randomize_goal:
            self.grid.set_random_goal()
        if self.randomize_start:
            self.grid.set_random_start()

        # Reset positions
        self.evader.set_pos(self.grid.start)
        self.chaser.set_pos(self.grid.goal)

        return np.array(self.state)

    def render(self, mode='human', close=False):

        if (self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.display.set_caption('RL Chaser Evader Environment')

            pygame.init()
        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        for e in self.entities:
            e.render(self.screen, self.grid.block_width, self.grid.block_height)

        # self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)

        # time.sleep(0.1)
        pygame.display.update()
