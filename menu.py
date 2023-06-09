import pygame
from text import Text
from constantes import *
import sys
from game import Game

pygame.init()


class Menu:
    def __init__(self):
        self.window = pygame.display.set_mode(SIZE)

        self.music_volume = 100
        self.sound_volume = 100

        self.title = Text("OMEGA RACE", 80, SIZE[0]//2, SIZE[1]//2, "white")
        self.title.rect.center = SIZE[0]//2, 100

        self.jouer = Text("Jouer", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.jouer.rect.center = SIZE[0] // 2, 300

        self.cartes_text = Text("cartes", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.cartes_text.rect.center = SIZE[0] // 2, 400

        self.option_text = Text("options", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.option_text.rect.center = SIZE[0] // 2, 450

        self.music_text = Text("Musique :", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.music_text.rect.center = SIZE[0]//2 - 200, 200

        self.sound_text = Text("Sons :", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.sound_text.rect.center = SIZE[0]//2 - 200, 400

        self.reset_high_score_text = Text("Reset high score", 50, SIZE[0] // 2, SIZE[1] // 2, "#b93535")
        self.reset_high_score_text.rect.center = SIZE[0] // 2, 550

        self.percentage_music_text = Text(str(int(self.music_volume)) + "%", 50, SIZE[0] // 2 + 200 + 70, 200-25, "white")
        self.percentage_sound_text = Text(str(int(self.music_volume)) + "%", 50, SIZE[0] // 2 + 200 + 70, 400-25, "white")

        self.menu_text_group = pygame.sprite.Group(self.title, self.jouer, self.option_text)
        self.option_text_group = pygame.sprite.Group(self.title, self.music_text, self.sound_text, self.percentage_music_text, self.percentage_sound_text, self.reset_high_score_text)

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()

        pygame.mixer.music.load(MENU_MUSIC)
        self.music = "menu"

        self.clock = pygame.time.Clock()

        self.game = Game(self.window, self.clock)

        pygame.mixer.music.play()


    def option(self):
        continuer = True

        music_rod = pygame.rect.Rect(SIZE[0]//2 - 50, 200-25//2, 200, 25)
        music_rod_border = pygame.rect.Rect(SIZE[0]//2 - 50, 200-25//2, 200, 25)
        music_rod.width = self.music_volume*2

        sound_rod = pygame.rect.Rect(SIZE[0]//2 - 50, 400-25//2, 200, 25)
        sound_rod_border = pygame.rect.Rect(SIZE[0]//2 - 50, 400-25//2, 200, 25)
        sound_rod.width = self.sound_volume*2


        while continuer:
            self.window.blit(self.menu_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = False


            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if music_rod_border.collidepoint(mouse_pos):
                    music_rod.width =  mouse_pos[0] - (SIZE[0]//2 - 50)
                    self.music_volume = music_rod.width/200*100
                    pygame.mixer.music.set_volume(self.music_volume/100)
                    self.percentage_music_text.change_text(str(int(self.music_volume)) + "%")

                if sound_rod_border.collidepoint(mouse_pos):
                    sound_rod.width =  mouse_pos[0] - (SIZE[0]//2 - 50)
                    self.sound_volume = sound_rod.width/200*100

                    self.game.player.set_sound(self.sound_volume/100)


                    self.select_sound.set_volume(self.sound_volume/100)
                    self.percentage_sound_text.change_text(str(int(self.sound_volume)) + "%")

                if self.reset_high_score_text.rect.collidepoint(pygame.mouse.get_pos()):
                    self.select_sound.play()
                    with open("score.txt", "w") as fichier:
                        fichier.write("0")
                    self.game.high_score = 0

            self.reset_high_score_text.color = "#b93535"
            self.reset_high_score_text.change_text("Reset high score", False)

            if self.reset_high_score_text.rect.collidepoint(pygame.mouse.get_pos()):
                self.reset_high_score_text.color = "#ff2b2b"
                self.reset_high_score_text.change_text("Reset high score", False)
  

            pygame.draw.rect(self.window, "#5a5a5a", music_rod, 0, 4)
            pygame.draw.rect(self.window, "white", music_rod_border, 3)

            pygame.draw.rect(self.window, "#5a5a5a", sound_rod, 0, 4)
            pygame.draw.rect(self.window, "white", sound_rod_border, 3)

            self.option_text_group.draw(self.window)
            pygame.display.flip()

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pressed = True


            self.jouer.color = "white"
            self.jouer.change_text("Jouer", False)
            # self.cartes_text.color = "white"
            # self.cartes_text.change_text("Cartes", False)
            self.option_text.color = "white"
            self.option_text.change_text("Options", False)


            if self.jouer.rect.collidepoint(pygame.mouse.get_pos()):
                self.jouer.color = "orange"
                self.jouer.change_text("Jouer", False)
                if pressed:
                    if self.music == "menu":
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load(GAME_MUSIC)
                        pygame.mixer.music.play(loops=-1, fade_ms=1000)
                        self.music = "jeu"

                    self.select_sound.play()
                    self.game.reset_game()
                    self.game.run()

            elif self.option_text.rect.collidepoint(pygame.mouse.get_pos()):
                self.option_text.color = "orange"
                self.option_text.change_text("Options", False)
                if pressed:
                    self.select_sound.play()
                    self.option()

            """        
            elif self.cartes_text.rect.collidepoint(pygame.mouse.get_pos()):
                self.cartes_text.color = "orange"
                self.cartes_text.change_text("Cartes", False)
                if pressed:
                    self.select_sound.play()
            """



            self.menu_text_group.draw(self.window)
            pygame.display.update()


            self.clock.tick(60)


