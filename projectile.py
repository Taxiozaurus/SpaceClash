import math
import pygame


class Projectile:
    def __init__(self, x1, y1, x2, y2, speed=6): # x1,y1 are starting point, x2y2 are aiming point
        difx = x2 - x1
        dify = y2 - y1
        a = math.sqrt(difx ** 2 + dify ** 2)

        self.angle = (math.degrees(math.acos(difx / a)) + 90) * (-1)
        if dify < 0 :
            self.angle = math.degrees(math.acos(difx / a)) - 90 # return angular direction for the sprite in degrees
        self.speed = speed
        self.position = [x1, y1]
        self.direction = [difx / a * speed, dify / a * speed]
        self.base = pygame.Surface((2, 2))
        self.base.fill((255, 255, 0))
        self.surface = pygame.transform.rotate(self.base, self.angle)

    def move(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
        return self.render() # this way you need to call only "move" to get both updated position and get the right projectile

    def render(self):
        base_rect = pygame.Rect(int(self.position[0]), int(self.position[1]), 2, 2)
        return base_rect, self.surface