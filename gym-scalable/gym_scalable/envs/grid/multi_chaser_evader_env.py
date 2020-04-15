'''
Evader vs Chaser Environment
Multi agent

Author : Kinsey Reeves
Goal:
    evade the chaser as long as possible
    Chaser uses A* with some level of randomness

Map is made up of:
X - boundary
O - walkable tile
S - start tile
G - goal tile

'''

from gym import error, spaces, utils
from gym_scalable.envs import utils
from ray.rllib.env import MultiAgentEnv
from gym_scalable.envs.grid.grid_env import *


class GridChaserVsEvaderEnv(MultiAgentEnv, GridEnv):
    metadata = {'render.modes': ['human']}

    '''
    Basic maze environment, get to the finish
    full state gives the
    '''

    def __init__(self, config):
        GridEnv.__init__(self,config)

        if self.encoded_state:
            self.observation_space = spaces.Box(low=0, high=6,
                                                shape=self.grid.get_encoding_shape(),
                                                dtype=np.float32)
        else:
            high = np.array([1, 1, 1, 1])
            low = np.array([0, 0, 0, 0])

            self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self.reward = {"chaser": 0, "evader": 0}
        self.done = {"chaser": False, "evader": False}

        self.grid.set_render_goals(False)

        # Initialize Entities

        self.evader = Entity(self.grid.goal[0], self.grid.goal[1], self.grid)
        self.chaser = Entity(self.grid.start[0], self.grid.start[1], self.grid)
        self.entities = [self.evader, self.chaser]

    def set_reward(self):
        dist = self.grid.manhatten_dist(*self.evader.get_pos(), *self.chaser.get_pos())
        # dist = self.grid.get_astar_distance(*self.evader.get_pos(), *self.chaser.get_pos())
        self.reward["evader"] = dist
        self.reward["chaser"] = -dist

    def step(self, actions):
        """
        Step takes a dictionary of actions passed in from the RL agents
        e.g.
        {
            "chaser" : 1,
            "evader" : 2
        }
        :param actions:
        :return:
        """
        if self.slowdown_step:
            time.sleep(0.3)

        chaser_action = utils.convert_1hot_action(actions["chaser"], self.action_space.n)
        evader_action = utils.convert_1hot_action(actions["evader"], self.action_space.n)

        self.chaser.update(chaser_action)

        if self.chaser.get_pos() == self.evader.get_pos():
            self.set_done(True)
            return self.state, self.reward, self.done, {}

        self.evader.update(evader_action)

        if self.chaser.get_pos() == self.evader.get_pos():
            self.set_done(True)
            return self.state, self.reward, self.done, {}

        self.grid.set_util_text(f"Steps : {self.steps}")
        self.set_state()
        self.set_reward()

        if self.steps >= self.max_steps:
            self.set_done(True)
            return self.state, self.reward, self.done, {}

        return self.state, self.reward, self.done, {}

    def set_state(self):

        if self.normalize_state:
            state = [utils.normalize(self.evader.x, 0, self.grid.size),
                     utils.normalize(self.evader.y, 0, self.grid.size),
                     utils.normalize(self.chaser.x, 0, self.grid.size),
                     utils.normalize(self.chaser.y, 0, self.grid.size)]
            self.state = {"evader": state, "chaser": state}
        else:
            state = [self.evader.x, self.evader.y, self.chaser.x, self.chaser.y]
            self.state = {"evader": state, "chaser": state}

    def set_done(self, val):
        self.done["evader"] = val
        self.done["chaser"] = val
        self.done["__all__"] = val

    def reset(self):

        self.reward = {"chaser": 0, "evader": 0}
        self.steps = 0
        self.set_done(False)
        self.set_state()

        if self.randomize_goal:
            self.grid.set_random_goal_spawn()
        if self.randomize_start:
            self.grid.set_random_start()

        # Reset positions
        self.evader.set_pos(self.grid.start)
        self.chaser.set_pos(self.grid.goal)

        return self.state

    def render(self, mode='human', close=False):

        if (self.screen is None):
            pygame.init()
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))
            pygame.display.set_caption('RL Chaser Evader Environment')
            for e in self.entities:
                e.render_setup(self.screen)
            self.evader.set_sub_text("Evader")
            self.chaser.set_sub_text("Chaser")

        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        for e in self.entities:
            e.render(self.screen, self.grid.block_width, self.grid.block_height)

        pygame.display.update()
