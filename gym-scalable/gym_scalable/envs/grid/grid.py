import random
import pygame
import numpy as np
import collections

from gym_scalable.envs.grid.grid_entity import *

"""
Grid which serves as the lower level of all grid environments
i.e. maze solver, chaser, evader etc
Contains functionality for all environments and can be used to create
new grid environments easily

Kinsey Reeves 2020

"""

WALL_WIDTH = 10

WALL_COLOUR = (100, 100, 100)
BACKGROUND_COLOUR = ()


class Node:
    """
    Node for A*
    """

    def __init__(self, parent=None, position=None):
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
    Contains functionality for the 2d rendered gridmap.
    Includes
    - setting/removing agent goals
    - A* pathfinding between two points
    - Curriculum learning functionality

    Can be easily used for implementing new grid environments

    """
    map = []
    colours = {'O': (255, 255, 255), 'G': (0, 255, 0), 'X': (0, 0, 255),
               'S': (255, 0, 0), '-': (255, 0, 0), '+': (255, 0, 0)}

    state_encoding_nonmaze = {' ': 0, 'G': 0, '-': 1, '|': 1, '+': 1, 'S': 0}
    state_encoding_maze = {' ': 0, 'G': 2, '-': 1, '|': 1, '+': 1, 'S': 0}

    # All walkable positions
    walkable = set()
    a_searched = set()
    marked_positions = set()
    goals = set()
    static_goals = set()
    curriculum_goals = set()

    entities = []

    render_goals = False

    def __init__(self, mapfile, screen_width):

        self.screen = None
        self.map = self.read_map(mapfile)
        self.screen_width = screen_width

        self.width = len(self.map[0]) // 2
        self.height = len(self.map) // 2
        self.block_size = screen_width / len(self.map[0])

        self.block_width = screen_width / self.width
        self.block_height = screen_width / self.height

        # Action conversion:
        left = np.asarray([1, 0, 0, 0, 0])
        right = np.asarray([0, 1, 0, 0, 0])
        up = np.asarray([0, 0, 1, 0, 0])
        down = np.asarray([0, 0, 0, 1, 0])
        stay = np.asarray([0, 0, 0, 0, 1])

        self.actions_table = {(-2, 0): left, (2, 0): right, (0, -2): up, (0, 2): down}

    def render(self, screen):
        """
        Grid rendering function, renders everything
        #TODO refactor this
        """
        if (not self.screen):
            self.font = pygame.font.Font(None, 32)
            self.text = self.font.render(None, True, (0, 0, 0), None)
            self.text_rect = self.text.get_rect()
            self.screen = screen

        # Map rendering
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                # We're at a wall row
                if y % 2 == 0:
                    if self.map[y][x] == '+':
                        # maybe do something here
                        continue
                    if self.map[y][x] == '-':
                        r = (
                            ((x - 1) / 2) * self.block_width - WALL_WIDTH / 2,
                            (y / 2) * self.block_height - WALL_WIDTH / 2,
                            self.block_width + WALL_WIDTH / 2, WALL_WIDTH)
                        pygame.draw.rect(screen, WALL_COLOUR, r)

                # Either columns or walls
                elif x % 2 == 0:
                    if self.map[y][x] == '|':
                        r = ((x / 2) * self.block_width - WALL_WIDTH / 2,
                             ((y - 1) / 2) * self.block_height - int(WALL_WIDTH / 2),
                             WALL_WIDTH, self.block_height + WALL_WIDTH)
                        pygame.draw.rect(screen, WALL_COLOUR, r)
                # Goal and start
                if self.render_goals:
                    if self.map[y][x] == 'G':
                        r_goal = ((round(((x - 1) / 2) * self.block_width + (self.block_width / 2))),
                                  round((((y - 1) / 2) * self.block_height + (self.block_height / 2))), 10, 10)
                        pygame.draw.rect(screen, (50, 255, 0), r_goal)
                    if self.map[y][x] == 'S':
                        r_start = ((round(((x - 1) / 2) * self.block_width + (self.block_width / 2))),
                                   round((((y - 1) / 2) * self.block_height + (self.block_height / 2))), 10, 10)
                        pygame.draw.rect(screen, (255, 50, 0), r_start)

        # Render marked positions
        for pos in self.marked_positions:
            x = pos[0]
            y = pos[1]
            rect = ((round(((x - 1) / 2) * self.block_width + (self.block_width / 2))),
                    round((((y - 1) / 2) * self.block_height + (self.block_height / 2))), 3, 3)
            pygame.draw.rect(screen, (10, 10, 10), rect)

        # Util rendering
        self.text_rect.center = (self.screen_width - self.screen_width / 4, self.screen_width - self.screen_width / 20)
        screen.blit(self.text, self.text_rect)

    def encode(self, entities=None, maze=True):
        """
        Encodes the map. Note -1s and -2s are to reshape it to
        only take the inner grid
        """

        encoding = np.zeros((len(self.map) - 2, len(self.map[0]) - 2))
        for y in range(1, len(self.map) - 1):
            for x in range(1, len(self.map) - 1):
                if (maze):
                    encoding[y - 1][x - 1] = self.state_encoding_maze[self.map[y][x]]
                else:
                    encoding[y - 1][x - 1] = self.state_encoding_nonmaze[self.map[y][x]]
        if entities:
            n = 3
            for e in entities:
                e_pos = e.get_pos()
                encoding[e_pos[1] - 1][e_pos[0] - 1] = n

        return encoding

    def convert_table_position(self, pos):
        """
        Used for tabular encoding, converts an x,y coord to a
        single integer, ordered from top left to bottom right
        (screen rendering order)
        Indexing starts at 1 so 0 works as
        x,y -- > y*width + x
        :param pos:
        :return: position integer
        """
        pos = self.convert_pos(pos)
        encoding = pos[1] * self.get_nowall_size() + pos[0] + 1
        return encoding

    def encode_tabular(self, entitity_positions=None, captured_goal = False, maze=True):
        """
        Encodes for a tabular learning algorithm. Returns a hashable
        tuple of the entities, and goals positions as single integers. i.e.
        x,y -- > y*width + x
        If the postions are from the maze environment, the positions are
        sorted
        :return:
        """
        state = np.zeros(len(entitity_positions))
        for i in range(0, len(state)):
            state[i] = self.convert_table_position(entitity_positions[i])

        if not maze:
            out = state
        else:
            current_goals = self.get_goals().intersection(self.get_static_goals())
            goal_state = np.zeros(len(self.get_static_goals()))
            if current_goals:
                for i, goal in enumerate(current_goals):
                    goal_state[i] = self.convert_table_position(goal)

            cap = 1 if captured_goal else 0

            out = np.concatenate([state, sorted(goal_state, reverse=True), [cap]])
        return out

    def get_curriculum_goal_positions(self):
        """
        :return: list : goal positions
        """
        return list(self.curriculum_goals)

    def update_curriculum_goal_positions(self, entitity_positions=None):
        """
        Updates the new possible positions for curriculum learning
        :return:
        """
        new_positions = set()
        for pos in self.curriculum_goals:
            neighbours = self.get_neighbours(*pos)
            new_positions.update(set(neighbours))

        self.curriculum_goals.update(new_positions)

        if entitity_positions:
            self.set_curriculum_goals(self.curriculum_goals.difference(set(entitity_positions)))

        # print(self.curriculum_goals)

    def encode_no_walls(self, entities=None, maze=True):
        """
        Encodes the state without walls, so it is a 2D array of
        walkable positions only, with encoding for each thing
        """
        encoding = np.zeros((len(self.map) // 2, len(self.map[0]) // 2))

        for y in range(1, len(self.map) - 1):
            for x in range(1, len(self.map) - 1):
                if y % 2 != 0 and x % 2 != 0:
                    if maze:
                        encoding[y // 2][x // 2] = self.state_encoding_maze[self.map[y][x]]
                    else:
                        encoding[y // 2][x // 2] = self.state_encoding_nonmaze[self.map[y][x]]

        if entities:
            for e in entities:
                n = e.get_encode_val()
                e_pos = e.get_pos()
                encoding[e_pos[1] // 2][e_pos[0] // 2] = n
        return encoding

    def encode_stacked(self, entity_positions = None, captured_goal = False, maze=True):
        """
        :param entity_positions:
        :param captured_goal: Whether or not agent has captured the goal
        :return:
        """

        enc = self.encode_tabular(entitity_positions=entity_positions,
                                  captured_goal = captured_goal)
        out = (np.arange(self.get_tabular_encoding_size()) == enc[...,None]-1).astype(int)

        # Don't use rest of matrix
        if not maze:
            out = out[0:len(entity_positions)]

        return out

    def get_encoding_stacked_shape(self, num_entities_goals, maze=True):
        """Gets the shape of an encoded 1hot stacked state"""
        if(maze):
            return num_entities_goals + 2, self.get_tabular_encoding_size()
        else:
            return num_entities_goals, self.get_tabular_encoding_size()

    def mark_position(self, pos):
        """
        Add a block to be marked and rendered, for debugging
        """
        self.marked_positions.add(pos)

    def mark_positions(self, positions):
        """
        Updates the marked positions set, for debugging
        :param positions:
        :return:
        """
        self.marked_positions.update(positions)

    def clear_marked_positions(self):
        """
        Delete all marked positions
        """
        self.marked_positions = set()

    def get_encoding_walls_shape(self):
        """
        Get shape of the state, when its encoded with walls
        """
        return len(self.map) - 2, len(self.map[0]) - 2

    def get_encoding_nowalls_shape(self):
        """
        Get the encoding shape without walls
        """
        return len(self.map) // 2, len(self.map) // 2

    def set_util_text(self, str):
        if self.screen:
            self.text = self.font.render(str, True, (0, 0, 0), None)

    def convert_action(self, direct):
        """
        Converts action to 1hot vector
        """
        return self.actions_table[direct]

    def add_random_goals(self, num_goals):
        """
        Adds randomly placed goals
        """
        for i in range(num_goals):
            pos_pos = random.choice(list(self.walkable - self.goals - {self.start}))
            self.map[pos_pos[1]][pos_pos[0]] = 'G'
            self.goals.add(pos_pos)

        self.static_goals = self.goals.copy()

    def add_goals(self, goals_list):
        self.static_goals = set()
        for g in goals_list:
            self.add_goal(g[0], g[1])
            self.static_goals.add(g)

    def num_goals(self):
        """
        Gets the number of goals present on the grid
        """
        return len(self.goals)

    def num_static_goals(self):
        return len(self.static_goals)

    def get_astar_action(self, pos, goal):
        """
        Gets the converted action in one hot vector format
        """
        path = self.astar_path(pos[0], pos[1], goal[0], goal[1])

        if (len(path) <= 1):
            action = self.actions_table[random.choice(list(self.actions_table))]
        else:
            path = path[1]
            action = self.convert_action((pos[0] - path[0], pos[1] - path[1]))

        return action

    def convert_pos(self, pos):
        """
        Converts the position to actual coordinates
        """
        return (pos[0] // 2, pos[1] // 2)

    def get_astar_dist(self, pos, end):

        path = self.astar_path(pos[0], pos[1], end[0], end[1])
        return len(path) - 1

    def add_entity(self, entity):
        """

        :param entity:
        :return:
        """
        self.entities.append(entity)

    def remove_entity(self):
        # TODO
        pass

    def get_manhatten_dist(self, start, end):
        """
        Returns manhatten distance between two objects in real coords
        :param start: Tuple : start position
        :param end: Tuple : end position
        :return: integer distance value
        """
        x = start[0]
        y = start[1]
        gX = end[0]
        gY = end[1]
        return abs(x - gX) / 2 + abs(y - gY) / 2

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
        A star path, returns the path as a list of block coordinates using the A* pathfinding algorithm
        :param startX:
        :param startY:
        :param endX:
        :param endY:
        :return:
        """
        # TODO fix up innefficiencies in the
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
                if (item.f < current_node.f):
                    current_node = item
                    # current_index = index

            open_list.discard(current_node)
            closed_list.add(current_node)

            if current_node == end_node:

                current = current_node
                # track backwards through the path - reconstruct the path
                while current:
                    path.append(current.position)
                    current = current.parent
                break
            # children = set()
            for new_pos in self.get_neighbours(current_node.position[0], current_node.position[1]):
                child = Node(current_node, new_pos)
                # children.add(child)
                if child in closed_list:
                    continue

                child.g = current_node.g + 1
                child.h = self.get_manhatten_dist(child.position,
                                                  end_node.position)
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
        self.marked_positions.add((x, y))

    def get_dist_list(self, pos):
        """
        Distance list calculated by A*.
        Used for computing TSP/Minimum spanning tree
        to get the benchmark. works with MLrose TSP
        The agents position is always first in the returned
        coords list
        Pos: Position of the agent
        Return : (List of coordinates, list of coords index and the distance)
        @param pos:
        @return:
        """
        coords_list = self.static_goals
        coords_list = [pos] + list(coords_list)

        dist_list = []

        for i, pos in enumerate(coords_list):
            for j in range(i + 1, len(coords_list)):
                pos2 = coords_list[j]
                dist_list.append((i, j, self.get_astar_dist(pos, pos2)))

        return (coords_list, dist_list)

    def is_walkable(self, x, y):
        """
        Whether a position is walkable or not
        :param x:
        :param y:
        :return:
        """
        if x >= len(self.map[0]) or y >= len(self.map):
            return False
        if self.map[y][x] == ' ' or self.map[y][x] == 'G':
            return True
        return False

    def is_goal(self, x, y):
        if self.map[y][x] == 'G':
            return True
        return False

    def get_neighbours(self, x, y):
        """
        Gets a positions neighbours on the grid
        """
        out = []
        if self.is_walkable(x + 1, y) and (x + 2, y):
            out.append((x + 2, y))
        if self.is_walkable(x - 1, y) and (x - 2, y):
            out.append((x - 2, y))
        if self.is_walkable(x, y + 1) and (x, y + 2):
            out.append((x, y + 2))
        if self.is_walkable(x, y - 1) and (x, y - 2):
            out.append((x, y - 2))
        return out

    def set_random_goal_spawn(self):
        """
        Sets a random position for the goal position
        """
        self.map[self.goal[1]][self.goal[0]] = ' '
        # The new goal can't be the previous goal, the starting point, or the starting points neighbours
        bad_spots = {self.goal, self.start}.union(set(self.get_neighbours(self.start[0], self.start[1])))
        self.goal = random.choice(list(self.walkable.difference(bad_spots)))
        self.map[self.goal[1]][self.goal[0]] = 'G'

    def add_goal(self, x, y):
        self.map[y][x] = 'G'
        self.goals.add((x, y))

    def get_goals(self):
        return self.goals

    def remove_goal(self, x, y):
        self.map[y][x] = ' '
        self.goals.remove((x, y))

    def clear_goals(self):
        for goal in self.goals:
            self.set_map(goal[0], goal[1], ' ')
        self.goals = set()
        self.static_goals = set()

    def get_random_walkable(self):
        return random.choice(list(self.walkable))

    def get_random_walkable_non_goal(self, entities):
        all_entities = set([e.get_pos() for e in entities])
        return random.choice(list(self.walkable.difference(self.goals).difference(all_entities)))

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

        for y in range(0, len(out)):
            for x in range(len(out[0])):
                if y % 2 != 0 and x % 2 != 0:
                    if out[y][x] == ' ':
                        self.walkable.add((x, y))
                if (out[y][x] == 'G'):
                    self.walkable.add((x, y))
                    self.goal = (x, y)
                    self.goals.add((x, y))
                    self.static_goals.add((x, y))
                if (out[y][x] == 'S'):
                    self.walkable.add((x, y))
                    self.start = (x, y)

        return out

    def set_map(self, x, y, val):
        self.map[y][x] = val

    def set_curriculum_goals(self, curriculum_goals):
        self.curriculum_goals = curriculum_goals

    def get_walkable_positions(self):
        return self.walkable

    def get_static_goals(self):
        return self.static_goals

    def get_nowall_size(self):
        return self.size // 2

    def get_size(self):
        return self.size

    def get_tabular_encoding_size(self):
        return self.get_nowall_size() ** 2
