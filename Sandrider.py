import pygame
import random
from pygame.locals import *

Width = 750
Height = 1000


pygame.init()

backimg = pygame.image.load("background.png")
start_backimg = pygame.image.load("start_background.png")

level_skins = {
    1: [pygame.image.load("fakir.png")], 
    2: [pygame.image.load("jeep.png")],
    3: [pygame.image.load("jet.png")]
}
storm_image = pygame.image.load("storm.png")

level_speed_player = {
    1: 6.3,
    2: 8.4,
    3: 10
}

level_speed_storm = {
    1: 9,
    2: 12.7,
    3: 15
}

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Sandrider")
font = pygame.font.SysFont("comicsansms", 35)
font1 = pygame.font.SysFont("comicsansms", 70)
clock = pygame.time.Clock()
ranges = [(55, 70), (170, 185), (285, 300), (400, 415), (515, 530), (630, 645)]

class start_screen:
    @staticmethod
    def draw_start_screen():
        screen.blit(start_backimg, (0, 0))
        start_text = font.render("Sandrider Game", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=(Width // 2, Height // 2 - 100))
        screen.blit(start_text, text_rect)

        level1_button = pygame.Rect(Width // 2 - 100, Height // 2 - 30, 200, 50)
        level2_button = pygame.Rect(Width // 2 - 100, Height // 2 + 30, 200, 50)
        level3_button = pygame.Rect(Width // 2 - 100, Height // 2 + 90, 200, 50)
        Quit_button = pygame.Rect(Width // 2 - 100, Height // 2 + 150, 200, 50)

        pygame.draw.rect(screen, (1, 200, 1), level1_button)
        pygame.draw.rect(screen, (236, 178, 2), level2_button)
        pygame.draw.rect(screen, (215, 0, 0), level3_button)
        pygame.draw.rect(screen, (72, 116, 162), Quit_button)

        level1_text = font.render("Level 1", True, (255, 255, 255))
        level2_text = font.render("Level 2", True, (255, 255, 255))
        level3_text = font.render("Level 3", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        screen.blit(level1_text, level1_text.get_rect(center=level1_button.center))
        screen.blit(level2_text, level2_text.get_rect(center=level2_button.center))
        screen.blit(level3_text, level3_text.get_rect(center=level3_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=Quit_button.center))

        return level1_button, level2_button, level3_button, Quit_button

    @staticmethod
    def startscreen(clock):
        current_level = 1
        running = True
        show_start_screen = True

        while show_start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    show_start_screen = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    level1_button, level2_button, level3_button, quit_button = start_screen.draw_start_screen()
                    if level1_button.collidepoint(mouse_pos):
                        current_level = 1
                        show_start_screen = False
                    elif level2_button.collidepoint(mouse_pos):
                        current_level = 2
                        show_start_screen = False
                    elif level3_button.collidepoint(mouse_pos):
                        current_level = 3
                        show_start_screen = False
                    elif quit_button.collidepoint(mouse_pos):
                        show_start_screen = False
                        running = False

            start_screen.draw_start_screen()
            pygame.display.flip()
            clock.tick(60)

        return current_level, running

class Storm:
    def __init__(self, level):
        self.image = storm_image
        self.rect = self.image.get_rect()
        self.rect.x = self.get_random_x_from_ranges(ranges)
        self.rect.y = -self.rect.height
        self.dropyv = level_speed_storm[level]

    @staticmethod
    def get_random_x_from_ranges(ranges):
        chosen_range = random.choice(ranges)
        return random.randint(chosen_range[0], chosen_range[1])

    def move(self):
        self.rect.y += self.dropyv

    def update(self):
        self.move()

class Player:
    def __init__(self, x, y, level):
        self.images = level_skins[level]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = (x * 80) + 100
        self.rect.y = (y * 80) + 100
        self.dropx = self.rect.x
        self.speed = level_speed_player[level]

    def update_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def move(self, dx):
        self.dropx += dx
        if self.dropx < 0:
            self.dropx = 0
        if self.dropx > Width - self.rect.width:
            self.dropx = Width - self.rect.width

    def update(self):
        self.rect.x = int(self.dropx)
        self.update_image()

def display_lives(lives, font):
    lives_text = font.render(f'Leben: {lives}', True, (0, 0, 0))
    screen.blit(lives_text, (Width - 200, 25))

def display_score(score, font):
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (Width - 200, 60))

def display_level(current_level, font):
    level_text = font.render(f'Level: {current_level}', True, (0, 0, 0))
    screen.blit(level_text, (Width - 500, 20))

def display_high_score(high_score, font):
    high_score_text = font.render(f'High Score: {high_score}', True, (0, 0, 0))
    screen.blit(high_score_text, (Width - 500, 95))

lives = 3
score = 0
high_score = 0
running = True
show_start_screen = True

current_level, running = start_screen.startscreen(clock)

player = Player(1, 8.5, current_level)

storms = [Storm(current_level) for _ in range(4)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move(-player.speed)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move(player.speed)
    if keys[pygame.K_SPACE]:
        running = False
        show_start_screen = True 

    player.update()

    for storm in storms:
        storm.update()
        if storm.rect.top > Height:
            storms.remove(storm)
            storms.append(Storm(current_level))
            score += 1
        if player.rect.colliderect(storm.rect):
            lives -= 1
            storms.remove(storm)
            storms.append(Storm(current_level))
            if lives <= 0:
                if score > high_score:
                    high_score = score
                current_level, running = start_screen.startscreen(clock)
                lives = 3
                score = 0
                if running:
                    player = Player(1, 8.5, current_level)
                    storms = [Storm(current_level) for _ in range(4)]
                else:
                    running = False

    screen.fill((0, 0, 0))
    screen.blit(backimg, (0, 0))
    screen.blit(player.image, player.rect)

    for storm in storms:
        screen.blit(storm.image, storm.rect)

    display_lives(lives, font)
    display_score(score, font)
    display_level(current_level, font1)
    display_high_score(high_score, font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()