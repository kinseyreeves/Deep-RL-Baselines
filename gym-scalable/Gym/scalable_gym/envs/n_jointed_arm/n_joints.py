'''
N-Jointed arm environment
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

#Screen width/height
S_WIDTH = 400
S_HEIGHT = 300

#Arm params
ARM_ANGLE = 0
ARM_LENGTH = 40

N_JOINTS = 5

#Number of objectives, TODO able to change
N_OBJECTIVES = 1

#Whether or not the arm movements are relative. Read step()
RELATIVE = False

#Radians change per step() action, i.e. [-1,0,1] each change
#either -.1, 0 or .1 rads of the arm
ARM_RADS_CHANGE = 0.1

#Distance before goal is considered reached
DIST_THRESH = 80

#Reward for reaching objective
END_REWARD = 500



class NJointArm(gym.Env):
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
        
        self.centre_x = round(S_WIDTH/2)
        self.centre_y = round(S_HEIGHT/2)

        #Initialise the default single arm
        self.arm = Arm(self.centre_x,S_HEIGHT/2,ARM_ANGLE,ARM_LENGTH, None)
        self.arms = [self.arm]

        #self.max_radius = (N_JOINTS)*ARM_LENGTH

        #Intialise the extra arms
        for i in range(1,N_JOINTS+1):
            prev_arm = self.arms[i-1]
            (p_x, p_y) = prev_arm.getEnd()
            new_arm = Arm(p_x, p_y, random.uniform(0,2*3.14), ARM_LENGTH, prev_arm)
            self.arms.append(new_arm)

        self.end_arm = self.arms[-1]

        self.reset_objective()

        #Observation space [Joint angles ... , objective1x, ob1y]
        l_bounds = np.array([0]*(N_JOINTS+1) + [0] * (N_OBJECTIVES*2))
        h_bounds = np.array([2*math.pi]*(N_JOINTS+1)+[S_WIDTH,S_HEIGHT]*N_OBJECTIVES)
        
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)


    def step(self, action):
        '''
        Arms relative angle change or global angle change?
        if RELATIVE is set, an arms global angle will be 
        additive of the previous arms. e.g. the first arms
        angle will affect the global angle of all following
        arms. If RELATIVE is False, a former arm will not
        result in latter arms global angles being changed
        '''
        def update_arms(zip_changes, dtheta):
            for _, arm in zip_changes:
                arm.move_arm(dtheta)

        done = False

        reward = 0
        #Testing
        action = [1]*(N_JOINTS+1)


        #Update each angle either pos, neg or nil
        action_arms = list(zip(action,self.arms))

        if(RELATIVE):
            for action, arm in action_arms:
                arm.move_arm(action)
        else:
            for i in range(0,len(action_arms)):
                change = action_arms[i][0]
                arm = action_arms[i][1]
                if(change):
                    arm.move_arm(change)
                    update_arms(action_arms[i+1:], change)

        #check distance from goal of end arm, if less than thresh episode done
        if(math.hypot(self.end_arm.endX-self.ob_x,
             self.end_arm.endY - self.ob_y) < DIST_THRESH):

             done=True
             reward += END_REWARD
        
        #Reward 

        state = [arm.angle for arm in self.arms] + [self.ob_x, self.ob_y]
        
        return np.array(state), reward, done, {}



    def reset(self):
        for arm in self.arms:
            arm.setAngle(random.uniform(0,2*3.14))

        self.reset_objective()


    def render(self, mode='human', close=False):

        #If screen isnt initiated, initiate it, fill it white
        if(self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
            self.screen.fill((255,255,255))
            pygame.init()
        self.screen.fill((255,255,255))

        #Render joints ontop of arms
        for arm in self.arms:
            arm.render_arm(self.screen)
        for arm in self.arms:
            arm.render_joint(self.screen)

        #Draw the center circle
        pygame.draw.circle(self.screen,(0,0,255),(S_WIDTH//2, S_HEIGHT//2),5)
        
        #draw the objective
        pygame.draw.circle(self.screen,(70,30,255), (self.ob_x, self.ob_y), 10)
        pygame.display.update()


    def reset_objective(self):
        '''
        Initialises the objective
        '''
        #Intialise the objective
        arcpos = random.uniform(0,1)*2*math.pi
        #If we have more than one joint, the circle must be on the radius
        #Otherwise it can lie anywhere from 0 to the max dist
        #TODO bound to screen
        if(N_JOINTS > 0):
            rad = ARM_LENGTH*N_JOINTS*random.uniform(0,1)
            self.ob_x = self.centre_x + round(rad*math.cos(arcpos))
            self.ob_y = self.centre_y + round(rad*math.sin(arcpos))
        else:
            self.ob_x = self.centre_x +round(ARM_LENGTH*math.cos(arcpos))
            self.ob_y = self.centre_y +round(ARM_LENGTH*math.sin(arcpos))


class Arm:
    '''
    Basic class for an arm defined by:
        x,y start position
        angle in rads
        length of the arm
        the preceeding arm
    '''
    def __init__(self, x, y, angle, length, prev_arm):
        self.x = x
        self.y = y
        self.length = length
        self.origin = (x,y)
        #Angle in rads
        self.angle = angle
        self.endX = math.cos(self.angle)*length + x
        self.endY = math.sin(self.angle)*length + y
        self.end = (self.endX, self.endY)

        self.prev_arm = prev_arm

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


    def move_arm(self,dir):
        '''
        Moves the arm by defined angle in params

        '''
        dtheta = dir*ARM_RADS_CHANGE
        self.angle+=dtheta
        self.update()

    def update(self):
        
        if(self.prev_arm):
            self.origin = self.prev_arm.end
            self.x = self.prev_arm.endX
            self.y = self.prev_arm.endY

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
        

    
