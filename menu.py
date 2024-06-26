import pygame
import os
from text import Text
from constantes import SIZE, MENU_MUSIC, ANIMATION_SPEED, ANIMATION_STARTING_OFFSET
import sys
from game import Game

pygame.init()


class Menu:
    def __init__(self):
        self.window = pygame.display.set_mode(SIZE, pygame.RESIZABLE)

        self.animationStartingOffset = ANIMATION_STARTING_OFFSET
        self.inOptions = False

        # list of all elements initial locations
        self.positions = {
            "title": (self.window.get_width() // 2, self.window.get_height() // 7),
            "jouer": (self.window.get_width() // 2, int(self.window.get_height() / 2.4)),
            "cartes_text": (self.window.get_width() // 2, int(self.window.get_height() / 1.8)),
            "option_text": (self.window.get_width() // 2, int(self.window.get_height() / 1.6)),
            "music_text": (
                self.window.get_width() // 2 - 200 + self.animationStartingOffset,
                int(self.window.get_height() / 3.6),
            ),
            "sound_text": (
                self.window.get_width() // 2 - 200 + self.animationStartingOffset,
                int(self.window.get_height() / 1.8),
            ),
            "reset_high_score_text": (
                self.window.get_width() // 2 + self.animationStartingOffset,
                int(self.window.get_height() / 1.3),
            ),
            "percentage_music_text": (
                self.window.get_width() // 2 + 200 + 70 + self.animationStartingOffset,
                int(self.window.get_height() / 3.6) - 25,
            ),
            "percentage_sound_text": (
                self.window.get_width() // 2 + 200 + 70 + self.animationStartingOffset,
                int(self.window.get_height() / 1.8) - 25,
            ),
            "music_rod": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 3.6) - 25 // 2,
            ),
            "music_rod_border": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 3.6) - 25 // 2,
            ),
            "sound_rod": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 1.85),
            ),
            "sound_rod_border": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 1.85),
            ),
        }

        self.title = Text("OMEGA RACE", 80, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.title.rect.center = self.positions["title"]

        self.jouer = Text("Jouer", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.jouer.rect.center = self.positions["jouer"]

        self.cartes_text = Text("cartes", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.cartes_text.rect.center = self.positions["cartes_text"]

        self.option_text = Text("options", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.option_text.rect.center = self.positions["option_text"]

        self.music_text = Text("Musique :", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.music_text.rect.center = self.positions["music_text"]

        self.music_rod = pygame.rect.Rect(self.positions["music_rod"], (200, 25))
        self.music_rod_border = pygame.rect.Rect(self.positions["music_rod_border"], (200, 25))

        self.sound_text = Text("Sons :", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.sound_text.rect.center = self.positions["sound_text"]

        self.sound_rod = pygame.rect.Rect((self.positions["sound_rod"]), (200, 25))
        self.sound_rod_border = pygame.rect.Rect(self.positions["sound_rod_border"], (200, 25))

        self.reset_high_score_text = Text("Reset high score", 50, SIZE[0] // 2, SIZE[1] // 2, "#b93535")
        self.reset_high_score_text.rect.center = SIZE[0] // 2 + 400, 550

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()

        pygame.mixer.music.load(MENU_MUSIC)
        self.music = "menu"

        self.clock = pygame.time.Clock()

        self.game = Game(self.window, self.clock)

        if not os.path.exists("saves/music_sound_volume.txt"):
            with open("saves/music_sound_volume.txt", "w") as fichier:
                fichier.write("100.0" + "\n" + "100.0")

        with open(
            "saves/music_sound_volume.txt",
        ) as volume_file:
            music_volume = volume_file.readline()
            self.music_volume = float(music_volume)
            pygame.mixer.music.set_volume(self.music_volume / 100)

            self.sound_volume = float(volume_file.readline())

            self.game.player.set_sound(self.sound_volume / 100)

            self.select_sound.set_volume(self.sound_volume / 100)

        # self.percentage_music_text = Text(
        #     str(int(self.music_volume)) + "%", 50, SIZE[0] // 2 + 200 + 70, 200 - 25, "white"
        # )
        self.percentage_music_text = Text(
            str(int(self.music_volume)) + "%",
            50,
            self.positions["percentage_music_text"][0],
            self.positions["percentage_music_text"][1],
            "white",
        )
        self.percentage_sound_text = Text(
            str(int(self.sound_volume)) + "%", 50, SIZE[0] // 2 + 200 + 70, 400 - 25, "white"
        )
        self.menu_text_group = pygame.sprite.Group(self.title, self.jouer, self.option_text)
        self.option_text_group = pygame.sprite.Group(
            self.title,
            self.music_text,
            self.sound_text,
            self.percentage_music_text,
            self.percentage_sound_text,
            self.reset_high_score_text,
        )

        pygame.mixer.music.play()

    def reset_menu_elements_pos(self):
        # reset location every time for the animation
        self.sound_text.rect.center = self.positions["sound_text"]
        self.music_text.rect.center = self.positions["music_text"]
        self.reset_high_score_text.rect.center = self.positions["reset_high_score_text"]
        self.percentage_music_text.x = self.positions["percentage_music_text"][0]
        self.percentage_music_text.change_text(self.percentage_music_text.text)
        self.percentage_sound_text.x = self.positions["percentage_sound_text"][0]
        self.percentage_sound_text.change_text(self.percentage_sound_text.text)

    def menu_elements_animation(self):
        if self.music_text.rect.center[0] > self.positions["music_text"][0] - self.animationStartingOffset:
            self.music_text.rect.x -= ANIMATION_SPEED

        if self.sound_text.rect.center[0] > self.positions["sound_text"][0] - self.animationStartingOffset:
            self.sound_text.rect.x -= ANIMATION_SPEED

        if (
            self.reset_high_score_text.rect.center[0]
            > self.positions["reset_high_score_text"][0] - self.animationStartingOffset
        ):
            self.reset_high_score_text.rect.x -= ANIMATION_SPEED

        if (
            self.percentage_music_text.x
            > self.positions["percentage_music_text"][0] - self.animationStartingOffset
        ):
            self.percentage_music_text.x -= ANIMATION_SPEED
            self.percentage_music_text.change_text(self.percentage_music_text.text)
        if (
            self.percentage_sound_text.x
            > self.positions["percentage_sound_text"][0] - self.animationStartingOffset
        ):
            self.percentage_sound_text.x -= ANIMATION_SPEED
            self.percentage_sound_text.change_text(self.percentage_sound_text.text)

    def option(self):
        self.inOptions = True
        continuer = True
        first_click = True
        clicked_reset = False

        # positions reset for the menu animation
        self.reset_menu_elements_pos()
        self.music_rod = pygame.rect.Rect(self.positions["music_rod"], (200, 25))

        # initial locations
        reset_popup_text = Text("Vous etes sur ?", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        reset_popup_yes_text = Text("Oui", 50, SIZE[0] // 2, SIZE[1] // 2, "white")
        reset_popup_no_text = Text("Non", 50, SIZE[0] // 2, SIZE[1] // 2, "white")

        reset_popup_text.rect.center = SIZE[0] // 2 - 100, 650
        reset_popup_yes_text.rect.center = SIZE[0] // 2, 650
        reset_popup_no_text.rect.center = SIZE[0] // 2, 650

        reset_popup_yes_text.rect.left = reset_popup_text.rect.right + 40
        reset_popup_no_text.rect.left = reset_popup_yes_text.rect.right + 50

        option_text_group = pygame.sprite.Group(reset_popup_text, reset_popup_yes_text, reset_popup_no_text)

        self.music_rod.width = int(self.music_volume * 2)

        self.sound_rod.width = int(self.sound_volume * 2)

        while continuer:
            self.window.blit(self.menu_image, (0, 0))

            # menu apparition animations
            self.menu_elements_animation()

            if self.music_rod.left > self.positions["music_rod"][0] - self.animationStartingOffset:
                self.music_rod.x -= ANIMATION_SPEED

            if (
                self.music_rod_border.left
                > self.positions["music_rod_border"][0] - self.animationStartingOffset
            ):
                self.music_rod_border.x -= ANIMATION_SPEED

            if self.sound_rod.left > self.positions["sound_rod"][0] - self.animationStartingOffset:
                self.sound_rod.x -= ANIMATION_SPEED

            if (
                self.sound_rod_border.left
                > self.positions["sound_rod_border"][0] - self.animationStartingOffset
            ):
                self.sound_rod_border.x -= ANIMATION_SPEED

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = False

                if event.type == pygame.WINDOWRESIZED:
                    self.resizeAssets()

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.music_rod_border.collidepoint(mouse_pos):
                    self.music_rod.width = mouse_pos[0] - (SIZE[0] // 2 - 50)
                    self.music_volume = self.music_rod.width / 200 * 100
                    pygame.mixer.music.set_volume(self.music_volume / 100)
                    self.percentage_music_text.change_text(str(int(self.music_volume)) + "%")
                    with open("saves/music_sound_volume.txt", "w") as volume_file:
                        volume_file.write(str(self.music_volume) + "\n" + str(self.sound_volume))

                if self.sound_rod_border.collidepoint(mouse_pos):
                    if first_click:
                        self.select_sound.play()

                    self.sound_rod.width = mouse_pos[0] - (SIZE[0] // 2 - 50)
                    self.sound_volume = self.sound_rod.width / 200 * 100

                    self.game.player.set_sound(self.sound_volume / 100)

                    self.select_sound.set_volume(self.sound_volume / 100)
                    self.percentage_sound_text.change_text(str(int(self.sound_volume)) + "%")

                    with open("saves/music_sound_volume.txt", "w") as volume_file:
                        volume_file.write(str(self.music_volume) + "\n" + str(self.sound_volume))

                if self.reset_high_score_text.rect.collidepoint(pygame.mouse.get_pos()):
                    if first_click:
                        self.select_sound.play()
                        clicked_reset = True

                first_click = False

            else:
                first_click = True

            self.reset_high_score_text.color = "#b93535"
            self.reset_high_score_text.change_text("Reset high score", False)
            reset_popup_yes_text.color = "white"
            reset_popup_yes_text.change_text("Oui", False)
            reset_popup_no_text.color = "white"
            reset_popup_no_text.change_text("Non", False)

            if self.reset_high_score_text.rect.collidepoint(pygame.mouse.get_pos()):
                self.reset_high_score_text.color = "#ff2b2b"
                self.reset_high_score_text.change_text("Reset high score", False)

            if reset_popup_yes_text.rect.collidepoint(pygame.mouse.get_pos()) and clicked_reset:
                if pygame.mouse.get_pressed()[0]:
                    self.select_sound.play()
                    with open("saves/score.txt", "w") as fichier:
                        fichier.write("0")
                    self.game.high_score = 0
                    clicked_reset = False

                reset_popup_yes_text.color = "orange"
                reset_popup_yes_text.change_text("Oui", False)

            elif reset_popup_no_text.rect.collidepoint(pygame.mouse.get_pos()) and clicked_reset:
                if pygame.mouse.get_pressed()[0]:
                    self.select_sound.play()
                    clicked_reset = False

                reset_popup_no_text.color = "orange"
                reset_popup_no_text.change_text("Non", False)

            pygame.draw.rect(self.window, "#5a5a5a", self.music_rod, 0, 4)
            pygame.draw.rect(self.window, "white", self.music_rod_border, 3)

            pygame.draw.rect(self.window, "#5a5a5a", self.sound_rod, 0, 4)
            pygame.draw.rect(self.window, "white", self.sound_rod_border, 3)

            self.option_text_group.draw(self.window)

            if clicked_reset:
                option_text_group.draw(self.window)
            pygame.display.flip()

        self.inOptions = False

    def resizeAssets(self):
        # on charge les images à nouveau pour éviter des déformations à cause des rescale en boucle
        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()

        self.menu_image = pygame.transform.scale(self.menu_image, self.window.get_size())

        if self.inOptions:
            self.animationStartingOffset = 0
        else:
            self.animationStartingOffset = 1000

        self.positions = {
            "title": (self.window.get_width() // 2, self.window.get_height() // 7),
            "jouer": (self.window.get_width() // 2, int(self.window.get_height() / 2.4)),
            "cartes_text": (self.window.get_width() // 2, int(self.window.get_height() / 1.8)),
            "option_text": (self.window.get_width() // 2, int(self.window.get_height() / 1.6)),
            "music_text": (
                self.window.get_width() // 2 - 200 + self.animationStartingOffset,
                int(self.window.get_height() / 3.6),
            ),
            "sound_text": (
                self.window.get_width() // 2 - 200 + self.animationStartingOffset,
                int(self.window.get_height() / 1.8),
            ),
            "reset_high_score_text": (
                self.window.get_width() // 2 + self.animationStartingOffset,
                int(self.window.get_height() / 1.3),
            ),
            "percentage_music_text": (
                self.window.get_width() // 2 + 200 + 70 + self.animationStartingOffset,
                int(self.window.get_height() / 3.6) - 25,
            ),
            "percentage_sound_text": (
                self.window.get_width() // 2 + 200 + 70 + self.animationStartingOffset,
                int(self.window.get_height() / 1.8) - 25,
            ),
            "music_rod": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 3.6) - 25 // 2,
            ),
            "music_rod_border": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 3.6) - 25 // 2,
            ),
            "sound_rod": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 1.85),
            ),
            "sound_rod_border": (
                self.window.get_width() // 2 - 50 + self.animationStartingOffset,
                round(self.window.get_height() / 1.85),
            ),
        }

        self.title.rect.center = self.positions["title"]
        self.jouer.rect.center = self.positions["jouer"]
        self.option_text.rect.center = self.positions["option_text"]
        self.music_text.rect.center = self.positions["music_text"]
        self.sound_text.rect.center = self.positions["sound_text"]
        self.reset_high_score_text.rect.center = self.positions["reset_high_score_text"]
        self.music_rod.center = self.positions["music_rod"]
        self.music_rod_border.center = self.positions["music_rod_border"]
        self.sound_rod.center = self.positions["sound_rod"]
        self.sound_rod_border.center = self.positions["sound_rod_border"]

        self.percentage_music_text.rect.center = self.positions["percentage_music_text"]
        self.percentage_sound_text.rect.center = self.positions["percentage_sound_text"]

        if self.inOptions:
            self.animationStartingOffset = 0
        else:
            self.animationStartingOffset = 1000

        ### Resize of Game assets
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pressed = True

                if event.type == pygame.WINDOWRESIZED:
                    self.resizeAssets()
                    self.game.player.width = self.window.get_width()
                    self.game.player.height = self.window.get_height()

            self.jouer.color = "white"
            self.jouer.change_text("Jouer", False)
            self.option_text.color = "white"
            self.option_text.change_text("Options", False)

            if self.jouer.rect.collidepoint(pygame.mouse.get_pos()):
                self.jouer.color = "orange"
                self.jouer.change_text("Jouer", False)
                if pressed:
                    self.select_sound.play()
                    self.game.reset_game()
                    self.game.run()

            elif self.option_text.rect.collidepoint(pygame.mouse.get_pos()):
                self.option_text.color = "orange"
                self.option_text.change_text("Options", False)
                if pressed:
                    self.select_sound.play()
                    self.option()

            self.menu_text_group.draw(self.window)
            pygame.display.update()

            self.clock.tick(60)
