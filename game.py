import pygame

# from player import Player
from player2 import Player
from ennemis import *
from random import randint
from projectiles import Projectiles
from math import radians, sin, cos, acos, asin, degrees

pygame.init()


class Game:
    def __init__(self, size, title):
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        self.background = pygame.image.load("image/Space Background2.png")

        self.center_square = pygame.rect.Rect(
            (0, 0, size[0] // 3, size[1] // 3))  # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square.center = (size[0] // 2, size[1] // 2)  # on place le carré au centre de l'écran
        self.score = 1000
        self.high_score = 0
        self.ariel = pygame.font.SysFont("Comic Sans MS", 30)  # on créer la police de caractère ariel

        self.score_text1_surface = self.ariel.render("score", False, "white")  # le texte à afficher
        self.score_text1_rect = self.score_text1_surface.get_rect()  # le rectangle pour avoir la position du text
        self.score_text1_rect.topright = self.center_square.topright  # on place le text dans l'angle en haut à droite du rectangle
        self.score_text1_rect.x -= 10
        self.score_text1_rect.y += 10  # légère correction sur la position

        # on refait la même chose pour l'affichage de la valeur du score
        self.score_text2_surface = self.ariel.render(str(self.score), False, "white")
        self.score_text2_rect = self.score_text2_surface.get_rect()
        self.score_text2_rect.topright = self.score_text1_rect.bottomright

        self.sussy_walls = [pygame.rect.Rect(20, 20, self.size[0], 1)]

        self.projectile_list = []

        self.player = Player(100, 100, self.size, self.center_square)
        self.player_group = pygame.sprite.GroupSingle(self.player)  # on creer une instance du joueur
        self.ennemy_list = []

        # self.bg_musique = pygame.mixer.music.load("music/bgm_1.mp3")
        # pygame.mixer.music.play(10)

        self.clock = pygame.time.Clock()  # module pygame pour gérer le temps dans le jeu (notamment les fps)

    def draw(self):
        # on remplit la fenetre de noir à chaque tour de boucle pour effacer les éléments précédents
        self.window.fill("black")
        self.window.blit(self.background, (0, 0))

        pygame.draw.rect(self.window, "red", self.player.hitbox, 1)

        pygame.draw.rect(self.window, "white", self.center_square, 5)  # on affiche le rectangle central
        self.window.blit(self.score_text1_surface, self.score_text1_rect)  # on affiche le texte "score"
        self.window.blit(self.score_text2_surface, self.score_text2_rect)  # on affiche la valeur du score
        self.player_group.draw(self.window)  # affichage du joueur

        for i in range(len(self.ennemy_list)):
            if self.ennemy_list[i].alive:
                self.ennemy_list[i].draw()

        for proj in self.projectile_list:
            proj.draw()

    def update_ennemy(self):
        tmp = self.ennemy_list.copy()  # on copie self.ennemy_list pour pas retirer des éléments de la liste pendant qu'on bosse dessus
        a = 0  # a=nombre d'entités suprimées du tableau a ce parcours de self.ennemy_list
        for i in range(len(self.ennemy_list)):
            if self.ennemy_list[i].colide(self.player.x,self.player.y,20):#si l'objet est en colision avec le joueur a 20 px près
                self.ennemy_list[i].alive=False#alors on tue l'objet
            if self.ennemy_list[i].alive:
                self.ennemy_list[i].move()
            else:
                tmp.pop(
                    i - a)  # comme on retire des éléments, il faut se décaler pour suprimer l'élément qui correspond a self.ennemy_list[i]
                a += 1
        self.ennemy_list = tmp.copy()

    def run(self):
        continuer = True
        tu = pygame.display.get_window_size()

        for i in range(10):
            self.ennemy_list.append(mine(randint(0,tu[0]-10),randint(0,tu[1]-10),self.window))
        while continuer:
            # on récupère à chaque tour de boucle les touches enfoncées par le joueur
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    pass
                    if pygame.key.get_pressed()[pygame.K_z]:
                        self.projectile_list.append(
                            Projectiles(self.player.x, self.player.y, -90, self.size, self.window))

            # rotation du vaisseau (juste graphique pour l'instant
            if keys[pygame.K_RIGHT]:
                self.player.rotate("R")
            if keys[pygame.K_LEFT]:
                self.player.rotate("L")
            if keys[pygame.K_SPACE]:
                self.ennemy_list.append(
                    bull(self.player.x, self.player.y, self.player.x + cos(radians(self.player.angle)),
                         self.player.y + sin(radians(-self.player.angle)), self.window))
            if keys[pygame.K_UP]:
                self.player.move()
            else:
                if keys[pygame.K_SPACE]:
                    self.ennemy_list.append(
                        bull(self.player.x, self.player.y, self.player.x + cos(radians(self.player.angle)),
                             self.player.y + sin(radians(-self.player.angle)), self.window))

            # collision (TODO -> faire une fonction update ou on mettra les collisions et les trucs similaire)
            # self.player.collision_bord()
            # self.player.central_square_collision(self.center_square)

            # affichage des éléments graphiques
            self.update_ennemy()
            self.draw()

            self.player_group.update()

            # on update l'affichage
            pygame.display.flip()

            # on fait en sorte d'avoir 60 fps
            self.clock.tick(60)
