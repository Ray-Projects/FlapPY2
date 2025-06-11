import pygame
import os
from sys import exit

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# starting vars
pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()

# game loop
running = True
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
    clock.tick(60)