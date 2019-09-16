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
import itertools

import numpy as np

# Paramaters

# Screen width/height
S_WIDTH = 400
S_HEIGHT = 300

# Arm params
ARM_ANGLE = 0
ARM_LENGTH = 60

# Number of joints excluding the middle point
extra_joints = 2

# Number of objectives, TODO able to change
N_OBJECTIVES = 1

# Whether or not the arm movements are relative. Read step()
RELATIVE = True

# Radians change per step() action, i.e. [-1,0,1] each change
# either -.1, 0 or .1 rads of the arm
ARM_RADS_CHANGE = 0.2

# Distance before goal is considered reached
DIST_THRESH = 15

# Reward for reaching objective
END_REWARD = 500

TIME_PENALTY = 200

#Maximum steps for episode
MAX_STEPS = 400

#How long must pointer be held on objective to win
HOLD_COUNT = 50

#If we're using a continuous action space
CONT_ACTIONS = True

# should the objective position stay static
STATIC = False


class NJointArm(gym.Env):
    '''
    N-Jointed Arm environment. Currently goal is to reach point destinations
        - May update to have destinations moving towards object
        - 

        Action space:
            1 dimension array with of length N_JOINTS^3
        
        Observation space:
            1 dimension array with each angle

        Reward function:

    '''

    metadata = {'render.modes': ['human']}

    action_bound = [-1, 1]

    def __init__(self, extra_joints = 2):
        self.screen = None
        self.extra_joints = extra_joints
        # If continuous action space = n, where n in range [-1,1]
        # if discrete action space initialised to [-1,0,1]*joints
        if CONT_ACTIONS:
            l_bound = np.array((extra_joints + 1) * [-1])
            h_bound = np.array((extra_joints + 1) * [1])
            self.action_space = spaces.Box(l_bound, h_bound, dtype=np.float32)
        else:
            self.action_space = spaces.Discrete(3 ** (extra_joints + 1))
        # self.observation_space = spaces.

        self.time_pen = TIME_PENALTY
        self.steps = 0
        self.done = False

        # Steps the pointer has been at the target
        self.at_objective_n = 0

        self.non_discrete_actions = self.action_one_hot()

        self.centre_x = round(S_WIDTH / 2)
        self.centre_y = round(S_HEIGHT / 2)

        # Initialise the default single arm
        self.arm = Arm(self.centre_x, S_HEIGHT / 2, ARM_ANGLE, ARM_LENGTH, None)
        self.arms = [self.arm]

        # self.max_radius = (N_JOINTS)*ARM_LENGTH

        # Intialise the extra arms
        for i in range(1, extra_joints + 1):
            prev_arm = self.arms[i - 1]
            (p_x, p_y) = prev_arm.getEnd()
            new_arm = Arm(p_x, p_y, 0, ARM_LENGTH, prev_arm)
            self.arms.append(new_arm)

        self.end_arm = self.arms[-1]

        self.reset_objective(static = True)

        # Observation space [Joint angles ... , objective1x, ob1y] #TODO update below

        l_bounds = np.array([0] + [-1] * ((extra_joints + 1) * 2) + [-1, -1])
        h_bounds = np.array([1] + [1] * ((extra_joints + 1) * 2) + [1, 1])

        self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)
        # print(self.observation_space)

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

        def undiscretise_actions(disc_actions):
            # Converts from a one hot array
            for i in range(0, len(disc_actions)):
                if disc_actions[i]:
                    return list(self.non_discrete_actions[i])

        self.time_pen -= 1
        self.steps += 1

        if not CONT_ACTIONS:
            action = undiscretise_actions(action)

        # Update each angle either pos, neg or nil
        action_arms = list(zip(action, self.arms))

        if RELATIVE:
            for action, arm in action_arms:
                arm.move_arm(action)
        else:
            for i in range(0, len(action_arms)):
                change = action_arms[i][0]
                arm = action_arms[i][1]
                if change:
                    arm.move_arm(change)
                    update_arms(action_arms[i + 1:], change)
        # check distance from goal of end arm, if less than thresh episode done
        reward = self.calc_reward()

        state = self.get_state()

        return np.array(state), reward, self.done, {}

    def calc_reward(self):
        """
        Reward is -ve abs distance
        unless pointer is on objective its dist+1
        (therefore positive)
        :return: reward
        """
        dist = self.get_dist()
        r = - dist / (S_WIDTH/2)
        if dist < DIST_THRESH and (not self.done):
            r += 1.0
            self.at_objective_n += 1
            if self.at_objective_n > HOLD_COUNT:
                r +=10
                self.done = True
        elif dist > DIST_THRESH:
            self.at_objective_n = 0
            self.done = False

        return r

    def get_state(self):
        '''
        Gets the state, [at_obj] [jointx-objx, jointy-objy]*N_JOINTS + [dist from centrex, dfcy]
        '''
        #angles = [normalize(arm.angle, 0, 2 * math.pi) for arm in self.arms]

        in_point = 1. if self.at_objective_n > 0. else 0.
        arm_coords = []
        for arm in self.arms:
            arm_coords.append(arm.endX - self.ob_x)
            arm_coords.append(arm.endY - self.ob_y)

        dist = np.asarray([self.centre_x - self.ob_x, self.centre_y - self.ob_y]) / (S_WIDTH/2)
        arm_coords = np.asarray(arm_coords) / (S_WIDTH/2)
        # minx = self.centre_x - ARM_LENGTH * (N_EXTRA_JOINTS + 1)
        # maxx = self.centre_x + ARM_LENGTH * (N_EXTRA_JOINTS + 1)
        # miny = self.centre_y - ARM_LENGTH * (N_EXTRA_JOINTS + 1)
        # maxy = self.centre_x + ARM_LENGTH * (N_EXTRA_JOINTS + 1)
        #
        # objs = [normalize(self.ob_x, minx, maxx), normalize(self.ob_y, minx, maxx)]
        #print(in_point, dist, arm_coords)
        state = np.concatenate([[in_point], dist, arm_coords])

        return state

    def reset(self):
        for arm in self.arms:
            arm.setAngle(0)
        self.time_pen = TIME_PENALTY
        self.reset_objective()
        self.done = False
        self.steps = 0
        return self.get_state()

    def render(self, mode='human', close=False):
        # If screen isnt initiated, initiate it, fill it white
        if (self.screen is None):
            self.screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
            self.screen.fill((255, 255, 255))
            pygame.init()
        self.screen.fill((255, 255, 255))

        # Draw the objective
        pygame.draw.circle(self.screen, (100, 100, 10), (self.ob_x, self.ob_y), DIST_THRESH)

        # Render joints ontop of arms
        for arm in self.arms:
            arm.render_arm(self.screen)
        for arm in self.arms:
            arm.render_joint(self.screen)

        # Draw the center circle
        pygame.draw.circle(self.screen, (0, 0, 255), (S_WIDTH // 2, S_HEIGHT // 2), 5)
        # draw the objective

        pygame.display.update()

    def reset_objective(self, static=STATIC):
        '''
        Initialises the objective
        '''
        # Intialise the objective
        if static:
            arcpos = math.pi + 0.5
        else:
            arcpos = random.uniform(0, 1) * 2 * math.pi

        # If we have more than one joint, the circle must be on the radius
        # Otherwise it can lie anywhere from 0 to the max dist
        # TODO bound to screen
        if static:
            rad = ARM_LENGTH * (self.extra_joints + 1)
            self.ob_x = self.centre_x + round(rad * math.cos(arcpos))
            self.ob_y = self.centre_y + round(rad * math.sin(arcpos))
        elif self.extra_joints > 0:
            rad = ARM_LENGTH * (self.extra_joints + 1) * random.uniform(0, 1)
            self.ob_x = self.centre_x + round(rad * math.cos(arcpos))
            self.ob_y = self.centre_y + round(rad * math.sin(arcpos))
        else:
            self.ob_x = self.centre_x + round(ARM_LENGTH * math.cos(arcpos))
            self.ob_y = self.centre_y + round(ARM_LENGTH * math.sin(arcpos))

        if self.ob_x > S_WIDTH:
            self.ob_x = S_WIDTH-10
        if self.ob_y > S_HEIGHT:
            self.ob_y= S_HEIGHT - 10
        if self.ob_x < 0:
            self.ob_x = 10
        if self.ob_y < 0:
            self.ob_y = 10


    def get_dist(self):
        '''
        Gets the distance of the end arm point to
        the objective
        :return:
        '''
        dist = math.hypot(self.end_arm.endX - self.ob_x,
                          self.end_arm.endY - self.ob_y)
        return dist


    def action_one_hot(self):
        out = []
        perms = [[-1, 0, 1] for _ in range(self.extra_joints + 1)]
        for element in itertools.product(*perms):
            out.append(element)

        return out


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
        self.origin = (x, y)
        # Angle in rads
        self.angle = angle
        self.endX = math.cos(self.angle) * length + x
        self.endY = math.sin(self.angle) * length + y
        self.end = (self.endX, self.endY)

        self.prev_arm = prev_arm

    def render_arm(self, screen):
        '''
        Renders the arm.
        TODO update to a rectangle to avoid weird width
        '''

        pygame.draw.line(screen, (255, 0, 0), self.origin, self.end, 5)

    def render_joint(self, screen):
        '''
        Renders the joint at the end of the arm
        '''
        end = (round(self.end[0]), round(self.end[1]))
        pygame.draw.circle(screen, (0, 255, 0), end, 5)

    def setAngle(self, angle):
        '''
        Sets the angle of the arm and updates its endpoint
        '''
        self.angle = angle
        self.update()

    def moveRads(self, rads):
        '''
        Movess the arm by rads radians
        '''
        self.angle = self.angle + rads
        self.update()

    def move_arm(self, dir):
        '''
        Moves the arm by defined angle in params
        '''
        dtheta = dir * ARM_RADS_CHANGE

        self.angle += dtheta
        self.angle %= math.pi*2
        self.update()

    def update(self):

        if self.prev_arm:
            self.origin = self.prev_arm.end
            self.x = self.prev_arm.endX
            self.y = self.prev_arm.endY

        self.endX = math.cos(self.angle) * self.length + self.x
        self.endY = math.sin(self.angle) * self.length + self.y
        self.end = (self.endX, self.endY)

    def getAngle(self):
        return self.angle

    def setOrigin(self, x, y):
        self.x = x
        self.y = y

    def getOrigin(self):
        return (self.x, self.y)

    def getEnd(self):
        return self.end


def normalize(x, minx, maxx):
    return (x - minx) / (maxx - minx)
