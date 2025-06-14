import pygame
from sys import exit
from random import randint

# sprites
class Sky(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/background-day.png").convert()
        tmp0 = self.image.width * scaling
        tmp1 = self.image.height * scaling
        self.image = pygame.transform.scale(self.image, (tmp0, tmp1))
        self.rect = self.image.get_rect(topleft=(0, 0))


class Base(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/base.png").convert()
        tmp0 = self.image.width * scaling
        tmp1 = self.image.height * scaling
        self.image = pygame.transform.scale(self.image, (tmp0, tmp1))
        self.rect = self.image.get_rect(bottomleft=(x, 1024))

    def move(self):
        self.rect.x -= 3

        if self.rect.x <= -important_coords[0]:
            self.rect.x = important_coords[0]

    def update(self):
        self.move()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/pipe-green.png").convert_alpha()
        tmp0 = self.image.width * scaling
        tmp1 = self.image.height * scaling
        self.image = pygame.transform.scale(self.image, (tmp0, tmp1))

        self.position = position
        if self.position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y))
        elif self.position == -1:
            self.rect = self.image.get_rect(topleft=(x, y))

        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        global pipes

        self.rect.x -= 3

        if not(self.rect.x <= -self.image.width):
            return
        if self.position == 1:
            add_pipe(important_coords[1] -self.image.width, randint(300, 700))
        self.kill()

    def update(self):
        self.move()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.downflap = pygame.image.load("flappy-bird-assets-master/sprites/yellowbird-downflap.png").convert_alpha()
        self.midflap = pygame.image.load("flappy-bird-assets-master/sprites/yellowbird-midflap.png").convert_alpha()
        self.upflap = pygame.image.load("flappy-bird-assets-master/sprites/yellowbird-upflap.png").convert_alpha()

        # all the bird flapping images are the same width and height, so we don't have to get the size of every single one!
        tmp0 = self.downflap.width * scaling
        tmp1 = self.downflap.height * scaling
        self.downflap = pygame.transform.scale(self.downflap, (tmp0, tmp1))
        self.midflap = pygame.transform.scale(self.midflap, (tmp0, tmp1))
        self.upflap = pygame.transform.scale(self.upflap, (tmp0, tmp1))

        self.flap = [self.downflap, self.midflap, self.upflap, self.midflap]
        self.index = 0
        self.image = self.flap[self.index]
        self.rect = self.image.get_rect(topleft=(250, 200))
        self.mask = pygame.mask.from_surface(self.image)

        self.acceleration = 0

    def move(self):
        global mode, gravity

        self.acceleration += gravity
        self.rect.y += self.acceleration

        if self.rect.y < 224:
            mode = "dead"

    def animate(self):
        self.index += 0.3
        if self.index >= len(self.flap):
            self.index = 0
        self.image = self.flap[int(self.index)]

    def update(self):
        self.move()
        self.animate()

# functions
def add_sprites():
    skies.add(Sky())
    bird.add(Bird())
    add_pipe(important_coords[1], randint(300, 700))
    add_pipe(important_coords[2], randint(300, 700))
    add_pipe(important_coords[3], randint(300, 700))
    bases.add(Base(0))
    bases.add(Base(important_coords[0]))

def add_pipe(x, y):
    global pipes, pipe_gap
    pipes.add(Pipe(x, y - pipe_gap, 1))
    pipes.add(Pipe(x, y, -1))

# function loops
def update_sprites():
    skies.update()
    bird.update()
    pipes.update()
    bases.update()
    skies.draw(screen)
    bird.draw(screen)
    pipes.draw(screen)
    bases.draw(screen)

# initiating variables
pygame.init()
pygame_icon = pygame.image.load('flappy-bird-assets-master/favicon.ico')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Flappy Bird')
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# variables
scaling = 2
pipe_gap = 200
frame_up_to_60 = 0
important_coords = [576, 864, 1152, 1440]
gravity = 0.25

skies = pygame.sprite.Group()
bases = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = pygame.sprite.GroupSingle()
add_sprites()

# game loop
mode = "main"
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # important functions / variables
    update_sprites()

    frame_up_to_60 += 1
    if frame_up_to_60 > 60:
        frame_up_to_60 = 0

    pygame.display.flip()
    clock.tick(60)