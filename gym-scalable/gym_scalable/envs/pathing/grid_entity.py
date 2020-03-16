import pygame


class Entity:
    # Basic class for defining circle object
    def __init__(self, x, y, grid, color=(0,255,0)):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0
        self.grid = grid

    def update(self, action):
        if action[0] and self.grid.is_walkable(self.x+1, self.y):
            self.x+=2
        elif action[1] and self.grid.is_walkable(self.x-1, self.y):
            self.x-=2
        elif action[2] and self.grid.is_walkable(self.x, self.y+1):
            self.y+=2
        elif action[3] and self.grid.is_walkable(self.x, self.y-1):
            self.y-=2

    def render(self, screen, block_width, block_height):

        pygame.draw.circle(screen, self.color, ((round(((self.x-1)/2)*block_width+(block_width/2))), round((((self.y-1)/2)*block_height+(block_height/2)))), 10)

        # TODO draw vector in direction of entity
        # pygame.draw.line(screen, (255,90,0), )


    def move_towards(self, x, y):
        ...

    def get_entity_info(self):
        #Return the location, angle and other info
        ...