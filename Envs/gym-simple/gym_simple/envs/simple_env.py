'''
Simple environment as 1st prototype
Author : Kinsey Reeves
Goal:
    N-Jointed arm touches each point with its tip, 
    points awarded for:
        - Reaching the point
        - Inverse time taken to reach the point
'''

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import math
import random

import numpy as np

#Paramaters

S_WIDTH = 640
S_HEIGHT = 480

ARM_ANGLE = 30
ARM_LENGTH = 50

N_JOINTS = 5

N_OBJECTIVES = 1



class SimpleEnv(gym.Env):
    '''
    N-Jointed Arm environment. Currently goal is to reach point destinations
        - May update to have destinations moving towards object
        - 

        Action space:
            1 dimension array with of length N_JOINTS
        
        Observation space:
            1 dimension array with each angle 
    '''
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.screen = None
        #Action space initialised to [-1,0,1] for each joint
        self.action_space = spaces.MultiDiscrete((N_JOINTS+1)*[3])
        #self.observation_space = spaces.
        
        print(self.action_space)
        #Initialise the default single arm
        self.arm = Arm(S_WIDTH/2,S_HEIGHT/2,ARM_ANGLE,ARM_LENGTH)
        self.arms = [self.arm]

        self.max_radius = (N_JOINTS)*ARM_LENGTH

        
        #Intialise the extra arms
        for i in range(1,N_JOINTS+1):
            prev_arm = self.arms[i-1]
            (p_x, p_y) = prev_arm.getEnd()
            new_arm = Arm(p_x, p_y, random.uniform(0,3.14), 50)
            self.arms.append(new_arm)

        #Observation space [Joint angles ... , objective1x, ob1y]
        l_bounds = np.array([0]*(N_JOINTS+1) + [0] * (N_OBJECTIVES*2))
        h_bounds = np.array([2*math.pi]*(N_JOINTS+1)+[S_WIDTH,S_HEIGHT]*N_OBJECTIVES)
        

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        '''
        TODO:
            should we represent arm actions as angles 
            or movements from the current angle?

        '''
        ...


    def reset(self):
        ...
    def render(self, mode='human', close=False):

        #If screen isnt initiated, initiate it, fill it white
        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
            self.screen.fill((255,255,255))
            pygame.init()
        self.screen.fill((255,255,255))




        for arm in self.arms:
            arm.render_arm(self.screen)
        for arm in self.arms:
            arm.render_joint(self.screen)

        #Draw the center circle
        pygame.draw.circle(self.screen,(0,0,255),(S_WIDTH//2, S_HEIGHT//2),5)


        pygame.display.update()



class Arm:
    '''
    Basic class for an arm defined by the start x,y, angle in rads and
    length of the arm
    '''
    def __init__(self, x, y, angle, length):
        self.x = x
        self.y = y
        self.length = length
        self.origin = (x,y)
        self.angle = angle
        self.endX = math.cos(self.angle)*length + x
        self.endY = math.sin(self.angle)*length + y
        self.end = (self.endX, self.endY)

    def render_arm(self,screen):
        '''
        Renders the arm.
        TODO update to a rectangle to avoid weird width
        '''
        
        pygame.draw.line(screen,(255,0,0),self.origin, self.end, 5)
        
    
    def render_joint(self,screen):
        '''
        Renders the joint at the end of the arm
        '''
        end = (round(self.end[0]), round(self.end[1]))
        pygame.draw.circle(screen,(0,255,0),end,5)
 
    def setAngle(self,angle):
        '''
        Sets the angle of the arm and updates its endpoint
        '''
        self.angle = angle
        self.update()

    def moveRads(self,rads):
        '''
        Movess the arm by rads radians
        ''' 
        self.angle = self.angle + rads
        self.update()

    def update(self):
        self.endX = math.cos(self.angle)*self.length + self.x
        self.endY = math.sin(self.angle)*self.length + self.y
        self.end = (self.endX, self.endY)


    def getAngle(self):
        return self.angle
        
    def setOrigin(self,x,y):
        self.x = x
        self.y = y

    def getOrigin(self):
        return (self.x,self.y)

    def getEnd(self):
        return self.end
        

    
