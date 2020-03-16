import pygame
import numpy as np


screen = pygame.display.set_mode((500,600))
screen.fill((255,255,255))
pygame.init()
screen.fill((255,255,255))

pxarray = pygame.PixelArray(screen)

pxarray[40,50] = pygame.Color(255, 0, 255)


pixels = pygame.surfarray.array3d(screen)

print(np.shape(pixels))