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
        self.image.set_alpha(0)
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
            jump_down = True
        else:
            jump_down = False

    def move(self):
        global gravity, max_fall_speed

        self.acceleration += gravity
        self.rect.y += self.acceleration
        if self.rect.y < 0 - self.rect.height:
            self.rect.y = 0 - self.rect.height

        if mode == "main":
            if self.acceleration > max_fall_speed:
                self.acceleration = max_fall_speed
        elif mode == "dead":
            if self.acceleration > dead_max_fall_speed:
                self.acceleration = dead_max_fall_speed

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
        global mode, score_val, touching_pipe_gaps, bases, pipes, pipe_gaps

        if self.rect.center[1] > 790:
            mode = "dead"
        if pygame.sprite.spritecollide(self, pipes, False, pygame.sprite.collide_rect):
            self.mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.spritecollide(self, pipes, False, pygame.sprite.collide_mask):
                mode = "dead"

        if pygame.sprite.spritecollide(self, pipe_gaps, False, pygame.sprite.collide_rect):
            if not touching_pipe_gaps:
                score_val += 1
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

class Score(pygame.sprite.Sprite):
    def __init__(self, number, digit_place, x, y, centered):
        pygame.sprite.Sprite.__init__(self)

        self.number = number
        self.digit_place = digit_place
        self.original_x = x
        self.original_y = y
        self.centered = centered

        self.zero = pygame.image.load("flappy-bird-assets-master/sprites/0.png")
        self.one = pygame.image.load("flappy-bird-assets-master/sprites/1.png")
        self.two = pygame.image.load("flappy-bird-assets-master/sprites/2.png")
        self.three = pygame.image.load("flappy-bird-assets-master/sprites/3.png")
        self.four = pygame.image.load("flappy-bird-assets-master/sprites/4.png")
        self.five = pygame.image.load("flappy-bird-assets-master/sprites/5.png")
        self.six = pygame.image.load("flappy-bird-assets-master/sprites/6.png")
        self.seven = pygame.image.load("flappy-bird-assets-master/sprites/7.png")
        self.eight = pygame.image.load("flappy-bird-assets-master/sprites/8.png")
        self.nine = pygame.image.load("flappy-bird-assets-master/sprites/9.png")

        tmp0 = self.zero.width * scaling # all of them except for 1 are 24 pixels wide, 1 is 16 wide.
        tmp1 = self.zero.height * scaling # all of them are 36 pixels tall
        self.zero = pygame.transform.scale(self.zero, (tmp0, tmp1))
        self.two = pygame.transform.scale(self.two, (tmp0, tmp1))
        self.three = pygame.transform.scale(self.three, (tmp0, tmp1))
        self.four = pygame.transform.scale(self.four, (tmp0, tmp1))
        self.five = pygame.transform.scale(self.five, (tmp0, tmp1))
        self.six = pygame.transform.scale(self.six, (tmp0, tmp1))
        self.seven = pygame.transform.scale(self.seven, (tmp0, tmp1))
        self.eight = pygame.transform.scale(self.eight, (tmp0, tmp1))
        self.nine = pygame.transform.scale(self.nine, (tmp0, tmp1))
        tmp0 = self.one.width * scaling # making sure to change tmp0 before scaling one
        self.one = pygame.transform.scale(self.one, (tmp0, tmp1))

        self.value = [self.zero, self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight, self.nine]
        self.index = int(str(self.number)[self.digit_place])
        self.image = self.value[self.index]

        self.rect = self.image.get_rect(topleft=(x, y))

    def render(self, orig_x, orig_y, centered):
        self.rect.x, self.rect.y = orig_x, orig_y
        self.index = int(str(self.number)[self.digit_place])
        self.image = self.value[self.index]

        for index, index_value in enumerate(str(self.number)):
            if index == self.digit_place:
                if not centered:
                    break

            if index_value == "1":
                self.rect.x += self.one.width + 4
            else:
                self.rect.x += self.zero.width + 4

            if index == 4:
                self.rect.x += self.image.width
                new_x = self.original_x - ((self.rect.x - self.original_x) / 2)
                self.render(new_x, self.original_y, False)

    def update(self, number):
        self.number = number
        self.render(self.original_x, self.original_y, self.centered)

