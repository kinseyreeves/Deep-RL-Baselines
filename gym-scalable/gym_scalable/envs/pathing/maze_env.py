'''
Maze solving environment
Author : Kinsey Reeves
Goal:
    Solve the maze within a move limit

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

N_EVADERS = 1

# minimum chaser/evader angle change
DTHETA = 0.2

CHASER_SPEED = 3

EVADER_SPEED = 6
MAX_SCORE = 200

CAUGHT_DIST = 10

MAPFILE = "map.txt"



class MazeEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    
    '''

    def __init__(self, full_state = False, normalize_state = True):
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
        self.gridmap = GridMap(MAPFILE, S_WIDTH)

        self.entity = Entity(self.gridmap.start[0], self.gridmap.start[1], self.gridmap)
        print(f"Env starting entity at {self.gridmap.start[0]} {self.gridmap.start[1]}")

        self.state = self.reset()

        # observation space = [self.x, self.y, enemy.x, enemy.y]
        # self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)

        #Action conversion:
        left = np.asarray([1, 0, 0, 0])
        right = np.asarray([0,1,0,0])
        up = np.asarray([0,0,1,0])
        down = np.asarray([0,0,0,1])

        self.actions_table = {(-1, 0): left, (1, 0) : right, (0,-1) : up, (0,1) : down}

    def step(self, action):
        self.entity.update(action)

        self.steps += 1
        self.reward = 1

        self.set_state()

        if self.entity.x == self.gridmap.goal[0] and self.entity.y == self.gridmap.goal[1]:
            self.reset()
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
        self.entity.render(self.screen, self.gridmap.block_size)


        time.sleep(0.1)
        pygame.display.update()

    def convert_action(self, dir):
        return self.actions_table[dir]

    def get_astar_action(self, pos):
        path = self.gridmap.astar_path(pos[0], pos[1], self.gridmap.goal[0], self.gridmap.goal[1])[1]
        action = self.convert_action((pos[0] - path[0], pos[1] - path[1]))
        return action


def out_of_bounds(pos):
    x, y = pos
    if x < 0 or x > S_WIDTH or y < 0 or y > S_WIDTH:
        return True
    return False

class Entity:
    # Basic class for defining circle object
    def __init__(self, x, y, grid, color=(0,255,0)):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0
        self.grid = grid

    def update(self, action):
        if action[0] and self.grid.is_walkable(self.x+1, self.y):
            self.x+=1
        elif action[1] and self.grid.is_walkable(self.x-1, self.y):
            self.x-=1
        elif action[2] and self.grid.is_walkable(self.x, self.y+1):
            self.y+=1
        elif action[3] and self.grid.is_walkable(self.x, self.y-1):
            self.y-=1

    def render(self, screen, block_size):
        pygame.draw.circle(screen, self.color, (round(self.x*block_size+(block_size/2)), round(self.y*block_size+(block_size/2))), 10)
        # TODO draw vector in direction of entity
        # pygame.draw.line(screen, (255,90,0), )


    def move_towards(self, x, y):
        ...

    def get_entity_info(self):
        #Return the location, angle and other info
        ...


# class Evader(Entity):
#     # evader class, moves away from the chaser
#     def __init__(self, x, y):
#         color = (255, 0, 0)
#         super().__init__(x, y, color)
#
#     def update(self, action):
#
#         if (action):
#             self.angle += DTHETA
#         else:
#             self.angle -= DTHETA
#         dx = math.cos(self.angle) * EVADER_SPEED
#         dy = math.sin(self.angle) * EVADER_SPEED
#
#         self.x += dx
#         self.y += dy
#         self.angle = utils.clamp_angle(self.angle)
#
#     def is_caught(self, chaser_pos):
#         c_x, c_y = chaser_pos
#         dist = math.hypot(c_x - self.x, c_y - self.y)
#         if dist < CAUGHT_DIST:
#             return True
#         return False
#
#
# class Chaser(Entity):
#     '''
#     Chaser class, moves towards the evader
#     TODO replace with trained chaser
#     '''
#
#     def __init__(self, x, y):
#         color = (0, 255, 0)
#         super().__init__(x, y, color)
#
#     def update(self, ev_pos):
#         # clockwise
#
#         ev_x, ev_y = ev_pos
#
#         x_diff = ev_x - self.x
#         y_diff = ev_y - self.y
#
#         self.angle = math.atan2(y_diff, x_diff)
#         # print("evader angle " , self.angle)
#         dx = math.cos(self.angle) * CHASER_SPEED
#         dy = math.sin(self.angle) * CHASER_SPEED
#
#         self.x += dx
#         self.y += dy




