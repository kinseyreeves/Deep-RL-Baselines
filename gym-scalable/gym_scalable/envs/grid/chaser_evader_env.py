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
from gym_scalable.envs.grid.grid import *
from gym_scalable.envs.grid.grid_entity import *
from gym_scalable.envs.grid.grid_env import *


class ChaserEvaderEnv(gym.Env, GridEnv):
    metadata = {'render.modes': ['human']}

    '''
    Evader or chaser environment
    '''

    def __init__(self, config):
        GridEnv.__init__(self, config)
        self.RL_evader = config["RL_evader"] if "RL_evader" in config else True
        if (self.RL_evader):
            print(f"Started RL evader environment with config:{config}")
        else:
            print(f"Started RL Chaser environment with config:{config}")

        if self.encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_walls_shape(),
                                                dtype=np.float32)
        elif self.nw_encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_nowalls_shape(),
                                                dtype=np.float32)
        else:
            m = self.grid.get_tabular_encoding_size()
            high = np.array([m,m])
            low = np.array([0,0])
            self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

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

        if self.curriculum:
            self.controlled_entity.set_randomness(self.get_curriculum_value())

        self.entities = [self.evader, self.chaser]

    def step(self, action):
        GridEnv.step(self, action)

        if self.steps >= self.max_steps:
            self.done = True
            return np.array(self.state), self.reward, self.done, {}

        if self.RL_evader:
            self.reward = 1
        else:
            self.reward = -.1

        self.check_done()
        self.controlled_entity.update(self.action)
        self.check_done()
        self.ai_entity.update_auto()

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
        if self.encoded_state:
            self.state = self.grid.encode(entities=self.entities)
        elif self.nw_encoded_state:
            self.state = self.grid.encode_no_walls(entities=self.entities)
        else:
            encoding = self.grid.encode_tabular([e.get_pos() for e in self.entities])
            if self.normalize_state:
                self.state = utils.normalize(encoding, 0, self.grid.get_tabular_encoding_size())
            else:
                self.state = encoding

    def reset(self):

        GridEnv.reset(self)
        self.set_state()

        if self.curriculum:
            self.controlled_entity.set_randomness(self.get_curriculum_value())
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
            pygame.init()
            pygame.display.set_caption('RL Chaser Evader Environment')

            for e in self.entities:
                e.render_setup(self.screen)

            self.controlled_entity.set_text("R")

            if self.RL_evader:
                self.ai_entity.set_text("C")
            else:
                self.ai_entity.set_text("E")
        GridEnv.render(self)

        for e in self.entities:
            e.render(self.screen, self.grid.block_width, self.grid.block_height)

        pygame.display.update()

    def check_done(self):
        """
        Checks if the state is complete by evaluating entity positons
        :return:
        """
        if self.chaser.get_pos() == self.evader.get_pos():
            self.done = True
            if self.RL_evader:
                self.reward = -1
            else:
                self.reward = 1

    def set_state(self):
        """
        Sets the state
        :return:
        """
        if self.encoded_state:
            self.state = self.grid.encode(entities=self.entities)
        elif self.nw_encoded_state:
            self.state = self.grid.encode_no_walls(entities=self.entities)
        else:
            if self.normalize_state:
                self.state = [utils.normalize(self.evader.x, 0, self.grid.size),
                              utils.normalize(self.evader.y, 0, self.grid.size),
                              utils.normalize(self.chaser.x, 0, self.grid.size),
                              utils.normalize(self.chaser.y, 0, self.grid.size)]
            else:
                self.state = [self.evader.x, self.evader.y, self.chaser.x, self.chaser.y]
