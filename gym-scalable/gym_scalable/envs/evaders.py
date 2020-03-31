'''
Evader environment
Author : Kinsey Reeves
Goal:
    Evade the chaser as long as possible
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

S_WIDTH = 200   
S_HEIGHT = 200

N_EVADERS = 1

#minimum chaser/evader angle change
DTHETA = 0.2

CHASER_SPEED = 3

EVADER_SPEED = 6
MAX_SCORE = 200

CAUGHT_DIST = 10


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

        #TODO should we normalize or use int vals?
        high = np.array([1, 1, 1, 1, 1])
        low = np.array([0,0,0,0,0])

        self.observation_space = spaces.Box(low = low, high = high, dtype = np.float32)
        
        self.centre_x = round(S_WIDTH/2)
        self.centre_y = round(S_HEIGHT/2)
        self.steps = 0
        self.reward = 0
        self.done = False
        self.evader = Evader(self.centre_x, self.centre_y)
        self.chaser = Chaser(random.randrange(0,S_WIDTH), random.randrange(0,S_WIDTH))

        self.state = self.reset()
        
        #observation space = [self.x, self.y, enemy.x, enemy.y]
        #self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        self.evader.update(action)
        self.chaser.update((self.evader.x, self.evader.y))
        
        self.steps += 1
        self.reward = 1

        self.set_state()

        if out_of_bounds((self.evader.x, self.evader.y)) or \
                self.evader.is_caught((self.chaser.x, self.chaser.y)):
            
            #self.reward = -100 + self.reward
            self.done = True
            return np.array(self.state), self.reward, self.done, {}
        
        if(self.steps >= MAX_SCORE):
            
            self.done = True
            return np.array(self.state), self.reward, self.done, {}
        
        return np.array(self.state), self.reward, self.done, {}

    def set_state(self):

        self.state = [utils.normalize(self.evader.angle,0,2*math.pi), 
                        utils.normalize(self.evader.x, 0, S_WIDTH),
                        utils.normalize(self.evader.y, 0, S_HEIGHT),
                        utils.normalize(self.chaser.x, 0, S_WIDTH),
                        utils.normalize(self.chaser.y, 0, S_HEIGHT)]
    
    def reset(self):
        
        self.reward = 0
        self.steps = 0
        self.done = False
        self.evader = Evader(self.centre_x, self.centre_y)
        self.chaser = Chaser(random.randrange(0,S_WIDTH), random.randrange(0,S_WIDTH))

        self.set_state()

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
    #Basic class for defining circle object
    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.angle = 0
    
    def render(self, screen):
        pygame.draw.circle(screen,self.color,(round(self.x), round(self.y)),20)
        #TODO draw vector in direction of entity
        #pygame.draw.line(screen, (255,90,0), )


class Evader(Entity):
    #evader class, moves away from the chaser
    def __init__(self, x, y):
        color = (255,0,0)
        super().__init__(x, y, color)
    
    def update(self,action):

        if action:
            self.angle += DTHETA
        else:
            self.angle -= DTHETA
        dx = math.cos(self.angle)*EVADER_SPEED
        dy = math.sin(self.angle)*EVADER_SPEED

        self.x += dx
        self.y += dy
        self.angle = utils.clamp_angle(self.angle)

    def is_caught(self, chaser_pos):
        c_x, c_y = chaser_pos
        dist = math.hypot(c_x - self.x, c_y - self.y)
        if dist < CAUGHT_DIST:
            return True
        return False
        
    
class Chaser(Entity):
    '''
    Chaser class, moves towards the evader
    TODO replace with trained chaser
    '''
    def __init__(self, x, y):
        color = (0,255,0)
        super().__init__(x,y,color)
    

    def update(self, ev_pos):
        #clockwise
        
        ev_x, ev_y = ev_pos

        x_diff = ev_x - self.x
        y_diff = ev_y - self.y

        self.angle = math.atan2(y_diff,x_diff)
        #print("evader angle " , self.angle)
        dx = math.cos(self.angle)*CHASER_SPEED
        dy = math.sin(self.angle)*CHASER_SPEED

        self.x += dx
        self.y += dy

