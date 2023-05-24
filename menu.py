import pygame
from text import Text
from constantes import *
import sys
from game import Game

pygame.init()


class Menu:
    def __init__(self):
        self.window = pygame.display.set_mode(SIZE)

        self.title = Text("OMEGA RACE", 80, SIZE[0]//2, SIZE[1]//2, "white")
        self.title.rect.center = SIZE[0]//2, 100

        self.jouer = Text("Jouer", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.jouer.rect.center = SIZE[0] // 2, 300

        self.cartes = Text("cartes", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.cartes.rect.center = SIZE[0] // 2, 400

        self.option = Text("options", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.option.rect.center = SIZE[0] // 2, 500

        self.text_group = pygame.sprite.Group(self.title, self.jouer, self.cartes, self.option)

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()

        pygame.mixer.music.load(MENU_MUSIC)

        self.clock = pygame.time.Clock()

        self.game = Game(self.window, self.clock)

    def run(self):
        continuer = True
        pressed = False
        while continuer:
            self.window.blit(self.menu_image, (0, 0))
            pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = False
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pressed = True


            self.jouer.color = "white"
            self.jouer.change_text("Jouer", False)
            self.cartes.color = "white"
            self.cartes.change_text("Cartes", False)
            self.option.color = "white"
            self.option.change_text("Options", False)


            if self.jouer.rect.collidepoint(pygame.mouse.get_pos()):
                self.jouer.color = "orange"
                self.jouer.change_text("Jouer", False)
                if pressed:
                    self.select_sound.play()
                    self.game.reset_game()
                    self.game.run()

            elif self.cartes.rect.collidepoint(pygame.mouse.get_pos()):
                self.cartes.color = "orange"
                self.cartes.change_text("Cartes", False)
                if pressed:
                    self.select_sound.play()
                    
            elif self.option.rect.collidepoint(pygame.mouse.get_pos()):
                self.option.color = "orange"
                self.option.change_text("Options", False)
                if pressed:
                    self.select_sound.play()
                
            
            self.text_group.draw(self.window)
            pygame.display.update()


            self.clock.tick(60)


