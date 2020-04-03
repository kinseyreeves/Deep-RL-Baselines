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

MAX_STEPS = 200

INT_ACTION = True

class GridChaserVsEvaderEnv(MultiAgentEnv):
    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''

    high = np.array([1, 1, 1, 1])
    low = np.array([0, 0, 0, 0])

    observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
    action_space = spaces.Discrete(4)

    def __init__(self, config):
        self.screen = None
        # Action space initialised to [-1,0,1] for each joint


        # TODO should we normalize or use int vals ?

        self.centre_x = round(S_WIDTH / 2)
        self.centre_y = round(S_WIDTH / 2)
        self.steps = 0
        self.reward = {"chaser":0, "evader": 0}
        self.done = {"chaser":False, "evader":False}

        if "mapfile" in config:
            self.map_file = config["mapfile"]
        else:
            print("Error : Please enter a mapfile")
            exit(1)

        # TODO Set Defaults for config:
        self.normalize_state = config["normalize_state"] if "normalize_state" in config else True

        self.randomize_goal = config["randomize_goal"] if "randomize_goal" in config else False
        self.randomize_start = config["randomize_start"] if "randomize_start" in config else False
        self.slowdown_step = config["slowdown_step"] if "slowdown_step" in config else False


        self.grid = GridMap(self.map_file, S_WIDTH)
        self.grid.set_render_goals(False)

        # Initialize Entities

        self.evader = Entity(self.grid.goal[0], self.grid.goal[1], self.grid)
        self.chaser = Entity(self.grid.start[0], self.grid.start[1], self.grid)



        self.entities = [self.evader, self.chaser]
        self.state = self.reset()

    def set_reward(self):
        dist = self.grid.manhatten_dist(*self.evader.get_pos(), *self.chaser.get_pos())
        #dist = self.grid.get_astar_distance(*self.evader.get_pos(), *self.chaser.get_pos())
        self.reward["evader"] = dist
        self.reward["chaser"] = -dist

    def step(self, actions):
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
        if self.slowdown_step:
            time.sleep(0.3)

        chaser_action = utils.convert_1hot_action(actions["chaser"], self.action_space.n)
        evader_action = utils.convert_1hot_action(actions["evader"], self.action_space.n)

        self.chaser.update(chaser_action)

        if self.chaser.get_pos() == self.evader.get_pos():
            self.set_done(True)
            return self.state, self.reward, self.done, {}

        self.evader.update(evader_action)

        if self.chaser.get_pos() == self.evader.get_pos():
            self.set_done(True)
            return self.state, self.reward, self.done, {}

        self.steps += 1
        self.grid.set_util_text(f"Steps : {self.steps}")
        self.set_state()
        self.set_reward()

        if self.steps >= MAX_STEPS:
            self.set_done(True)
            return self.state, self.reward, self.done, {}

        return self.state, self.reward, self.done, {}

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

    def set_done(self, val):
        self.done["evader"] = val
        self.done["chaser"] = val
        self.done["__all__"] = val


    def reset(self):

        self.reward = {"chaser":0, "evader": 0}
        self.steps = 0
        self.set_done(False)
        self.set_state()

        if self.randomize_goal:
            self.grid.set_random_goal_spawn()
        if self.randomize_start:
            self.grid.set_random_start()

        # Reset positions
        self.evader.set_pos(self.grid.start)
        self.chaser.set_pos(self.grid.goal)

        return self.state

    def render(self, mode='human', close=False):

        if (self.screen is None):
            pygame.init()
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.display.set_caption('RL Chaser Evader Environment')
            for e in self.entities:
                e.render_setup(self.screen)
            self.evader.set_sub_text("Evader")
            self.chaser.set_sub_text("Chaser")


        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        for e in self.entities:
            e.render(self.screen, self.grid.block_width, self.grid.block_height)

        # self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)

        # time.sleep(0.1)
        pygame.display.update()
