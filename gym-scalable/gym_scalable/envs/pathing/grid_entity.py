import pygame
import random
import numpy as np

class Entity:
    # Basic class for defining circle object
    def __init__(self, x, y, grid, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.grid = grid
        #self.pos = (x,y)

    def update(self, action):
        #print(action)
        if action[0] and self.grid.is_walkable(self.x + 1, self.y):
            self.x += 2
        elif action[1] and self.grid.is_walkable(self.x - 1, self.y):
            self.x -= 2
        elif action[2] and self.grid.is_walkable(self.x, self.y + 1):
            self.y += 2
        elif action[3] and self.grid.is_walkable(self.x, self.y - 1):
            self.y -= 2
        elif action[4]:
            pass

    def render(self, screen, block_width, block_height):
        pygame.draw.circle(screen, self.color, ((round(((self.x - 1) / 2) * block_width + (block_width / 2))),
                                                round((((self.y - 1) / 2) * block_height + (block_height / 2)))), 10)

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


class AStarChaser(Entity):
    """
    Chaser using A*
    Note: the evader must be initialized first
    """

    def __init__(self, x, y, grid, randomness=0.2, env_controlled=False):
        """
        :param x:
        :param y:
        :param grid:
        :param chasing:
        :param randomness: Probability a random action will be taken #TODO
        :return:
        """
        super().__init__(x, y, grid, color=(255, 0, 0))
        self.evading = None
        self.chased_entities = None
        self.randomness = randomness

    def update_auto(self):
        """

        :param action:
        :return:
        """
        if(random.random() < self.randomness):
            action = self.grid.get_astar_action((self.x, self.y), self.chasing.get_pos())
        else:
            action = self.get_random_action()

        super().update(action)
        

    def set_chasing(self, entity):
        self.chasing = entity

    def set_chased(self, entities):
        self.chased_entities = entities


class AStarEvader(Entity):
    evader_thresh = 4

    def __init__(self, x, y, grid, randomness=0.2):
        """

        :param x:
        :param y:
        :param grid:
        :param chasing:
        :param randomness: Probability a random action will be taken
        :return:
        """
        super().__init__(x, y, grid, color=(255, 0, 255))
        self.evading = None
        self.randomness = randomness


    def update_auto(self):

        if random.random() < self.randomness:
            action = self.get_random_action()
        else:
            best_pos = (self.x, self.y)
            best_dist = 0

            if(self.grid.manhatten_dist(self.x, self.y,self.evading.x, self.evading.y) < self.evader_thresh):
                
                rad_pos = self.get_radius_positions(self.x, self.y, self.evader_thresh)
                walkable = self.grid.get_walkable_positions().intersection(rad_pos)
                # print("Own position: ")
                
                for pos in walkable:
                    chase_dist = self.grid.manhatten_dist(pos[0], pos[1], self.evading.x, self.evading.y)
                    
                    if(chase_dist > best_dist):
                        best_dist = chase_dist
                        best_pos = pos

            action = self.grid.get_astar_action((self.x, self.y), best_pos)

        super().update(action)

    def get_radius_positions(self, x, y, r):
        out = set()
        for i in range(x-r, x+r):
            for j in range(y-r, y+r):
                out.add((i,j))
        
        return out


    def set_evading(self, entity):
        self.evading = entity



