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
S_WIDTH = 200


EW_ROADS = 2
NS_ROADS = 2
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

        self.ns_roads[0].generate_car(True)
        self.ns_roads[0].generate_car(False)

        #TODO remove duplicate
        #Work out intersection positions
        for road1 in self.ns_roads:
            for road2 in self.ew_roads:
                duplicates = {}
                for seg in road1.forward_lane + road1.reverse_lane + road2.forward_lane + road2.reverse_lane:
                    if seg.get_pos() in duplicates:
                        duplicates[seg.get_pos()] = duplicates[seg.get_pos()] + [seg]
                    else:
                        duplicates[seg.get_pos()] = [seg]
                for i in duplicates:
                    if(len(duplicates[i])>1):
                        print(duplicates[i])
                        #TODO add intersection here


        # self.ew_roads[0].generate_car(True)
        # self.ew_roads[0].generate_car(False)


        # observation space = [self.x, self.y, enemy.x, enemy.y]
        # self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)

    def step(self, action):

        # TODO apply action to intersection before road update
        for road in self.ns_roads:
            road.update()
        for road in self.ew_roads:
            road.update()



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
        for r in self.ew_roads + self.ns_roads:
            r.render(self.screen)

        for r in self.ew_roads + self.ns_roads:
            for car in r.get_all_cars():
                car.render(self.screen)

        pygame.display.update()


class Car:
    def __init__(self, track, index, pos, offset):
        self.track = track
        self.index = index
        self.pos = pos
        self.offset = offset

    def render(self, screen):
        # pygame.draw.rect(screen, (0,0,255), (self.pos[0], self.pos[1], 5, 5))
        pos = self.track[self.index].get_pos()

        pygame.draw.rect(screen, (0,0,255), (pos[0], pos[1], 5, 5))

    def update(self):

        if self.track[self.index + 1].is_drivable():
            self.track[self.index].remove_car()
            self.index += 1
            self.track[self.index].add_car(self)

        #self.pos = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])

class RoadSegment:

    def __init__(self, position):
        self.car = None
        self.position = (int(position[0]), int(position[1]))
        self.rect = (self.position, (ROAD_WIDTH, ROAD_WIDTH))

    def is_drivable(self):
        if self.car:
            return False
        return True

    def add_car(self, car):
        if not self.car:
            self.car = car

    def remove_car(self):
        self.car = None

    def get_pos(self):
        return self.position

    def render(self, screen):
        pygame.draw.rect(screen, (random.randrange(0,255),0,0), self.rect)




class IntersectionSegment(RoadSegment):
    def __init__(self):
        super().__init__()
        self.green = True

    def is_drivable(self):
        if self.car:
            return True
        return False

    def add_car(self, car):
        self.car = car

    def remove_car(self):
        self.car = None


class Intersection:
    def __init__(self, seg1, seg2, seg3, seg4):
        ...


class Road:
    """
    Road class

    Handles car generation and has 2 lists for each lane.
    """

    def __init__(self, start_pos, end_pos, ns_road):
        self.start_pos = start_pos
        self.end_pos = end_pos
        # If its a north/south road or not
        self.ns_road = ns_road
        self.all_cars = []
        num_blocks = int(S_WIDTH / ROAD_WIDTH)


        # Adds the rectangles for each lane
        if ns_road:
            self.forward_lane = [RoadSegment((self.start_pos[0], ROAD_WIDTH*x)) for x in range(0, num_blocks)]
            self.reverse_lane = [RoadSegment((self.start_pos[0]-ROAD_WIDTH, self.end_pos[1] - ROAD_WIDTH*x)) for x in range(1, num_blocks+1)]

            self.forward_lane_rect = pygame.Rect(self.start_pos, (ROAD_WIDTH, S_WIDTH))
            start_pos2 = (self.start_pos[0] - ROAD_WIDTH, self.start_pos[1])
            #self.rev_lane_rect = pygame.Rect(start_pos2, (ROAD_WIDTH, S_WIDTH))
        else:
            self.forward_lane = [RoadSegment((ROAD_WIDTH*x, self.start_pos[1]-ROAD_WIDTH)) for x in range(0, num_blocks)]
            self.reverse_lane = [RoadSegment((self.end_pos[0] - ROAD_WIDTH*x, self.start_pos[1])) for x in range(1, num_blocks+1)]

            #self.forward_lane_rect = pygame.Rect(self.start_pos, (S_WIDTH, ROAD_WIDTH))
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

    def generate_car(self, forward):
        """
        Generates a car and adds it to the road
        :param forward: Add it to the forward lane, otherwise reverse
        :return: the car
        """

        # setup offsets and car starting positions depending on orientation of road
        if self.ns_road:
            offset_for = (0, ROAD_WIDTH)
            offset_rev = (0, -ROAD_WIDTH)
            end_pos = (self.end_pos[0] - ROAD_WIDTH, self.end_pos[1])
            start_pos = self.start_pos
        else:
            offset_for = (ROAD_WIDTH, 0)
            offset_rev = (-ROAD_WIDTH, 0)
            end_pos = (self.end_pos[0], self.end_pos[1])
            start_pos = (self.start_pos[0], self.start_pos[1] - ROAD_WIDTH)
        if forward:
            car = Car(self.forward_lane, 0, start_pos, offset_for)
            self.forward_lane[0].add_car(car)
        else:
            car = Car(self.reverse_lane, 0, end_pos, offset_rev)
            self.reverse_lane[0].add_car(car)

        self.all_cars.append(car)
        return car

    def render(self, screen):
        #pygame.draw.rect(screen, (0, 0, 0), self.forward_lane_rect)
        #pygame.draw.rect(screen, (40, 40, 40), self.rev_lane_rect)
        for l in self.forward_lane:
            l.render(screen)
        for j in self.reverse_lane:
            j.render(screen)

    def get_all_cars(self):
        return self.all_cars
