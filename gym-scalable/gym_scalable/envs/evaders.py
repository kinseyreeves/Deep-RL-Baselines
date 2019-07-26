import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random
import time

import numpy as np

S_WIDTH = 500
S_HEIGHT = 480

N_EVADERS = 1

#minimum chaser/evader angle change
DTHETA = 0.1

MOVE_MAG = 2


class EvadersEnv(gym.Env):
    
    metadata = {'render.modes': ['human']}


    def __init__(self):
        self.screen = None
        #Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.Discrete(1)
        self.observation_space = None
        
        self.centre_x = round(S_WIDTH/2)
        self.centre_y = round(S_HEIGHT/2)

        self.evader = Evader(self.centre_x, self.centre_y)
        #self.chaser = Chaser(random.randrange(0,S_WIDTH), random.randrange(0,S_WIDTH))

        #observation space = [self.x, self.y, enemy.x, enemy.y]
        #self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        self.evader.update(action)
        #chaser.update()


        ...
        #return np.array(state), reward, done, {}



    def reset(self):
        ...


    def render(self, mode='human', close=False):

        #If screen isnt initiated, initiate it, fill it white
        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
            self.screen.fill((255,255,255))
            pygame.init()
        self.screen.fill((255,255,255))

        self.evader.render(self.screen)
        time.sleep(0.1)
        pygame.display.update()


    def reset_objective(self):
        '''
        Initialises the objective
        '''
        ...

class Entity:
    def __init__(self, x, y,color):

        self.x = x
        self.y = y
        self.color = color
        self.angle = 0
    
    def render(self, screen):
        pygame.draw.circle(screen,self.color,(round(self.x), round(self.y)),20)
        #TODO draw vector in direction of entity
        #pygame.draw.line(screen, (255,90,0), )

    


class Evader(Entity):

    def __init__(self, x, y):
        color = (255,0,0)
        super().__init__(x,y,color)
    

    def update(self,action):
        #clockwise
        print(self.angle)
        if(action):
            self.angle += DTHETA
        else:
            self.angle -= DTHETA
        dx = math.cos(self.angle)*MOVE_MAG
        dy = math.sin(self.angle)*MOVE_MAG

        self.x += dx
        self.y += dy
        
    
    def move_towards(self,x,y):
        ...




