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
DTHETA = 0.2

CHASER_SPEED = 1.5

EVADER_SPEED = 4
MAX_SCORE = 100

CAUGHT_DIST = 100


class EvadersEnv(gym.Env):
    
    metadata = {'render.modes': ['human']}

    '''
    Basic single chaser single evader environment
    Env agent controls the evader, which moves at a fixed speed
    with action 1 | 0, to change the angle.
    
    Chaser always moves towards the evader.
    '''

    def __init__(self):
        self.screen = None
        #Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.Discrete(2)
        self.observation_space = None
        
        self.centre_x = round(S_WIDTH/2)
        self.centre_y = round(S_HEIGHT/2)
        self.steps = 0
        self.reward = 0
    
        self.evader = Evader(self.centre_x, self.centre_y)
        self.chaser = Chaser(random.randrange(0,S_WIDTH), random.randrange(0,S_WIDTH))

        self.observation, self.reward, self.done, _ = self.reset()
        
        #observation space = [self.x, self.y, enemy.x, enemy.y]
        #self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        self.evader.update(action)
        self.chaser.update((self.evader.x, self.evader.y))
        
        self.steps += 1
        self.reward +=1

        self.state = [self.evader.x, self.evader.y, self.chaser.x, self.chaser.y]

        if out_of_bounds((self.evader.x, self.evader.y)) or \
                self.evader.is_caught((self.evader.x, self.evader.y)):
            self.reward = -100
            self.done = True
            return np.array(self.state), self.reward, self.done, {}
        
        if(self.reward >= MAX_SCORE):
            self.done = True
            return np.array(state), self.reward, self.done, {}
        
        return np.array(self.state), self.reward, self.done, {}


    def reset(self):
        self.state = [self.evader.x, self.evader.y, self.chaser.x, self.evader.y]
        self.reward = 0
        self.steps = 0
        self.done = False

        return np.array(self.state)


    def render(self, mode='human', close=False):

        #If screen isnt initiated, initiate it, fill it white
        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
            self.screen.fill((255,255,255))
            pygame.init()
        self.screen.fill((255,255,255))

        self.evader.render(self.screen)
        self.chaser.render(self.screen)
        time.sleep(0.1)
        pygame.display.update()


    def reset_objective(self):
        '''
        Initialises the objective
        '''
        ...

def out_of_bounds(pos):
    x,y = pos
    if x < 0 or x > S_WIDTH or y < 0 or y > S_HEIGHT:
        return True
    return False

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
        dx = math.cos(self.angle)*EVADER_SPEED
        dy = math.sin(self.angle)*EVADER_SPEED

        self.x += dx
        self.y += dy

    def is_caught(self,chaser_pos):
        c_x, c_y = chaser_pos
        dist = math.hypot(c_x - self.x, c_y - self.y)
        if dist < CAUGHT_DIST:
            return True
        return False
        
    
class Chaser(Entity):
    def __init__(self, x, y):
        color = (0,255,0)
        super().__init__(x,y,color)
    

    def update(self, ev_pos):
        #clockwise
        
        ev_x, ev_y = ev_pos

        x_diff = ev_x - self.x


        y_diff = ev_y - self.y

        self.angle = math.atan2(y_diff,x_diff)
        print("evader angle " , self.angle)
        dx = math.cos(self.angle)*CHASER_SPEED
        dy = math.sin(self.angle)*CHASER_SPEED

        self.x += dx
        self.y += dy

    




