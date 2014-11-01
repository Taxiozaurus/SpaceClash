import pygame
import math
from pygame.locals import *


class Player:
    def __init__(self, speed=3):
        self.image = pygame.image.load('assets/player.png')
        self.fire = pygame.image.load('assets/fire.png')
        self.base = pygame.Rect(0, 0, 38, 38)
        self.surface = pygame.Surface((38, 50), SRCALPHA)
        self.surface.blit(self.image, self.base)
        self.lives = 5
        self.health = 100
        self.shield = 0
        self.angle = 0
        self.speed = speed

    def re_draw(self, flying=False):
        self.surface = pygame.Surface((38, 50), SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        if flying:
            self.surface.blit(self.fire, (0, 38))

    def reset(self, full=False):
        self.health = 100
        self.shield = 0
        if full:
            self.lives = 5

    def move_up(self):
        if self.base.centery >= 24 :
            self.base.centery -= self.speed

    def move_down(self):
        if self.base.centery <= 556 :
            self.base.centery += self.speed

    def move_left(self):
        if self.base.centerx >= 24 :
            self.base.centerx -= self.speed

    def move_right(self):
        if self.base.centerx <= 556 :
            self.base.centerx += self.speed

    def damage_taken(self, dmg):
        if self.shield > 0 :
            self.shield -= dmg
        elif self.health > 0 :
            self.health -= dmg

        if self.shield < 0:
            self.health += self.shield # if shield becomes negative, the extra damage it took will be moved onto health
            self.shield = 0

    def player_collision(self, powers, enemy):
        power = -1
        for i in range(0, len(powers)):
            if self.base.colliderect(powers[i].base):
                power = i
                break
        if power >= 0 :
            if powers[power].name == "health" and self.health < 100:
                self.health += 20
                powers.pop(power)
                if self.health > 100:
                    self.health = 100
            elif powers[power].name == "shield" and self.shield < 200:
                self.shield += 20
                powers.pop(power)
                if self.shield > 250:
                    self.shield = 250
            elif powers[power].name == "life" :
                self.lives += 1
                powers.pop(power)

        bad = -1
        for unit in enemy :
            if self.base.colliderect(unit.base) :
                bad = 1
                break

        if bad >= 0:
            self.damage_taken(1)

    def render(self, mousex=0, mousey=0):
        difx = mousex - self.base.centerx
        dify = mousey - self.base.centery
        if (difx < -1 or difx > 1) and (dify < -1 or dify > 1):
            a = math.sqrt(difx ** 2 + dify ** 2)
            self.angle = (math.degrees(math.acos(difx / a)) + 90) * (-1)
            if dify < 0 :
                self.angle = math.degrees(math.acos(difx / a)) - 90
        temp_surface = pygame.transform.rotate(self.surface, self.angle)
        temp_base = temp_surface.get_rect()
        temp_base.center = self.base.center
        return temp_surface, temp_base