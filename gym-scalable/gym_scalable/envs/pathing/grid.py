import random
import pygame
import numpy as np
import collections

from gym_scalable.envs.pathing.grid_entity import *


"""
Grid which serves as the lower level of all pathing environments
i.e. maze solver, chaser, evader etc

"""

WALL_WIDTH = 10

WALL_COLOUR = (100, 100, 100)
BACKGROUND_COLOUR = ()

class Node:
    """
    Node for A*
    """
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

class GridMap:
    """
    Gridmap containing low level functionality for the grid.

    """
    map = []
    colours = {'O' : (255,255,255), 'G':(0,255,0), 'X':(0,0,255), 'S':(255,0,0), '-':(255,0,0), '+':(255,0,0)}

    #All walkable positions
    walkable = set()
    a_searched = set()
    marked_blocks = set()
    goals = set()
    static_goals = set()

    entities = []

    render_goals = False

    def __init__(self, mapfile, screen_width):
        #print(mapfile)
        
        self.screen = None
        self.map = self.read_map(mapfile)
        self.screen_width = screen_width

        self.width = len(self.map[0]) // 2
        self.height = len(self.map) // 2
        self.block_size = screen_width / len(self.map[0])

        self.block_width = screen_width / self.width
        self.block_height = screen_width / self.height


        # Action conversion:
        left = np.asarray([1, 0, 0, 0,0])
        right = np.asarray([0, 1, 0, 0,0])
        up = np.asarray([0, 0, 1, 0,0])
        down = np.asarray([0, 0, 0, 1,0])
        stay = np.asarray([0,0,0,0,1])

        self.actions_table = {(-2, 0): left, (2, 0): right, (0, -2): up, (0, 2): down, (0,0) : stay}

    def render(self, screen):
        if(not self.screen):
            self.font = pygame.font.Font(None, 32)
            self.text = self.font.render(None, True, (0, 0, 0), None)
            self.text_rect = self.text.get_rect()
            self.screen = screen

        # Map rendering
        for y in range(0,len(self.map)):
            for x in range(0,len(self.map[0])):
                #We're at a wall row
                if y%2==0:
                    if self.map[y][x] == '+':
                        #maybe do something here
                        continue
                    if self.map[y][x] == '-':

                        r = (((x-1)/2) * self.block_width-WALL_WIDTH/2, (y/2) * self.block_height-WALL_WIDTH/2,
                             self.block_width + WALL_WIDTH/2, WALL_WIDTH)
                        pygame.draw.rect(screen, WALL_COLOUR, r)

                #Either columns or walls
                elif x % 2 == 0:
                    if self.map[y][x] == '|':
                        r = ((x / 2) * self.block_width - WALL_WIDTH/2, ((y-1) / 2) * self.block_height - int(WALL_WIDTH/2),
                             WALL_WIDTH, self.block_height + WALL_WIDTH)
                        pygame.draw.rect(screen, WALL_COLOUR, r)
                #Goal and start
                if self.render_goals:
                    if self.map[y][x] == 'G':
                        r_start = ((round(((x - 1) / 2) * self.block_width + (self.block_width / 2))),
                                   round((((y - 1) / 2) * self.block_height + (self.block_height / 2))), 10, 10)
                        pygame.draw.rect(screen, (50, 255, 0), r_start)
                    if self.map[y][x] == 'S':
                        r_start = ((round(((x - 1) / 2) * self.block_width + (self.block_width / 2))),
                                   round((((y - 1) / 2) * self.block_height + (self.block_height / 2))), 10, 10)
                        pygame.draw.rect(screen, (255, 50, 0), r_start)

        # Util rendering
        self.text_rect.center = (self.screen_width-self.screen_width/4, self.screen_width-self.screen_width/20)
        screen.blit(self.text, self.text_rect)

    def set_util_text(self, str):
        if self.screen:
            self.text = self.font.render(str, True, (0, 0, 0), None)

    def convert_action(self, direct):
        """
        Converts action to 1hot vector
        """
        #print(direct)
        return self.actions_table[direct]

    def add_goals(self, num_goals):
        """
        Adds randomly placed goals
        """
        for i in range(num_goals):
            pos_pos = random.choice(list(self.walkable-self.goals-{self.start}))
            self.map[pos_pos[1]][pos_pos[0]] = 'G'
            self.goals.add(pos_pos)

        self.static_goals = self.goals.copy()

    def num_goals(self):
        return len(self.goals)

    def get_astar_action(self, pos, goal):
        """
        Gets the converted action in one hot vector format
        """
        path = self.astar_path(pos[0], pos[1], goal[0], goal[1])
        if len(path) <= 1:
            return self.convert_action((0,0))
        path = path[1]
        action = self.convert_action((pos[0] - path[0], pos[1] - path[1]))
        
        return action

    def get_astar_distance(self, pos, end):

        path = self.astar_path(pos[0], pos[1], end[0], end[1])
        return len(path)

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self):
        #TODO
        pass

    def manhatten_dist(self, x, y, gX, gY):
        return (abs(x-gX) + abs(y-gY))/2

    def get_astar_move(self, startX, startY, endX, endY):
        """
        Gets the single move from A*
        :param startX:
        :param startY:
        :param endX:
        :param endY:
        :return:
        """
        return self.astar_path(startX, startY, endX, endY)[1]

    def astar_path(self, startX, startY, endX, endY):
        """
        A star path, returns the path as a list of block coordinates
        :param startX:
        :param startY:
        :param endX:
        :param endY:
        :return:
        """
        #TODO fix up innefficiencies in the
        start_node = Node(None, (startX, startY))
        end_node = Node(None, (endX, endY))
        start_node.g = start_node.h = start_node.f = 0
        end_node.g = end_node.h = end_node.f = 0

        open_list = set()
        closed_list = set()

        path = []
        open_list.add(start_node)

        while len(open_list) > 0:
            current_node = e = next(iter(open_list))
            current_index = 0

            for index, item in enumerate(open_list):
                if(item.f < current_node.f):
                    current_node = item
                    #current_index = index

            open_list.discard(current_node)
            closed_list.add(current_node)

            if current_node == end_node:

                current = current_node
                #track backwards through the path - reconstruct the path
                while current:
                    path.append(current.position)
                    current = current.parent
                break
            #children = set()
            for new_pos in self.get_neighbours(current_node.position[0], current_node.position[1]):
                child = Node(current_node, new_pos)
                #children.add(child)
                if child in closed_list:
                    continue

                child.g = current_node.g+1
                child.h = self.manhatten_dist(child.position[0], child.position[1],
                                              end_node.position[0], end_node.position[1])
                child.f = child.g + child.h
                open_list.add(child)

        return path[::-1]

    def set_render_goals(self, val):
        self.render_goals = val

    def mark_block(self, x, y):
        """
        Marks a block for rendering purposes
        TODO NOT WORKING
        :param x:
        :param y:
        :return:
        """
        self.marked_blocks.add((x,y))

    def is_walkable(self, x, y):
        if(x >= len(self.map[0]) or y >= len(self.map)):
            return False
        if self.map[y][x] == ' ' or self.map[y][x] == 'G':
            return True
        return False

    def is_goal(self, x, y):
        if self.map[y][x] == 'G':
            return True
        return False

    def get_neighbours(self, x, y, check_searched = False):
        out = []
        if self.is_walkable(x+1, y) and (x+2, y) not in self.a_searched:
            out.append((x+2, y))
        if self.is_walkable(x-1, y) and (x-2, y) not in self.a_searched:
            out.append((x-2, y))
        if self.is_walkable(x, y+1) and (x, y+2) not in self.a_searched:
            out.append((x, y+2))
        if self.is_walkable(x, y-1) and (x, y-2) not in self.a_searched:
            out.append((x, y-2))
        return out

    def set_random_goal_spawn(self):
        """
        Sets a random position for the goal position
        """
        self.map[self.goal[1]][self.goal[0]] = ' '
        #The new goal can't be the previous goal, the starting point, or the starting points neighbours
        bad_spots = {self.goal, self.start}.union(set(self.get_neighbours(self.start[0], self.start[1])))
        self.goal = random.choice(list(self.walkable.difference(bad_spots)))
        self.map[self.goal[1]][self.goal[0]] = 'G'


    def add_goal(self, x, y):
        self.map[y][x] = 'G'
        self.goals.add((x,y))

    def get_goals(self):
        return self.goals

    def remove_goal(self, x, y):
        self.map[y][x] = ' '
        self.goals.remove((x,y))

    def clear_goals(self):
        for goal in self.goals:
            self.set_map(goal[0], goal[1], ' ')
        self.goals = set()
        self.static_goals=set()

    def get_random_walkable(self):
        return random.choice(list(self.walkable))

    def set_random_start(self):
        self.set_map(self.start[0], self.start[1], ' ')
        pos_pos = self.walkable - self.goals - {self.goal}
        self.start = random.choice(list(pos_pos))
        self.set_map(self.start[0], self.start[1], 'S')


    def read_map(self, filename):
        out = []
        f = open(filename)
        
        for i in f.readlines():
            out.append(list(i.strip('\n')))
        self.size = len(out[0])

        for y in range(0,len(out)):
            for x in range(len(out[0])):
                if  y % 2 != 0 and x%2 != 0:
                    if out[y][x] == ' ':
                        self.walkable.add((x,y))
                if(out[y][x] == 'G'):
                    self.walkable.add((x,y))
                    self.goal = (x,y)
                    self.goals.add((x,y))
                    self.static_goals.add((x,y))
                if(out[y][x] == 'S'):
                    self.walkable.add((x,y))
                    self.start = (x,y)

        return out

    def get_walkable_positions(self):
        return self.walkable

    def set_map(self, x, y, val):
        self.map[y][x] = val



