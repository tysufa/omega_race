import pygame
from text import Text
from constantes import *

pygame.init()


class Menu:
    def __init__(self, window):
        self.window = window

        self.title = Text(FONT, "OMEGA RACE", 20, WINDOW_W//2, WINDOW_H//2, "blue")
        self.title.rect.center = WINDOW_W//2, 100

        self.jouer = Text(FONT, "Jouer", 20, WINDOW_W // 2, WINDOW_H // 2, "blue")
        self.jouer.rect.center = WINDOW_W // 2, 200

        self.boutique = Text(FONT, "boutique", 20, WINDOW_W // 2, WINDOW_H // 2, "blue")
        self.boutique.rect.center = WINDOW_W // 2, 300

        self.option = Text(FONT, "options", 20, WINDOW_W // 2, WINDOW_H // 2, "blue")
        self.option.rect.center = WINDOW_W // 2, 400

        self.text_group = pygame.sprite.Group(self.title, self.jouer, self.boutique, self.option)

        self.over = ["white", "white", "white"]

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

    def draw(self):
        pygame.draw.rect(self.window, self.over[0], self.jouer.rect)
        pygame.draw.rect(self.window, self.over[1], self.boutique.rect)
        pygame.draw.rect(self.window, self.over[2], self.option.rect)
        self.text_group.draw(self.window)

    def menu_actions(self):
        mouse_events = pygame.mouse.get_pressed()
        self.over = ["white", "white", "white"]

        if self.jouer.rect.collidepoint(pygame.mouse.get_pos()):
            self.over[0] = "red"
            if mouse_events[0]:
                self.select_sound.set_volume(0.15)
                self.select_sound.play()
                return True

        elif self.boutique.rect.collidepoint(pygame.mouse.get_pos()):
            self.over[1] = "red"

        elif self.option.rect.collidepoint(pygame.mouse.get_pos()):
            self.over[2] = "red"