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

        GridEnv.__init__(self, config)

        # Action space initialised to [-1,0,1] for each joint

        # Checking config otherwise use defaults

        self.num_goals = config["num_goals"] if "num_goals" in config else 1
        # Sets the reward to 1 when a goal is found, otherwise uses -ve goals remaining

        # Observation space boundaries

        self.entity = Entity(self.grid.start[0], self.grid.start[1], self.grid)
        self.entities.append(self.entity)

        if self.encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_walls_shape(),
                                                dtype=np.float32)
        elif self.nw_encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_nowalls_shape(),
                                                dtype=np.float32)
        elif self.stack_encoded_state:
            self.observation_space = spaces.Box(low=0, high=1,
                                                shape=self.grid.get_encoding_stacked_shape(
                                                    self.num_goals),
                                                dtype=np.float32)
        else:
            m = self.grid.get_tabular_encoding_size()
            high = np.array([m,m] + [m] * self.num_goals)
            low = np.array([0,0] + [0] * self.num_goals)
            self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # Goal strategies, fixed, random or curriculum
        if self.randomize_goal:
            self.grid.add_random_goals(self.num_goals - self.grid.num_goals())
        elif self.curriculum:
            self.grid.add_random_goals(self.num_goals - self.grid.num_goals())
            self.grid.set_curriculum_goals(self.grid.get_static_goals())
        else:
            goals = []
            for _ in range(self.num_goals - self.grid.num_goals()):
                goal = self.grid.get_random_walkable_non_goal(set(self.entities))
                self.grid.add_goal(goal[0], goal[1])
                goals.append(goal)
            self.static_goals = goals
            self.static_goals.append(self.grid.goal)

        self.grid.set_render_goals(True)

    def step(self, action):
        """
        :param action:
        :return: tuple containing (state, reward, done, info)
        """
        GridEnv.step(self, action)
        captured_goal = False
        self.reward = -0.1

        self.entity.update(self.action)

        if self.grid.is_goal(self.entity.x, self.entity.y):
            self.grid.remove_goal(self.entity.x, self.entity.y)
            captured_goal = True

            if self.capture_reward:
                self.reward = 1

            if self.grid.num_goals() == 0:
                self.done = True

        self.set_state(goal=captured_goal)

        if self.steps >= self.max_steps:
            self.done = True
            return self.state, self.reward, self.done, {}

        return self.state, self.reward, self.done, {}

    def reset(self):
        """
        Resets the state to its initial state
        :return:
        """
        GridEnv.reset(self)

        # Random goals
        if self.randomize_goal:
            self.grid.clear_goals()
            self.grid.add_random_goals(self.num_goals)
        # Curriculum goals
        elif self.curriculum:
            self.update_curriculum_positions(curriculum_eps=self.curriculum_eps)
            self.grid.clear_goals()
            self.grid.add_goals(
                random.sample(self.grid.get_curriculum_goal_positions(),
                              self.num_goals))
        else:
            self.grid.clear_goals()
            self.grid.add_goals(self.static_goals)

        if self.randomize_start:
            self.grid.set_random_start()

        self.entity.x = self.grid.start[0]
        self.entity.y = self.grid.start[1]

        self.set_state()

        return self.state

    def render(self, mode='human', close=False):
        if self.screen is None:
            pygame.init()
            self.entity.render_setup(self.screen)
        GridEnv.render(self)
        self.entity.render(self.screen, self.grid.block_width, self.grid.block_height)
        pygame.display.update()

    def set_state(self, goal=False):
        """
        Sets the state for maze.
        """
        if self.encoded_state:
            self.state = self.grid.encode(entities=self.entities)
        elif self.nw_encoded_state:
            self.state = self.grid.encode_no_walls(entities=self.entities)
        elif self.stack_encoded_state:
            self.state = self.grid.encode_stacked(
                entity_positions=[e.get_pos() for e in self.entities])
        else:
            encoding = self.grid.encode_tabular(
                [e.get_pos() for e in self.entities], captured_goal=goal)
            if self.normalize_state:
                self.state = utils.normalize(encoding, 0, self.grid.get_tabular_encoding_size())
            else:
                self.state = encoding

    def update_curriculum_positions(self, curriculum_eps=100):
        """
        Updates the positions for curriculum learning
        :param episode_amount:
        :return:
        """
        self.grid.mark_positions(self.grid.get_curriculum_goal_positions())
        if self.total_eps % curriculum_eps == 0:
            self.grid.update_curriculum_goal_positions([self.entity.get_pos()])
