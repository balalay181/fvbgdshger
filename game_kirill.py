import pygame
import random
import sys
import os
from os import path
from pygame.locals import *


img_dir = path.join(path.dirname(__file__), 'img')
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space War')

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Space War"]

    fon = pygame.transform.scale(load_image('start.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Impact', 100)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 80
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)

start_screen()

rows = 5
cols = 5
alien_cooldown = 250
alien_lastshot = pygame.time.get_ticks()

red = (255, 0, 0)
green = (0, 255, 0)

b = pygame.image.load("data/bg.png")


def draw_b():
    screen.blit(b, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class SpaceShip(pygame.sprite.Sprite):  # корабль
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_r = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):  # движение
        speed = 5
        cooldown = 600
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:  # стрельба
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))  # начальная шкала
        if self.health_r > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_r / self.health_start)), 15))  # зеленая шкала


class Bullet(pygame.sprite.Sprite):  # пули корабля
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/bullet.png')
        self.time = 1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()


class Aliens(pygame.sprite.Sprite):  # иноприлетенцы
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/alien' + str(random.randint(1, 5)) + '.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_c = 0
        self.move_d = 1

    def update(self):
        self.rect.x += self.move_d
        self.move_c += 1
        if abs(self.move_c) > 75:
            self.move_d *= -1
            self.move_c *= self.move_d


class AliensBullet(pygame.sprite.Sprite):  # пули иноприлитенцев
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/alien_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False):  # хп корабля
            self.kill()
            spaceship.health_r -= 1
            if spaceship.health_r == 0:
                intro_text = ["Вы проиграли!",
                              "Перезайдите чтобы",
                              "сыграть снова"]

                fon = pygame.transform.scale(load_image('bg.png'),
                                             (screen_width, screen_height))
                screen.blit(fon, (0, 0))
                font = pygame.font.SysFont('Impact', 50)
                text_coord = 150
                for line in intro_text:
                    string_rendered = font.render(line, 1, pygame.Color('yellow'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 5
                    intro_rect.top = text_coord
                    intro_rect.x = 80
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                terminate()
                    pygame.display.flip()
                    clock.tick(fps)


spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
boom_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

def create_aliens():  # создание иноприлетенцов
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()

spaceship = SpaceShip(int(screen_width / 2), screen_height - 100, 3)  # создание корабля
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)
    draw_b()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                terminate()

    time_now = pygame.time.get_ticks()

    if time_now - alien_lastshot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = AliensBullet(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now


    spaceship.update()
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    boom_group.update()
    all_sprites.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    boom_group.draw(screen)
    all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()