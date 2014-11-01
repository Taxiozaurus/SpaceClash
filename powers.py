import pygame
from pygame.locals import *


class Health:
    def __init__(self, x, y):
        self.name = "health"
        self.image = pygame.image.load('assets/health.png')
        self.surface = pygame.Surface((24, 24), SRCALPHA)
        self.base = pygame.Rect(x, y, 24, 24)
        self.surface.blit(self.image, (0, 0))


class Shield:
    def __init__(self, x, y):
        self.name = "shield"
        self.image = pygame.image.load('assets/shield.png')
        self.surface = pygame.Surface((24, 24), SRCALPHA)
        self.base = pygame.Rect(x, y, 24, 24)
        self.surface.blit(self.image, (0, 0))


class Life:
    def __init__(self, x, y):
        self.name = "life"
        self.image = pygame.image.load('assets/life.png')
        self.surface = pygame.Surface((24, 24), SRCALPHA)
        self.base = pygame.Rect(x, y, 24, 24)
        self.surface.blit(self.image, (0, 0))


class Placeholder:
    def __init__(self, image, rect, time=20):
        self.image = image
        self.rect = rect
        self.time = time