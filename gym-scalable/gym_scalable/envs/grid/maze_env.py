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
from gym_scalable.envs.grid.grid import *
from gym_scalable.envs.grid.grid_env import *

INT_ACTION = True


class MazeEnv(gym.Env, GridEnv):
    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''
    name = "Maze Env"

    def __init__(self, config):
        GridEnv.__init__(self,config)

        # Action space initialised to [-1,0,1] for each joint

        # Checking config otherwise use defaults

        self.num_goals = config["num_goals"] if "num_goals" in config else 1
        # Sets the reward to 1 when a goal is found, otherwise uses -ve goals remaining

        # Observation space boundaries

        self.entity = Entity(self.grid.start[0], self.grid.start[1], self.grid)
        self.entities.append(self.entity)

        if self.encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_shape(),
                                                dtype=np.float32)
        elif self.nw_encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_nowalls_shape(),
                                                dtype=np.float32)
        else:
            high = np.array([1, 1] + [1, 1] * self.num_goals)
            low = np.array([0, 0] + [0, 0] * self.num_goals)
            self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        if not self.randomize_goal:
            goals = []
            for _ in range(self.num_goals - self.grid.num_goals()):
                goal = self.grid.get_random_walkable_non_goal(set(self.entities))
                self.grid.add_goal(goal[0], goal[1])
                goals.append(goal)
            self.static_goals = goals
            self.static_goals.append(self.grid.goal)
        else:
            self.grid.add_random_goals(self.num_goals - self.grid.num_goals())

        self.grid.set_render_goals(True)

    def step(self, action):
        GridEnv.step(self, action)

        self.reward = 0 if self.capture_reward else -.1

        self.entity.update(self.action)
        self.set_state()

        if self.grid.is_goal(self.entity.x, self.entity.y):
            self.grid.remove_goal(self.entity.x, self.entity.y)

            if self.capture_reward:
                self.reward = 1
            else:
                self.reward = 1

            if self.grid.num_goals() == 0:
                self.done = True

        if self.steps >= self.max_steps:
            self.done = True
            return self.state, self.reward, self.done, {}

        return self.state, self.reward, self.done, {}


    def set_state(self):
        """
        Sets the state for maze.
        """
        if self.encoded_state:
            self.state = self.grid.encode(entities = self.entities)
        elif self.nw_encoded_state:
            self.state = self.grid.encode_no_walls(entities=self.entities)
        else:
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
        GridEnv.reset(self)

        if not self.randomize_goal:
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
        if self.screen is None:
            pygame.init()
            self.entity.render_setup(self.screen)
        GridEnv.render(self)

        self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)
        pygame.display.update()




