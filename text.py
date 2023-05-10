import pygame

pygame.init()


class Text(pygame.sprite.Sprite):
    def __init__(self, font, text, size, x, y, color):
        super().__init__()
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.color = color

        self.font = pygame.font.SysFont(font, size)
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(topright=(self.x, self.y))

    def change_text(self, text):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(topright=(self.x, self.y))