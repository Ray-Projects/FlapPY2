import pygame
import random
import sys

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
        global mode

        if mode != "dead":
            self.move()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/pipe-green.png").convert_alpha()
        tmp0 = self.image.width * scaling
        tmp1 = self.image.height * scaling
        self.image = pygame.transform.scale(self.image, (tmp0, tmp1))

        if self.position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y))
        elif self.position == -1:
            self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        # moves pipe, and if off the left edge of the screen it goes to the spot of the farthest right pipe (in this case 768),
        # plus the gap between the pipe (in this case 2 1/3's of 576). we also subtract image width to make up for the image subtraction from earlier,
        # preventing the gap between pipes changing.
        global pipes

        self.rect.x -= 3

        if not(self.rect.x <= -self.image.width):
            return
        if self.position == 1:
            add_pipe(important_coords[3] -self.image.width, random.randint(300, 700))
        self.kill()

    def update(self):
        global mode

        if mode != "dead":
            self.move()

class PipeGap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((52 * scaling, pipe_distance))
        self.image.set_alpha(100)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        global pipes

        self.rect.x -= 3

        if self.rect.x <= -self.image.width:
            self.kill()

    def update(self):
        global mode

        if mode != "dead":
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
        self.falltime = 0
        self.angle = 0

        self.touching_base = False

    def input(self):
        global jump_down, jump_height, mode
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or mouse[0]:
            if not jump_down:
                if mode == "main":
                    self.acceleration = - jump_height
                    self.angle = 20
                elif mode == "dead" and frame_counter - main_running_time > 60:
                    print("\n-----------------------\n")
                    mode = "main"
                    delete_sprites()
                    set_variables_to_default()
                    add_sprites()
            jump_down = True
        else:
            jump_down = False

    def move(self):
        global gravity, max_fall_speed

        self.acceleration += gravity
        self.rect.y += self.acceleration
        if self.rect.y < 0 - self.rect.height:
            self.rect.y = 0 - self.rect.height

        if self.acceleration > max_fall_speed:
            self.acceleration = max_fall_speed
        if self.acceleration > 0:
            self.falltime += 1
        else:
            self.falltime = 0

    def animate(self):
        if self.index >= len(self.flap):
            self.index = 0
        self.image = self.flap[int(self.index)]
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def main(self):
        global rotate_speed

        self.index += 0.3
        if self.falltime > 20:
            self.angle -= rotate_speed
        if self.angle < -90:
            self.angle = -90

    def dead(self):
        global frame_counter, main_running_time, rotate_speed

        if frame_counter - main_running_time > 20 and not self.touching_base:
            self.acceleration += 1
            self.angle -= rotate_speed
        else:
            self.acceleration = 0
        if self.angle < -90:
            self.angle = -90

        if self.rect.center[1] > 789:
            self.rect.center = (self.rect.center[0], 790)
            self.touching_base = True
        else:
            self.touching_base = False

    def collide(self):
        global mode, score, touching_pipe_gaps, bases, pipes, pipe_gaps

        if self.rect.center[1] > 790:
            mode = "dead"
        if pygame.sprite.spritecollide(self, pipes, False, pygame.sprite.collide_rect):
            self.mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.spritecollide(self, pipes, False, pygame.sprite.collide_mask):
                mode = "dead"

        if pygame.sprite.spritecollide(self, pipe_gaps, False, pygame.sprite.collide_rect):
            if not touching_pipe_gaps:
                score += 1
            touching_pipe_gaps = True
        else:
            touching_pipe_gaps = False

    def update(self):
        global mode

        self.input()
        self.move()
        self.collide()
        if mode == "main":
            self.main()
        elif mode == "dead":
            self.dead()
        self.animate()

# functions
def add_sprites():
    skies.add(Sky())
    add_pipe(important_coords[2], random.randint(300, 700))
    add_pipe(important_coords[4], random.randint(300, 700))
    add_pipe(important_coords[6], random.randint(300, 700))
    bases.add(Base(0))
    bases.add(Base(important_coords[0]))
    bird.add(Bird())

def add_pipe(x, y):
    global pipes, pipe_distance, pipe_gaps

    pipes.add(Pipe(x, y - pipe_distance, 1))
    pipe_gaps.add(PipeGap(x, y - pipe_distance))
    pipes.add(Pipe(x, y, -1))

def delete_sprites():
    skies.empty()
    pipes.empty()
    pipe_gaps.empty()
    bases.empty()
    bird.remove(Bird())

def set_variables_to_default():
    global frame_up_to_60, jump_down, frame_counter, main_running_time, flash_index, game_over_index, score, old_score, touching_pipe_gaps

    frame_up_to_60 = 0
    jump_down = False
    frame_counter = 0
    main_running_time = 0
    flash_index = 0
    game_over_index = 1
    score = 0
    old_score = -1
    touching_pipe_gaps = False

def update_score():
    global score
    print(f"CURRENT SCORE: {score}")

# loop functions
def update_sprites():
    skies.update()
    pipes.update()
    pipe_gaps.update()
    bird.update()
    bases.update()

    skies.draw(screen)
    pipes.draw(screen)
    pipe_gaps.draw(screen)
    bird.draw(screen)
    bases.draw(screen)
    death_flash()
    game_over()

def death_flash():
    global mode, flash_index

    if mode == "dead":
        translucent = pygame.Surface((576, 1024))
        translucent.set_alpha(255 - flash_index)
        translucent.fill((223, 217, 150))
        screen.blit(translucent, (0, 0))
        flash_index += 12

def game_over():
    global game_over_index
    if mode == "dead":
        game_over = pygame.image.load("flappy-bird-assets-master/sprites/gameover.png")
        tmp0 = game_over.width * scaling
        tmp1 = game_over.height * scaling
        game_over = pygame.transform.scale(game_over, (tmp0, tmp1))
        game_over.set_alpha(game_over_index * 2.55)
        screen.blit(game_over, (288 - (game_over.width / 2), 100 + game_over_index))
        game_over_index += 7
        if game_over_index > 100:
            game_over_index = 100

# initiating variables
pygame.init()
pygame_icon = pygame.image.load('flappy-bird-assets-master/favicon.ico')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Flappy Bird')
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
important_coords = [576, 768, 960, 1152, 1344, 1536, 1728]

# default variables
frame_up_to_60 = 0
jump_down = False
frame_counter = 0
main_running_time = 0
flash_index = 0
game_over_index = 1
score = 0
old_score = -1
touching_pipe_gaps = False

# config variables
scaling = 2
pipe_distance = 180
gravity = 0.8
jump_height = 12
max_fall_speed = 10
rotate_speed = 8

# setup
skies = pygame.sprite.Group()
bases = pygame.sprite.Group()
pipes = pygame.sprite.Group()
pipe_gaps = pygame.sprite.Group()
bird = pygame.sprite.GroupSingle()
add_sprites()

# game loop
mode = "main"
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # important functions / variables
    update_sprites()
    if score != old_score:
        old_score = score
        update_score()

    frame_up_to_60 += 1
    if frame_up_to_60 > 60:
        frame_up_to_60 = 0
    frame_counter += 1
    if mode == "main":
        main_running_time += 1

    pygame.display.flip()
    clock.tick(60)