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

# ----------------------------------------------------#####

# Screen width/height
S_WIDTH = 400
S_HEIGHT = 400

# --------------------ARM PARAMS-----------------------####
ARM_ANGLE = 0
ARM_LENGTH = 50

# Radians change per step() action, i.e. [-1,0,1] each change
# either -.1, 0 or .1 rads of the arm
ARM_RADS_CHANGE = 0.1

# Whether or not the arm movements are relative. Read step()
RELATIVE = False

RESET_ARM_ANGS = True

# -------------------ENV PARAMS----------------------######

# Number of objectives, TODO able to change
N_OBJECTIVES = 1

# Number of obstacles, set to 0 for jacobian or no obs
N_OBSTACLES = 0

# Distance before goal is considered reached
DIST_THRESH = 10

# Reward for reaching objective
END_REWARD = 10

TIME_PENALTY = 200

# Maximum steps for episode
MAX_STEPS = 400

# How long must pointer be held on objective to win
HOLD_COUNT = 50

# If we're using a continuous action space
CONT_ACTIONS = True

# should the objective position stay static
STATIC = False

USE_MOUSE = True


class NJointArm(gym.Env):
    '''
    N-Jointed Arm environment. Currently goal is to reach point destinations
        - May update to have destinations moving towards object

        Action space:
            1 dimension array with of length N_JOINTS^3

        Observation space:
            1 dimension array with each angle
        Reward function:

    '''

    metadata = {'render.modes': ['human']}

    action_bound = [-1, 1]

    def __init__(self, config):
        """

        :param extra_joints: Specify how many extra joints
        :param extra_state: Adds extra info into the state space such as
            precise positions
        """
        self.extra_joints = config["extra_joints"] if "extra_joints" in config else 1
        self.extra_state = config["extra_state"] if "extra_state" in config else False
        
        print(f"N-jointed arm started with {self.extra_joints+1} joints")
        self.screen = None

        self.obstacles = []
        # If continuous action space = n, where n in range [-1,1]
        # if discrete action space initialised to [-1,0,1]*joints
        if CONT_ACTIONS:
            l_bound = np.array((self.extra_joints + 1) * [-1])
            h_bound = np.array((self.extra_joints + 1) * [1])
            self.action_space = spaces.Box(l_bound, h_bound, dtype=np.float32)
        else:
            self.action_space = spaces.Discrete(3 ** (self.extra_joints + 1))
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


        # Intialise the extra arms
        for i in range(1, self.extra_joints + 1):
            prev_arm = self.arms[i - 1]
            (p_x, p_y) = prev_arm.getEnd()
            new_arm = Arm(p_x, p_y, 0, ARM_LENGTH, prev_arm)
            self.arms.append(new_arm)
        #print(self.arms)
        self.normalize_len = (self.extra_joints+1) * (ARM_LENGTH)*2

        self.end_arm = self.arms[-1]

        self.reset_objective(static=True)

        # Observation space [Joint angles ... , objective1x, ob1y] #TODO update below

        l_bounds = np.array([0] + [-1] * ((self.extra_joints + 1) * 2) + [-1, -1])
        h_bounds = np.array([1] + [1] * ((self.extra_joints + 1) * 2) + [1, 1])

        self.observation_space = spaces.Box(l_bounds, h_bounds, dtype=np.float32)

        # setup objectives
        if (N_OBJECTIVES > 0):
            for i in range(0, N_OBJECTIVES):
                self.spawn_obstacle()

        # print(self.observation_space)

    def step(self, action, normalize=False):
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

        action = np.clip(action, -1, 1)

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
        reward = self.calc_reward(action)

        state = self.get_state()

        if (USE_MOUSE and self.screen and pygame.mouse.get_focused()):
            mouse_pos = pygame.mouse.get_pos()
            self.ob_x = mouse_pos[0]
            self.ob_y = mouse_pos[1]

        if (self.steps > MAX_STEPS):
            self.done = True

        return np.array(state), reward, self.done, {}

    def calc_reward(self, action, alpha=0.1, beta=0.01):
        """
        Reward is -ve abs distance
        unless pointer is on objective its dist+1
        (therefore positive)
        :return: reward
        """
        #dist_pen = -self.get_dist() / (S_WIDTH / 2)
        dist_pen = -self.get_dist() / self.normalize_len


        action_pen = sum(-beta * abs(action))
        h = ((dist_pen * 2 + alpha * 2) ** (1 / 2) + alpha)

        r = dist_pen + action_pen
        # r = (h + action_pen)

        # r = math.sqrt(dist**2 + alpha**2) + alpha + action_pen
        # print(f"dist: {dist}, action pen {action_pen}, reward {r}")
        # r = -(dist / (S_WIDTH/2))
        # if(self.steps > MAX_STEPS):
        #     self.done=True
        #     r -= 10
        #     return r
        # if dist < DIST_THRESH and (not self.done):
        #     r += 2.0
        #     self.at_objective_n += 1
        #     if self.at_objective_n > HOLD_COUNT:
        #         r +=END_REWARD
        #         self.done = True
        # elif dist > DIST_THRESH:
        #     self.at_objective_n = 0
        #     self.done = False
        return r

    def get_state(self):
        '''
        Gets the state, [at_obj] [jointx-objx, jointy-objy]*N_JOINTS + [dist from centrex, dfcy]
        '''
        # angles = [normalize(arm.angle, 0, 2 * math.pi) for arm in self.arms]
        arm_coords = []
        arm_angs = []
        if self.extra_state:

            for arm in self.arms:
                arm_coords.append(arm.x)
                arm_coords.append(arm.y)
                arm_angs.append(arm.angle)
            state = np.concatenate(
                [[self.ob_x, self.ob_y], arm_coords + [self.arms[-1].endX, self.arms[-1].endY], arm_angs])
        else:
            in_point = 1. if self.at_objective_n > 0. else 0.

            for arm in self.arms:
                arm_coords.append(arm.endX - self.ob_x)
                arm_coords.append(arm.endY - self.ob_y)

            # dist = np.asarray([self.centre_x - self.ob_x, self.centre_y - self.ob_y]) / (S_WIDTH / 2)
            # arm_coords = np.asarray(arm_coords) / (S_WIDTH / 2)

            dist = np.asarray([self.centre_x - self.ob_x, self.centre_y - self.ob_y]) / self.normalize_len
            arm_coords = np.asarray(arm_coords) / self.normalize_len

            state = np.concatenate([[in_point], dist, arm_coords])

        return state

    def reset(self):
        if (RESET_ARM_ANGS):
            for arm in self.arms:
                arm.setAngle(0 + random.uniform(0, 0.01))
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
        pygame.event.get()
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

        # make the objective slightly within the screen
        if self.ob_x > S_WIDTH:
            self.ob_x = S_WIDTH - 10
        if self.ob_y > S_HEIGHT:
            self.ob_y = S_HEIGHT - 10
        if self.ob_x < 0:
            self.ob_x = 10
        if self.ob_y < 0:
            self.ob_y = 10

    def spawn_obstacle(self):
        ...

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
        self.angle %= math.pi * 2
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