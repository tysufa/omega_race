import pygame.time

from player2 import Player, PlayerAnim
from ennemis import *
from text import Text
from wall import Wall


class Game:
    def __init__(self, size, title):
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        self.background = pygame.image.load("image/Space Background2.png")

        # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square = pygame.rect.Rect((0, 0, size[0] // 3, size[1] // 3))
        self.center_square.center = (size[0] // 2, size[1] // 2)  # on place le carré au centre de l'écran

        self.score = 1000
        self.high_score = 0

        # les 4 textes à afficher pour score et high score
        text1 = Text("Comic Sans MS", "score", 24, self.center_square.right - 5, self.center_square.top, "white")
        text2 = Text("Comic Sans MS", str(self.score), 24, self.center_square.right - 5, text1.rect.bottom, "white")
        text3 = Text("Comic Sans MS", "high score", 24, self.center_square.right - 5, text2.rect.bottom, "white")
        text4 = Text("Comic Sans MS", str(self.high_score), 24, self.center_square.right - 5, text3.rect.bottom,
                     "white")

        # on créer un groupe qui contient les sprites de text
        self.text_group = pygame.sprite.Group(text1, text2, text3, text4)

        ##### walls ######
        top_wall = Wall(20, 20, self.size[0] - 40, 1, 1, "white")
        right_wall = Wall(self.size[0] - 20, 20, 1, self.size[1] - 40, 1, "white")
        down_wall = Wall(20, self.size[1] - 20, self.size[0] - 40, 1, 1, "white")
        left_wall = Wall(20, 20, 1, self.size[1] - 40, 1, "white")

        self.walls = pygame.sprite.Group(top_wall, right_wall, down_wall, left_wall)

        ####

        self.player = Player(200, 200, self.size, self.center_square, self.walls)

        self.player_group = pygame.sprite.Group()  # on creer une instance du joueur
        self.player_group.add(self.player)

        self.clock = pygame.time.Clock()

    def wall_collisions(self):
        for wall in self.walls:
            if self.player.hitbox.colliderect(wall.rect):
                wall.show()

    def sprites_update(self):
        self.player_group.update()
        self.walls.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))

        for wall in self.walls.sprites():
            if wall.displayed:
                wall.draw(self.window)

        self.player.player_anim.draw(self.window)
        if self.player.alive:
            self.player_group.draw(self.window)
        self.text_group.draw(self.window)  # on affiche l'ensemble des sprites Text dans text_group

        pygame.draw.rect(self.window, "white", self.center_square, 2)  # rectangle du milieu

        pygame.display.flip()

    def run(self):
        continuer = True

        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False

            self.sprites_update()
            self.wall_collisions() # sert uniquement pour l'affichage des murs
            self.draw()

            self.clock.tick(60)
