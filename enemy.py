import pygame
import random
import math
from pygame.locals import *


class Enemy01: # bullet takers, they cannot shoot but can swarm the player as their speed in only a fraction les than players and they have auto follow system
    def __init__(self, speed=2):
        if speed <= 2:
            speed = 2
        self.speed = speed
        self.y = 0
        self.x = 0
        self.health = 200
        y_base = random.randint(0, 1)
        x_base = random.randint(0, 1)
        if y_base == 0 :
            self.y = random.randint(-100, -10)
        else :
            self.y = random.randint(700, 800)
        if x_base == 0 :
            self.x = random.randint(-100, -10)
        else :
            self.x = random.randint(700, 800)

        self.image = pygame.image.load('assets/enemy_01.png')
        self.base = pygame.Rect(self.x, self.y, 18, 18)
        self.surface = pygame.Surface((18, 32), SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.angle = 0

    def damage_taken(self, damage):
        self.health -= damage

    def move(self, x, y):
        if self.health > 0:
            difx = x - self.x
            dify = y - self.y
            a = math.sqrt(difx ** 2 + dify ** 2)
            self.angle = (math.degrees(math.acos(difx / a)) + 90) * (-1)
            if dify < 0 :
                self.angle = math.degrees(math.acos(difx / a)) - 90

            movement_x = difx / a * self.speed
            movement_y = dify / a * self.speed
            self.x += movement_x
            self.y += movement_y
            self.base.x = self.x
            self.base.y = self.y

            temp_surface = pygame.transform.rotate(self.surface, self.angle)
            return temp_surface, self.base


class Enemy02:
    def __init__(self, speed=1):
        if speed <= 1:
            speed = 1
        self.speed = speed
        self.x = 0
        self.y = 0
        self.health = 150
        y_base = random.randint(0, 1)
        x_base = random.randint(0, 1)
        if y_base == 0 :
            self.y = random.randint(-100, -10)
        else :
            self.y = random.randint(700, 800)
        if x_base == 0 :
            self.x = random.randint(-100, -10)
        else :
            self.x = random.randint(700, 800)
        self.image = pygame.image.load('assets/enemy_02.png')
        self.base = pygame.Rect(self.x, self.y, 24, 24)
        self.surface = pygame.Surface((32, 24), SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.angle = 0

    def damage_taken(self, damage):
        self.health -= damage