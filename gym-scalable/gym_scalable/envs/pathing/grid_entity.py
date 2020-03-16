import pygame


class Entity:
    # Basic class for defining circle object
    def __init__(self, x, y, grid, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.grid = grid

    def update(self, action):
        if action[0] and self.grid.is_walkable(self.x + 1, self.y):
            self.x += 2
        elif action[1] and self.grid.is_walkable(self.x - 1, self.y):
            self.x -= 2
        elif action[2] and self.grid.is_walkable(self.x, self.y + 1):
            self.y += 2
        elif action[3] and self.grid.is_walkable(self.x, self.y - 1):
            self.y -= 2

    def render(self, screen, block_width, block_height):
        pygame.draw.circle(screen, self.color, ((round(((self.x - 1) / 2) * block_width + (block_width / 2))),
                                                round((((self.y - 1) / 2) * block_height + (block_height / 2)))), 10)

    def update_auto(self):
        pass

    def get_pos(self):
        return (self.x, self.y)


class Chaser(Entity):
    """
    Chaser using A*
    Note: the evader must be initialized first
    """

    def __init__(self, x, y, grid, randomness=0.0, env_controlled=False):
        """
        :param x:
        :param y:
        :param grid:
        :param chasing:
        :param randomness: Probability a random action will be taken
        :return:
        """
        super().__init__(x, y, grid, color=(255, 0, 0))

        self.env_controlled = env_controlled
        self.evading = None

    def update_auto(self):
        if self.chasing:
            action = self.grid.get_astar_move(self.x, self.y, *self.chasing.get_pos())
            super().update(action)

    def update(self, action):
        if self.env_controlled:
            # TODO
            pass
        else:
            action = self.grid.get_astar_move(self.x, self.y, *self.chasing.get_pos())
            super().update(action)

    def set_chasing(self, entity):
        self.chasing = entity


class Evader(Entity):
    def __init__(self, x, y, grid, randomness=0.0):
        """

        :param x:
        :param y:
        :param grid:
        :param chasing:
        :param randomness: Probability a random action will be taken
        :return:
        """
        super().__init__(x, y, grid, color=(255, 0, 255))
        self.chasing = None

    def update_auto(self):
        pass
        # action = self.grid.get_astar_move(self.x, self.y, *self.chasing.get_pos())
        # super().update(action)


