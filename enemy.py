import pygame
import random
import math
from pygame.locals import *


class Enemy01: # bullet takers, they cannot shoot but can swarm the player as their speed in only a fraction les than players and they have auto follow system
    def __init__(self, speed=2):
        self.name = "swarmer"
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
        self.name = "fighter"
        self.cooldown = 20
        if speed <= 1:
            speed = 1
        self.speed = speed
        self.x = 0
        self.y = 0
        self.health = 300
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
        self.wp = [(50, 50), (300, 50), (550, 50), (50, 300), (300, 300), (550, 300), (50, 550), (300, 550), (550, 550)] # this one goes in between fixed points on the screen while shooting the player
        self.count = 0
        self.dir = 0

    def damage_taken(self, damage):
        self.health -= damage

    def move(self, x, y):
        self.cooldown -= 1
        self.count -= 1
        if self.count <= 1:
            self.count = 50
            self.dir = random.randint(0, 8)
        difx = self.wp[self.dir][0] - self.x
        dify = self.wp[self.dir][1] - self.y
        a = math.sqrt(difx ** 2 + dify ** 2)

        difx2 = x - self.x
        dify2 = y - self.y
        a2 = math.sqrt(difx2 ** 2 + dify2 ** 2)
        self.angle = (math.degrees(math.acos(difx2 / a2)) + 90) * (-1)
        if dify2 < 0 :
            self.angle = math.degrees(math.acos(difx2 / a2)) - 90

        mov_x = difx / a * self.speed
        mov_y = dify / a * self.speed
        self.x += mov_x
        self.y += mov_y
        self.base.x = self.x
        self.base.y = self.y

        temp_surface = pygame.transform.rotate(self.surface, self.angle)
        return temp_surface, self.base


class Boss01:
    def __init__(self, speed=1):
        self.name = "Boss Fighter"
        self.speed = speed
        self.cooldown = 30
        self.x = 284
        self.y = -100
        self.base = pygame.Rect(self.x, self.y, 64, 64)
        self.surface = pygame.Surface((64, 64), SRCALPHA)
        self.image = pygame.image.load('assets/boss_01.png')
        self.surface.blit(self.image, (0, 0))
        self.health = 10000
        self.count = 0
        self.dir = 0
        self.wp = [(50, 150), (284, 60), (114, 150)]
        self.bullets = []

    def calculate(self):
        self.bullets = []
        for i in range(0, 45):
            ta = i * 8
            self.bullets.append((self.base.centerx, self.base.centery, self.base.centerx + math.cos(ta), self.base.centery + math.sin(ta)))
        return self.bullets

    def damage_taken(self, dmg):
        self.health -= dmg

    def move(self, x, y):
        self.cooldown -= 1
        self.count -= 1
        if self.count < 1:
            self.count = 50
            self.dir = random.randint(0, 2)
        difx = self.wp[self.dir][0] - self.x
        dify = self.wp[self.dir][1] - self.y
        a = math.sqrt(difx ** 2 + dify ** 2)
        mov_x = difx / a * self.speed
        mov_y = dify / a * self.speed
        self.x += mov_x
        self.y += mov_y
        self.base.x = self.x
        self.base.y = self.y

        return self.surface, self.base