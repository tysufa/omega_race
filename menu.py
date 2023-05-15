import pygame
from text import Text
from constantes import *

pygame.init()


class Menu:
    def __init__(self, window):
        self.window = window

        self.title = Text("OMEGA RACE", 20, SIZE[0]//2, SIZE[1]//2, "blue")
        self.title.rect.center = SIZE[0]//2, 100

        self.jouer = Text("Jouer", 20, SIZE[0] // 2, SIZE[1] // 2, "blue")
        self.jouer.rect.center = SIZE[0] // 2, 200

        self.boutique = Text("boutique", 20, SIZE[0] // 2, SIZE[1] // 2, "blue")
        self.boutique.rect.center = SIZE[0] // 2, 300

        self.option = Text("options", 20, SIZE[0] // 2, SIZE[1] // 2, "blue")
        self.option.rect.center = SIZE[0] // 2, 400

        self.text_group = pygame.sprite.Group(self.title, self.jouer, self.boutique, self.option)

        self.over = ["white", "white", "white"]

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        pygame.mixer.music.load(MENU_MUSIC)

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

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

    def menu_loop(self):
        continuer = True
        while continuer:
            if pygame.key.get_mods()[pygame.K_ESCAPE]:
                continuer = False

            self.draw()
            pygame.display.flip()
