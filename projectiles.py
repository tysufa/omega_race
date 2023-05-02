import pygame
from math import sin, cos, radians


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x, self.y = x, y
        self.direction = direction
        self.image = pygame.surface.Surface((10, 5))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(self.x, self.y))


        self.velocity = cos(radians(self.direction)) * 12, sin(radians(self.direction)) * 12


    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]
