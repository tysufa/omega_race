import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, length, height, width, color):
        super().__init__()
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.width = width
        self.color = color

        self.image = pygame.surface.Surface((length, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.displayed = False
        self.timer = None

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def show(self):
        self.timer = pygame.time.get_ticks()
        self.displayed = True

    def update(self):
        if self.displayed and self.timer is not None:
            if pygame.time.get_ticks() - self.timer > 180:
                self.displayed = False