class GameOver(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)

        self.type = type
        if self.type == "gameover":
            self.image = pygame.image.load("flappy-bird-assets-master/sprites/gameover.png")
            tmp0 = self.image.width * scaling
            tmp1 = self.image.height * scaling
            self.image = pygame.transform.scale(self.image, (tmp0, tmp1))
            self.starting_y = 0
            self.rect = self.image.get_rect(midtop=(288, self.starting_y))

        elif self.type == "restart":
            self.image = pygame.image.load("flappy-bird-assets-master/sprites/restart.png")
            tmp0 = self.image.width * scaling
            tmp1 = self.image.height * scaling
            self.image = pygame.transform.scale(self.image, (tmp0, tmp1))
            self.starting_y = 400
            self.rect = self.image.get_rect(midtop=(288, self.starting_y))

        self.image.set_alpha(0)
        self.most_recent_event = 0

    def input(self, events):
        global mode, jump_down, game_over_index

        if self.type == "restart":
            for event in events:
                if game_over_index > 50 and self.rect.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.most_recent_event = "buttonclicked"

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.most_recent_event == "buttonclicked":
                        self.most_recent_event = "buttonreleased"
                        print("\n-------------------------\n")
                        mode = "main"
                        delete_sprites()
                        set_variables_to_default()
                        add_sprites()
                        jump_down = True  # stops jumping at the start of the game

    def animate(self):
        global game_over_index, game_over_opacity_index

        self.image.set_alpha(game_over_opacity_index)
        self.rect.y = self.starting_y + game_over_index

        game_over_index += 4
        if game_over_index > 100:
            game_over_index = 100

        game_over_opacity_index += 20
        if game_over_opacity_index > 255:
            game_over_opacity_index = 255

        if self.most_recent_event == "buttonclicked":
            self.rect.y += 10

    def update(self, events):
        if mode == "dead":
            self.input(events)
            self.animate()

# functions
def add_sprites():
    skies.add(Sky())
    add_pipe(important_coords[2], random.randint(300, 700))
    add_pipe(important_coords[4], random.randint(300, 700))
    add_pipe(important_coords[6], random.randint(300, 700))
    bird.add(Bird())
    bases.add(Base(0))
    bases.add(Base(important_coords[0]))

    tmp0 = 12345
    tmp1 = 288
    tmp2 = 0
    tmp3 = True
    score.add(Score(tmp0, 0, tmp1, tmp2, tmp3))
    score.add(Score(tmp0, 1, tmp1, tmp2, tmp3))
    score.add(Score(tmp0, 2, tmp1, tmp2, tmp3))
    score.add(Score(tmp0, 3, tmp1, tmp2, tmp3))
    score.add(Score(tmp0, 4, tmp1, tmp2, tmp3))

    game_over.add(GameOver("gameover"))
    game_over.add(GameOver("restart"))

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
    game_over.empty()

def set_variables_to_default():
    global frame_up_to_60, jump_down, frame_counter, main_running_time, flash_index, game_over_index, game_over_opacity_index, score_val, old_score_val, touching_pipe_gaps

    frame_up_to_60 = 0
    jump_down = False
    frame_counter = 0
    main_running_time = 0
    flash_index = 0
    game_over_index = 0
    game_over_opacity_index = -200
    score_val = 0
    old_score_val = -1
    touching_pipe_gaps = False

# loop functions
def update_sprites():
    skies.update()
    pipes.update()
    pipe_gaps.update()
    bird.update()
    bases.update()
    score.update(12345)
    game_over.update(events)

    skies.draw(screen)
    pipes.draw(screen)
    pipe_gaps.draw(screen)
    bird.draw(screen)
    bases.draw(screen)
    score.draw(screen)
    game_over.draw(screen)
    death_flash()

def death_flash():
    global flash_index, mode

    if mode == "dead":
        translucent = pygame.Surface((576, 1024))
        translucent.set_alpha(255 - flash_index)
        translucent.fill((223, 217, 150))
        screen.blit(translucent, (0, 0))
        flash_index += 12

# initiating variables
pygame.init()
pygame_icon = pygame.image.load('flappy-bird-assets-master/favicon.ico')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Flappy Bird')
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
important_coords = [576, 768, 960, 1152, 1344, 1536, 1728]

# config variables
scaling = 2
pipe_distance = 180
gravity = 0.8
jump_height = 12
max_fall_speed = 10
dead_max_fall_speed = 20
rotate_speed = 8

# default variables
frame_up_to_60 = 0
jump_down = False
frame_counter = 0
main_running_time = 0
flash_index = 0
game_over_index = 0
game_over_opacity_index = -200
score_val = 0
old_score_val = -1
touching_pipe_gaps = False

# setup
skies = pygame.sprite.Group()
bases = pygame.sprite.Group()
pipes = pygame.sprite.Group()
pipe_gaps = pygame.sprite.Group()
bird = pygame.sprite.GroupSingle()
score = pygame.sprite.Group()
game_over = pygame.sprite.Group()
add_sprites()

# game loop
mode = "main"
while True:
    # check for events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # important functions / variables
    update_sprites()

    frame_up_to_60 += 1
    if frame_up_to_60 > 60:
        frame_up_to_60 = 0
    frame_counter += 1
    if mode == "main":
        main_running_time += 1

    pygame.display.flip()
    clock.tick(60)