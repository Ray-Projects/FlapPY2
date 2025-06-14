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
        self.rect.x -= 2

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

        self.rect.x -= 2

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
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/yellowbird-midflap.png").convert_alpha()
        tmp0 = self.image.width * scaling
        tmp1 = self.image.height * scaling
        self.image = pygame.transform.scale(self.image, (tmp0, tmp1))


# functions
def add_sprites():
    skies.add(Sky())
    bases.add(Base(0))
    bases.add(Base(important_coords[0]))

    add_pipe(important_coords[0], randint(300, 700))
    add_pipe(important_coords[1], randint(300, 700))
    add_pipe(important_coords[2], randint(300, 700))

def add_pipe(x, y):
    global pipes, pipe_gap
    pipes.add(Pipe(x, y - pipe_gap, 1))
    pipes.add(Pipe(x, y, -1))

def update_sprites(type):
    if type == "skies":
        skies.update()
        skies.draw(screen)
    elif type == "bird":
        bird.update()
        bird.draw(screen)
    elif type == "pipes":
        pipes.update()
        pipes.draw(screen)
    elif type == "bases":
        bases.update()
        bases.draw(screen)




# function loops
def main():
    update_sprites("skies")
    update_sprites("bird")
    update_sprites("pipes")
    update_sprites("bases")

def title():
    update_sprites("skies")
    update_sprites("bird")
    update_sprites("pipes")
    update_sprites("bases")

def dead():
    update_sprites("skies")
    update_sprites("bird")
    update_sprites("pipes")
    update_sprites("bases")

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
    if mode == "main":
        main()
    elif mode == "title":
        title()
    elif mode == "dead":
        dead()

    frame_up_to_60 += 1
    if frame_up_to_60 > 60:
        frame_up_to_60 = 0

    pygame.display.flip()
    clock.tick(60)