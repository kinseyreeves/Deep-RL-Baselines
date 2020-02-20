import random
import pygame

"""
File 

"""

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

class GridMap:
    map = []
    colours = {'O' : (255,255,255), 'G':(0,255,0), 'X':(0,0,255), 'S':(255,0,0)}

    walkable = set()
    a_searched = set()
    marked_blocks = set()

    def __init__(self, mapfile, screen_width):

        self.map = self.read_map(mapfile)
        self.screen_width = screen_width

        self.size = len(self.map[0])
        self.block_size = screen_width / len(self.map[0])

        print(f"start : {self.start}")
        print(f"end : {self.goal}")

        path = self.astar_path(self.start[0],self.start[1], self.goal[0],self.goal[1])
        for n in path:
            self.marked_blocks.add(n)

        self.marked_blocks.add(self.goal)


    def render(self, screen):
        for i in range(0,self.size):
            for j in range(0,self.size):
                block = self.map[i][j]
                r = (j*self.block_size,i*self.block_size,self.block_size,self.block_size)

                pygame.draw.rect(screen, self.colours[block], r)

        for item in self.marked_blocks:
            r = (self.block_size*item[0], self.block_size*item[1], self.block_size/2, self.block_size/2)
            pygame.draw.rect(screen, (0,0,0), r)

    def manhatten_dist(self, x, y, gX, gY):
        return abs(x-gX) + abs(y-gY)

    def get_astar_move(self, startX, startY, endX, endY):
        return self.astar_path(startX, startY, endX, endY)[0]

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

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0

            print(current_node.position)

            #[TODO DO WITH HEAP]
            for index, item in enumerate(open_list):
                if(item.f < current_node.f):
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)


            if current_node == end_node:
                print("FOUND GOAL")
                path = []
                current = current_node

                #track backwards through the path
                while current:
                    path.append(current.position)
                    current = current.parent
                print(path)
                return path[::-1]

            children = []
            for new_pos in self.get_neighbours(current_node.position[0], current_node.position[1]):
                new_node = Node(current_node, new_pos)
                children.append(new_node)
                #print("here")

            for child in children:
                if child in closed_list:
                    continue

                child.g = current_node.g+1
                child.h = self.manhatten_dist(child.position[0], child.position[1],
                                              end_node.position[0], end_node.position[1])
                child.f = child.g + child.h

                #[TODO] Do this with a heap
                for open_node in open_list:
                    if(child == open_node and child.g > open_node.g):
                        continue

                open_list.append(child)


    def get_bfs_path(self, startX, startY, endX, endY):
        neighbours = self.get_neighbours(startX, startY)
        self.a_searched.add((startX, startY))
        self.marked_blocks.add((startX, startY))
        curr = random.choice(neighbours)
        self.astar_search(curr[0], curr[1], endX, endY)

    def bfs_path(self, currX, currY, endX, endY):
        self.a_searched.add((currX, currY))
        self.mark_block(currX, currY)

        if((currX, currY) == (endX, endY)):
            print("found path")
            return
        neighbours = self.get_neighbours(currX, currY, check_searched=True)
        for n in neighbours:
            self.bfs_path(n[0], n[1], endX, endY)



    def mark_block(self, x, y):
        self.marked_blocks.add((x,y))


    def is_walkable(self, x, y):
        if self.map[y][x] == 'O' or self.map[y][x] == 'G':
            return True
        return False

    def is_goal(self, x, y):
        if self.map[y][x] == 'G':
            return True
        return False

    def get_neighbours(self, x, y, check_searched = False):
        out = []
        if self.is_walkable(x+1, y) and (x+1, y) not in self.a_searched:
            out.append((x+1, y))
        if self.is_walkable(x-1, y)and (x-1, y) not in self.a_searched:
            out.append((x-1, y))
        if self.is_walkable(x, y+1)and (x, y+1) not in self.a_searched:
            out.append((x, y+1))
        if self.is_walkable(x, y-1)and (x, y-1) not in self.a_searched:
            out.append((x, y-1))
        return out


    def read_map(self, filename):
        out = []
        f = open(filename)
        for i in f.readlines():
            out.append(list(i.strip('\n')))
        if(len(out[0])!=len(out)):
            print("Map file invalid")
            exit(0)

        for x in range(0, len(out)):
            for y in range(0, len(out[x])):
                if out[y][x] == 'G':
                    self.goal = (x, y)
                if out[y][x] == 'S':
                    self.start = (x,y)

        return out
