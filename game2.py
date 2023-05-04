import pygame.time
from player2 import Player
from ennemis import *
from text import Text
from wall import Wall
from menu import Menu
from random import randint
from constantes import *


class Game:
    def __init__(self, size, title):
        self.playing_music = False
        self.window = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(title)

        self.background = pygame.image.load(BACKGROUND_IMAGE)

        # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square = pygame.rect.Rect((0, 0, SIZE[0] // 3, SIZE[1] // 3))
        self.center_square.center = (SIZE[0] // 2, SIZE[1] // 2)  # on place le carré au centre de l'écran

        self.score = 1000
        self.high_score = 0

        # les 4 textes à afficher pour score et high score
        text1 = Text(GAME_FONT, "score", 24, self.center_square.right - 5, self.center_square.top, "white")
        text2 = Text(GAME_FONT, str(self.score), 24, self.center_square.right - 5, text1.rect.bottom, "white")
        text3 = Text(GAME_FONT, "high score", 24, self.center_square.right - 5, text2.rect.bottom, "white")
        text4 = Text(GAME_FONT, str(self.high_score), 24, self.center_square.right - 5, text3.rect.bottom,
                     "white")

        # on créer un groupe qui contient les sprites de text
        self.text_group = pygame.sprite.Group(text1, text2, text3, text4)

        ##### walls ######
        top_wall = Wall(WALL_DISTANCE, WALL_DISTANCE, SIZE[0] - WALL_DISTANCE*2, 1, 1, "white")
        right_wall = Wall(SIZE[0] - WALL_DISTANCE, WALL_DISTANCE, 1, SIZE[1] - WALL_DISTANCE*2, 1, "white")
        down_wall = Wall(10, SIZE[1] - WALL_DISTANCE, SIZE[0] - WALL_DISTANCE*2, 1, 1, "white")
        left_wall = Wall(WALL_DISTANCE, WALL_DISTANCE, 1, SIZE[1] - WALL_DISTANCE*2, 1, "white")

        self.walls = pygame.sprite.Group(top_wall, right_wall, down_wall, left_wall)

        self.ennemis = Ennemy_list()

        ####

        self.player = Player(PLAYER_INITIAL_POSITION[0], PLAYER_INITIAL_POSITION[1], SIZE, self.center_square)

        self.player_group = pygame.sprite.Group()  # on creer une instance du joueur
        self.player_group.add(self.player)

        self.in_menu = False
        self.menu = Menu(self.window)

        pygame.mixer.music.load(GAME_MUSIC)

        self.clock = pygame.time.Clock()

    def wall_collisions(self):
        for wall in self.walls:
            if self.player.hitbox.colliderect(wall.rect):
                wall.show()

    def spawn(self):
        while len(self.ennemis.tab)<10:
            self.ennemis.tab.append(Bull(randint(40,SIZE[0]-40),randint(40,SIZE[1]-40),self.window,self.center_square))
            spawnbox = pygame.rect.Rect((self.player.x,self.player.y), PLAYER_SAFE_SPAWN_ZONE) 
            spawnbox.center=self.player.hitbox.center
            spawncenter = pygame.rect.Rect((self.center_square.x,self.center_square.y),(self.center_square.width+self.ennemis.tab[-1].hitbox.width,self.center_square.height+self.ennemis.tab[-1].hitbox.height))
            spawncenter.center=self.center_square.center
            if self.ennemis.tab[-1].colide(spawnbox) or self.ennemis.tab[-1].colide(spawncenter) :
                self.ennemis.tab[-1].alive=False
                self.ennemis.tab.pop(-1)

    def update(self):
        self.player_group.update()
        self.walls.update()
        self.ennemis.update(self.player, self.player.projectiles)

    def draw(self):
        self.window.blit(self.background, (0, 0))
        if not self.in_menu:
            for wall in self.walls.sprites():
                if wall.displayed:
                    wall.draw(self.window)

            self.player.player_anim.draw(self.window)
            if self.player.alive:
                self.player_group.draw(self.window)

            self.ennemis.draw()


            self.text_group.draw(self.window)  # on affiche l'ensemble des sprites Text dans text_group

            pygame.draw.rect(self.window, "white", self.center_square, 2)  # rectangle du milieu
            self.player.projectiles.draw(self.window)

        else:
            self.menu.draw()

        pygame.display.flip()

    def menu_loop(self):
        if self.menu.menu_actions():
            self.in_menu = False

    def game_loop(self):
        keys = pygame.key.get_pressed()

        self.update()
        self.wall_collisions()  # sert uniquement pour l'affichage des murs

        if keys[pygame.K_ESCAPE]:
            self.in_menu = True

        if not self.playing_music:
            pygame.mixer.music.play(10, fade_ms=0)
            self.playing_music = True

    def run(self):
        continuer = True
        self.spawn()
        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    pygame.quit()
                    exit()

            if self.in_menu:
                self.menu_loop()
            else:
                self.game_loop()

            self.draw()

            self.clock.tick(60)
