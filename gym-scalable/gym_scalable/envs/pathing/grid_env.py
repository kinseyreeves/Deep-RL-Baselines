import gym
from gym_scalable.envs.pathing.grid import *
from gym import spaces
import time
import pygame

S_WIDTH = 500
INT_ACTION = True



class GridEnv():
    """
    Base Grid Env stub for other grid envs to extend.


    """
    total_eps = 0

    def __init__(self, config):

        self.steps = 0
        self.reward = 0
        self.done = False
        self.action_space = spaces.Discrete(4)

        self.entities = []

        self.screen = None
        print(f"Starting  with config {config}")

        if "mapfile" in config:
            self.map_file = config["mapfile"]
        else:
            print("Error : Please enter a mapfile")
            exit(1)

        self.randomize_start = config["randomize_start"] if "randomize_start" in config else False
        self.normalize_state = config["normalize_state"] if "normalize_state" in config else False
        self.capture_reward = config["capture_reward"] if "capture_reward" in config else False
        self.randomize_goals = config["randomize_goals"] if "randomize_goals" in config else False
        self.encoded_state = config["encoded_state"] if "encoded_state" in config else False

        self.grid = GridMap(self.map_file, S_WIDTH)

    def step(self, action):
        if INT_ACTION:
            z_arr = np.zeros(self.action_space.n)
            z_arr[action] = 1
            self.action = z_arr
        self.steps += 1
        self.reward = 0

    def reset(self):
        self.reward = 0
        self.steps = 0
        self.done = False
        self.total_eps += 1

    def render(self):
        if self.screen is None:
            self.screen = pygame.display.set_mode((S_WIDTH, S_WIDTH))
            self.screen.fill((255, 255, 255))


        self.screen.fill((255, 255, 255))
        self.grid.render(self.screen)
        time.sleep(0.1)

