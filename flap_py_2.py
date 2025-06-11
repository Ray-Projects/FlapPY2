import pygame
from sys import exit

# sprites
class Sky(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/background-day.png")
        tmp0 = self.image.width * scaling
        tmp1 = self.image.height * scaling
        self.image = pygame.transform.scale(self.image, (tmp0, tmp1))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x, 0))

# functions
def add_sprites():
    skies.add(Sky(0))
    skies.add(Sky(1024))

def render_objects():
    skies.draw(screen)

def update_objects():
    skies.update()


# initiating variables
pygame.init()
screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# starting vars
scaling = 2

skies = pygame.sprite.Group()
add_sprites()

# game loop
running = True
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if running:
        update_objects()
        render_objects()

    pygame.display.flip()
    clock.tick(60)