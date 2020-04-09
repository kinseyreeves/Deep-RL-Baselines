'''
Maze solving environment
Author : Kinsey Reeves
Goal:
    Solve the maze within a move limit

Map is made up of:
X - boundary
O - walkable tile
S - start tile
G - goal tile

'''

import time

import gym
from gym import spaces, utils
from gym_scalable.envs import utils
from gym_scalable.envs.pathing.grid import *

S_WIDTH = 500

MAX_STEPS = 500

INT_ACTION = True


class MazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''
    total_eps = 0

    def __init__(self, config):

        print(f"Starting MazeEnv with config {config}")

        self.screen = None
        # Action space initialised to [-1,0,1] for each joint

        # Checking config otherwise use defaults
        if "mapfile" in config:
            self.map_file = config["mapfile"]
        else:
            print("Error : Please enter a mapfile")
            exit(1)

        self.randomize_start = config["randomize_start"] if "randomize_start" in config else False
        self.normalize_state = config["normalize_state"] if "normalize_state" in config else False
        self.num_goals = config["num_goals"] if "num_goals" in config else False
        # Sets the reward to 1 when a goal is found, otherwise uses -ve goals remaining
        self.capture_reward = config["capture_reward"] if "capture_reward" in config else False
        self.fixed_goals = config["fixed_goals"] if "fixed_goals" in config else False

        # Observation space boundaries
        high = np.array([1, 1] + [1, 1] * self.num_goals)
        low = np.array([0, 0] + [0, 0] * self.num_goals)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self.centre_x = round(S_WIDTH / 2)
        self.centre_y = round(S_WIDTH / 2)
        self.steps = 0
        self.reward = 0
        self.done = False
        self.grid = GridMap(self.map_file, S_WIDTH)

        if self.fixed_goals:
            goals = [self.grid.get_random_walkable_non_goal() for _ in range(self.num_goals - self.grid.num_goals())]
            goals+=[self.grid.goal]
            self.static_goals = goals
            for g in goals:
                self.grid.add_goal(g[0], g[1])

        else:
            self.grid.add_random_goals(self.num_goals - self.grid.num_goals())

        self.grid.set_render_goals(True)

        self.entity = Entity(self.grid.start[0], self.grid.start[1], self.grid)
        self.state = self.reset()

    def step(self, action):

        if INT_ACTION:
            z_arr = np.zeros(self.action_space.n)
            z_arr[action] = 1
            action = z_arr

        self.entity.update(action)

        self.steps += 1

        self.reward = 0 if self.capture_reward else -.1

        self.set_state()

        if self.grid.is_goal(self.entity.x, self.entity.y):
            self.grid.remove_goal(self.entity.x, self.entity.y)

            if self.capture_reward:
                self.reward = 1
            else:
                self.reward=1
            if self.grid.num_goals() == 0:
                self.reward = (MAX_STEPS-self.steps)*.05
                self.done = True

        if self.steps >= MAX_STEPS:
            self.done = True
            return self.state, self.reward, self.done, {}

        return self.state, self.reward, self.done, {}

    def set_state(self):
        if self.normalize_state:
            self.state = [utils.normalize(self.entity.x, 0, self.grid.size),
                          utils.normalize(self.entity.y, 0, self.grid.size)]
            for goal in self.grid.static_goals:
                self.state += [utils.normalize(goal[0], 0, self.grid.size),
                               utils.normalize(goal[1], 0, self.grid.size)]
        else:
            self.state = [self.entity.x, self.entity.y]
            for goal in self.grid.static_goals:
                self.state += [goal[0], goal[1]]

        self.state = np.asarray(self.state)

    def reset(self):

        self.reward = 0
        self.steps = 0
        self.done = False
        self.total_eps+=1


        if self.fixed_goals:
            self.grid.clear_goals()
            self.grid.add_goals(self.static_goals)
        else:
            self.grid.clear_goals()
            self.grid.add_random_goals(self.num_goals)

        self.set_state()

        if self.randomize_start:
            self.grid.set_random_start()

        self.entity.x = self.grid.start[0]
        self.entity.y = self.grid.start[1]

        return self.state

    def render(self, mode='human', close=False):

        # If screen isnt initiated, initiate it, fill it white
        if self.screen is None:
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.init()
        self.screen.fill((255, 255, 255))
        self.entity.render_setup(self.screen)
        self.grid.render(self.screen)
        self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)

        time.sleep(0.1)
        pygame.display.update()
