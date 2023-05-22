import pygame
from text import Text
from constantes import *
import sys

pygame.init()


class Menu:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.title = Text("OMEGA RACE", 40, SIZE[0]//2, SIZE[1]//2, "white")
        self.title.rect.center = SIZE[0]//2, 100

        self.jouer = Text("Jouer", 40, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.jouer.rect.center = SIZE[0] // 2, 200

        self.boutique = Text("boutique", 40, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.boutique.rect.center = SIZE[0] // 2, 300

        self.option = Text("options", 40, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.option.rect.center = SIZE[0] // 2, 400

        self.text_group = pygame.sprite.Group(self.title, self.jouer, self.boutique, self.option)

        self.over = ["white", "white", "white"]

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()

        pygame.mixer.music.load(MENU_MUSIC)

    def menu_loop(self):
        continuer = True

        while continuer:
            self.window.blit(self.menu_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = False
            
            self.text_group.draw(self.window)
            pygame.display.update()


            self.clock.tick(60)


class GameOver:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.jouer = Text("Jouer", 40, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.jouer.rect.center = SIZE[0] // 2, SIZE[0] // 2

        self.boutique = Text("boutique", 40, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.boutique.rect.center = SIZE[0] // 2 + 100, SIZE[0] // 2

        self.text_group = pygame.sprite.Group(self.jouer, self.boutique)

        self.over = ["white", "white", "white"]

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()

        pygame.mixer.music.load(MENU_MUSIC)

    def game_over_loop(self):
        continuer = True

        while continuer:
            self.window.blit(self.menu_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = False
            
            self.text_group.draw(self.window)
            pygame.display.update()


            self.clock.tick(60)
