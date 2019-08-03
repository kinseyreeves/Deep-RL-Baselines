import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random
import time
from gym_scalable.envs import utils
import numpy as np

# NOTE THIS MUST BE SQUARE, AND MULTIPLE OF 10
S_WIDTH = 400

B_LEN = 10

EW_ROADS = 4
NS_ROADS = 4
ROAD_WIDTH = 10


class TrafficEnv(gym.Env):
    """
    Basic single chaser single evader environment
    Env agent controls the evader, which moves at a fixed speed
    with action 1 | 0, to change the angle.

    Chaser always moves towards the evader.
    """

    def __init__(self):
        self.screen = None
        # East west offsets or north south
        offset_ew = S_WIDTH / (EW_ROADS + 1)
        offset_ns = S_WIDTH / (NS_ROADS + 1)

        self.ew_roads = []
        self.ns_roads = []

        for i in range(0, EW_ROADS):
            # print(offset_ew)
            YPos = i * offset_ew + offset_ew
            # print(YPos)
            r = Road((0, YPos), (S_WIDTH, YPos), False)
            self.ew_roads.append(r)

        for i in range(0, NS_ROADS):
            xPos = i * offset_ns + offset_ns
            r = Road((xPos, 0), (xPos, S_WIDTH), True)

            self.ns_roads.append(r)

        # observation space = [self.x, self.y, enemy.x, enemy.y]
        # self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)

    def step(self, action):
        ...

    def set_state(self):
        ...

    def reset(self):
        ...

    def render(self):
        if self.screen is None:
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.init()
        self.screen.fill((255, 255, 255))
        for r in self.ew_roads:
            r.render(self.screen)
        for r in self.ns_roads:
            r.render(self.screen)
        pygame.display.update()


class Car:
    def __init__(self, track, position):
        self.track = track
        self.position = position

    def render(self, screen):

        ...

    def update(self):
        self.position += 1
        self.track[self.position] = self
        self.track[self.position-1] = None


class Intersection:
    def __init__(self, road1, road2):
        ...







class Road:
    """
    Road class

    No road really starts and ends, just for simplicity
    """

    def __init__(self, start_pos, end_pos, ns_road):
        self.start_pos = start_pos
        self.end_pos = end_pos
        # If its a north/south road or not
        self.all_cars = []
        num_blocks = int(S_WIDTH / ROAD_WIDTH)
        self.forward_cars = [None for x in range(0, num_blocks)]
        self.reverse_cars = [None for x in range(0, num_blocks)]

        print(self.forward_cars)
        c = self.ad
        d_car(True)
        print(self.forward_cars)
        c.update()
        print(self.forward_cars)
        c.update()
        print(self.forward_cars)

        if ns_road:
            self.forward_lane_rect = pygame.Rect(self.start_pos, (ROAD_WIDTH, S_WIDTH))
            start_pos2 = (self.start_pos[0] - ROAD_WIDTH, self.start_pos[1])
            self.rev_lane_rect = pygame.Rect(start_pos2, (ROAD_WIDTH, S_WIDTH))
        else:
            self.forward_lane_rect = pygame.Rect(self.start_pos, (S_WIDTH, ROAD_WIDTH))
            start_pos2 = (self.start_pos[0], self.start_pos[1] - ROAD_WIDTH)
            self.rev_lane_rect = pygame.Rect(start_pos2, (S_WIDTH, ROAD_WIDTH))

        # Track made up of 2 tuples
        print(self.start_pos)

        self.cars = []

    def update(self):
        """
        updates both lanes of the road

        """
        for car in self.all_cars:
            car.update()

    def add_car(self, forward):
        if forward:
            car = Car(self.forward_cars, 0)
            self.forward_cars[0] = car
        else:
            car = Car(self.reverse_cars, 0)
            self.reverse_cars[0] = car
        return car

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.forward_lane_rect)
        pygame.draw.rect(screen, (40, 40, 40), self.rev_lane_rect)
