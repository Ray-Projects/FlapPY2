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
        self.rect = self.image.get_rect(topleft=(x, 0))

    def move(self):
        if frame_up_to_60 % 2 == 0:
            self.rect.x -= 1

        if self.rect.x <= -576:
            self.rect.x = 576

    def update(self):
        self.move()

# functions
def add_sprites():
    skies.add(Sky(0))
    skies.add(Sky(576))

def main():
    skies.update()
    skies.draw(screen)


# initiating variables
pygame.init()
screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# variables
scaling = 2
frame_up_to_60 = 0

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

    # important functions / variables
    if running:
        main()

    frame_up_to_60 += 1
    if frame_up_to_60 > 60:
        frame_up_to_60 = 0

    pygame.display.flip()
    clock.tick(60)