import pygame
import random
import numpy as np


class Entity:
    # Basic class for defining circle object
    def __init__(self, x, y, grid, color=(0, 200, 100)):
        self.x = x
        self.y = y
        self.color = color
        self.grid = grid
        self.screen = None
        self.render_sub_text = False

    def update(self, action):
        if action[0] and self.grid.is_walkable(self.x + 1, self.y):
            self.x += 2
        elif action[1] and self.grid.is_walkable(self.x - 1, self.y):
            self.x -= 2
        elif action[2] and self.grid.is_walkable(self.x, self.y + 1):
            self.y += 2
        elif action[3] and self.grid.is_walkable(self.x, self.y - 1):
            self.y -= 2
        elif (len(action) > 4) and action[4]:
            pass

    def render(self, screen, block_width, block_height):

        x = round(((self.x - 1) / 2) * block_width + (block_width / 2))
        y = round((((self.y - 1) / 2) * block_height + (block_height / 2)))

        pygame.draw.circle(screen, self.color, ((round(((self.x - 1) / 2) * block_width + (block_width / 2))),
                                                round((((self.y - 1) / 2) * block_height + (block_height / 2)))),
                           int(block_height / 5))
        self.text_rect.center = (x, y)
        screen.blit(self.text, self.text_rect)

        if self.render_sub_text:
            self.sub_text_rect.center = (x - int(block_height / 5), y + int(block_height / 3))
            screen.blit(self.sub_text, self.sub_text_rect)

    def set_text(self, text):
        self.text = self.font.render(text, True, (0, 0, 0), None)

    def set_sub_text(self, text):
        self.render_sub_text = True
        self.sub_text = self.sub_font.render(text, True, (0, 0, 0), None)

    def update_auto(self):
        pass

    def get_pos(self):
        return (self.x, self.y)

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_random_action(self):
        neighbours = self.grid.get_neighbours(self.x, self.y)
        new_pos = random.choice(neighbours)
        action = self.grid.convert_action((self.x - new_pos[0], self.y - new_pos[1]))
        return action

    def render_setup(self, screen):
        self.screen = screen
        self.render_text = "R"

        self.render_sub_text = False

        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(self.render_text, True, (0, 0, 0), None)
        self.text_rect = self.text.get_rect()

        self.sub_font = pygame.font.Font(None, 20)
        self.sub_text = self.font.render(self.render_text, True, (0, 0, 0), None)
        self.sub_text_rect = self.text.get_rect()


class AStarChaser(Entity):
    """
    Chaser using A*
    Note: the evader must be initialized first
    """

    def __init__(self, x, y, grid, randomness=0.1, env_controlled=False):
        """
        :param x:
        :param y:
        :param grid:
        :param chasing:
        :param randomness: Probability a random action will be taken #TODO
        :return:
        """
        super().__init__(x, y, grid, color=(255, 0, 0))
        # super().setText("C")
        self.evading = None
        self.chased_entities = None
        self.randomness = randomness

    def update_auto(self):
        """

        :param action:
        :return:
        """
        if (random.random() < self.randomness):
            action = self.get_random_action()
        else:
            action = self.grid.get_astar_action((self.x, self.y), self.chasing.get_pos())

        super().update(action)

    def set_chasing(self, entity):
        self.chasing = entity

    def set_chased(self, entities):
        self.chased_entities = entities


class AStarEvader(Entity):
    evader_thresh = 4

    def __init__(self, x, y, grid, randomness=0.3):
        """

        :param x:
        :param y:
        :param grid:
        :param chasing:
        :param randomness: Probability a random action will be taken
        :return:
        """
        super().__init__(x, y, grid, color=(200, 0, 100))
        self.evading = None
        self.randomness = randomness
        # super().setText("E")

    def update_auto(self):

        if random.random() < self.randomness:
            action = self.get_random_action()
        else:
            best_pos = (self.x, self.y)
            best_dist = 0

            if self.grid.manhatten_dist(self.x, self.y, self.evading.x, self.evading.y) < self.evader_thresh:

                rad_pos = self.get_radius_positions(self.x, self.y, self.evader_thresh)
                walkable = self.grid.get_walkable_positions().intersection(rad_pos)
                # print("Own position: ")

                for pos in walkable:
                    chase_dist = self.grid.manhatten_dist(pos[0], pos[1], self.evading.x, self.evading.y)

                    if (chase_dist > best_dist):
                        best_dist = chase_dist
                        best_pos = pos

            action = self.grid.get_astar_action((self.x, self.y), best_pos)

        super().update(action)

    def get_radius_positions(self, x, y, r):
        out = set()
        for i in range(x - r, x + r):
            for j in range(y - r, y + r):
                out.add((i, j))

        return out

    def set_evading(self, entity):
        self.evading = entity
