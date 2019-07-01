'''
Simple environment as 1st prototype
Author : kinsey reeves
Goal:
    N-Jointed arm touches each point with its tip, 
    points awarded for:
        - Reaching the point
        - Inverse time taken to reach the point
'''


import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pyglet
import pygame
import math

S_WIDTH = 640
S_HEIGHT = 480



class SimpleEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.screen = None
        self.arm = Arm(S_WIDTH/2,S_HEIGHT/2,30,50)

    def step(self, action):
        ...


    def reset(self):
        ...
    def render(self, mode='human', close=False):

        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
            self.screen.fill((255,255,255))
            pygame.init()
        
        self.screen.fill((255,255,255))

        #pygame.draw.rect(self.screen,(0, 0, 128), (50, 50, 16, 16))

        self.arm.moveRads(.017)
        self.arm.render(self.screen)
        pygame.display.update()


    


class Arm:
    def __init__(self, x, y, angle, length):
        self.x = x
        self.y = y
        self.length = length
        self.origin = (x,y)
        self.angle = angle
        self.endX = math.cos(self.angle)*length + x
        self.endY = math.sin(self.angle)*length + y
        self.end = (self.endX, self.endY)

    def render(self,screen):
        print(self.origin)
        print(self.end)
        pygame.draw.line(screen,(255,0,0),self.origin, self.end, 5)
        
    def setAngle(self,angle):
        '''
        Sets the angle of the arm and updates its endpoint
        '''
        self.angle = angle
        self.update()

    def moveRads(self,rads):
        self.angle = self.angle + rads
        self.update()

    def update(self):
        self.endX = math.cos(self.angle)*self.length + self.x
        self.endY = math.sin(self.angle)*self.length + self.y
        self.end = (self.endX, self.endY)


    def getAngle(self):
        return self.angle
        

    def setOrigin(x,y):
        self.x = x
        self.y = y

    
