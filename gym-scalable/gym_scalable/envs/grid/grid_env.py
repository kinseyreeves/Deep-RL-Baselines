import gym
from gym_scalable.envs.grid.grid import *
from gym import spaces
import time
import pygame

S_WIDTH = 500
INT_ACTION = True


class GridEnv():
    """
    Base Grid Env stub for other grid envs to extend.

    """
    max_steps = 200
    total_eps = 0

    def __init__(self, config):
        random.seed(1)

        self.steps = 0
        self.total_steps = 0
        self.reward = 0
        self.done = False
        self.action_space = spaces.Discrete(4)
        self.curriculum_value = 1
        self.entities = []
        self.encoded_state = False
        self.nw_encoded_state = False
        self.stack_encoded_state = False

        self.screen = None
        print(f"Starting  with config {config}")

        if "mapfile" in config:
            self.map_file = config["mapfile"]
        else:
            print("Error : Please enter a mapfile")
            exit(1)

        # Settings for all grid environments
        self.randomize_start = config["randomize_start"] if "randomize_start" in config else False
        self.normalize_state = config["normalize_state"] if "normalize_state" in config else False
        self.capture_reward = config["capture_reward"] if "capture_reward" in config else False
        self.randomize_goal = config["randomize_goal"] if "randomize_goal" in config else False
        self.state_encoding = config["state_encoding"] if "state_encoding" in config else "st"
        self.slowdown_step = config["slowdown_step"] if "slowdown_step" in config else False
        self.curriculum = config["curriculum"] if "curriculum" in config else False
        self.curriculum_eps = config["curriculum_eps"] if "curriculum_eps" in config else 100

        self.grid = GridMap(self.map_file, S_WIDTH)

        # Ensure parameters work with eachother
        if self.curriculum:
            self.randomize_goal = False

        if self.state_encoding == "nw":
            self.nw_encoded_state = True
        elif self.state_encoding == "w":
            self.encoded_state = True
        elif self.state_encoding == "st":
            self.stack_encoded_state = True

    def step(self, action):
        if self.slowdown_step:
            time.sleep(0.3)
        if INT_ACTION:
            z_arr = np.zeros(self.action_space.n)
            z_arr[action] = 1
            self.action = z_arr

        self.steps += 1
        self.reward = 0

    def reset(self):
        if self.curriculum:
            self.update_curriculum(curriculum_eps=self.curriculum_eps)
        self.reward = 0
        self.steps = 0
        self.done = False
        self.total_eps += 1


    def render(self):
        if self.screen is None:
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))

        self.grid.set_util_text(f"Steps : {self.steps}")

        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        time.sleep(0.1)

    def update_curriculum(self, curriculum_eps = 100, decay_value=0.99, min_value=0.2):
        if (self.total_eps+1) % curriculum_eps == 0:
            self.curriculum_value = max(min_value, self.curriculum_value * decay_value)

    def get_curriculum_value(self):
        return self.curriculum_value



