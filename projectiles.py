import pygame


class Projectiles:
    def __init__(self, x, y, direction, size, window):
        self.x, self.y = x, y
        self.direction = direction
        self.projectile_rect = pygame.rect.Rect(self.x, self.y, 10, 5)

        self.size = size
        self.window = window

    def draw(self):
        pygame.draw.rect(self.window, "red", self.projectile_rect)
