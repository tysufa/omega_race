import random
import pygame.time
from player import Player
from ennemis import *
from text import Text
from wall import Wall
from menu import Menu
from random import randint
from constantes import *
import csv

class Game:
    def __init__(self):
        self.game_over = False
        self.playing_music = False
        self.window = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(TITLE)

        self.background = pygame.image.load(BACKGROUND_IMAGE)
        self.game_over_image = pygame.image.load("image/GameOver(A)@2x.png")

        # 255 = 1.0 donc on garde la couleur de base de l'image et on mutliplie simplement le canal alpha : 1 * (160/255)
        # permet d'obtenir un arrière plan en parti transparent
        self.background.fill((255, 255, 255, 160), special_flags=BLEND_RGBA_MULT)

        # on créer une image pour le nombre de vies tourné vers la droite
        self.player_image = pygame.transform.rotate(pygame.image.load(PLAYER_IMAGE).convert_alpha(), -90)

        # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square = pygame.rect.Rect((0, 0, SIZE[0] // 3, SIZE[1] // 3))
        self.center_square.center = (SIZE[0] // 2, SIZE[1] // 2)  # on place le carré au centre de l'écran

        self.score = 0
        with open("score.txt", "r") as fichier:
            self.high_score = int(fichier.readline())

        # les 4 textes à afficher pour score et high score
        text1 = Text("score", 24, self.center_square.right - 5, self.center_square.top, "white")
        self.score_text = Text(str(self.score), 24, self.center_square.right - 5, text1.rect.bottom, "white")
        text3 = Text("high score", 24, self.center_square.right - 5, self.score_text.rect.bottom, "white")
        text4 = Text(str(self.high_score), 24, self.center_square.right - 5, text3.rect.bottom,
                     "white")

        # on créer un groupe qui contient les sprites de text
        self.text_group = pygame.sprite.Group(text1, self.score_text, text3, text4)

        ##### walls ######
        top_wall = Wall(WALL_DISTANCE, WALL_DISTANCE, SIZE[0] - WALL_DISTANCE * 2, 1, 1, "white")
        right_wall = Wall(SIZE[0] - WALL_DISTANCE, WALL_DISTANCE, 1, SIZE[1] - WALL_DISTANCE * 2, 1, "white")
        down_wall = Wall(WALL_DISTANCE, SIZE[1] - WALL_DISTANCE, SIZE[0] - WALL_DISTANCE * 2, 1, 1, "white")
        left_wall = Wall(WALL_DISTANCE, WALL_DISTANCE, 1, SIZE[1] - WALL_DISTANCE * 2, 1, "white")

        self.walls = pygame.sprite.Group(top_wall, right_wall, down_wall, left_wall)

        self.particles = []

        self.ennemis = Ennemy_list()
        self.starting_ennemis_number = 1

        #### Levels ####
        self.level=1
        self.levels=[]
        import csv
        with open("levels.csv", "r") as fichier:
            ligne = csv.reader(fichier, delimiter=',', quotechar='|')
            for case in ligne :
                self.levels.append(case)
        self.levels.pop(0)
        for i in range(len(self.levels)):
            self.levels[i].pop(0)
            for j in range(len(self.levels[i])):
                self.levels[i][j]=int(self.levels[i][j])
        ####
        self.player = Player(PLAYER_INITIAL_POSITION[0], PLAYER_INITIAL_POSITION[1], self.center_square,
                             self.ennemis.tab)

        self.player_group = pygame.sprite.Group()  # on creer une instance du joueur
        self.player_group.add(self.player)

        self.in_menu = False
        self.menu = Menu(self.window)

        self.test = 0
        self.test2 = False

        pygame.mixer.music.set_volume(0.4)
        self.clock = pygame.time.Clock()


    def wall_collisions(self):
        for wall in self.walls:
            if self.player.hitbox.colliderect(wall.rect):
                wall.show()

    def spawn(self,level):#self.levels[self.level-1]
        spawnbox = pygame.rect.Rect((self.player.x, self.player.y), PLAYER_SAFE_SPAWN_ZONE)
        spawnbox.center = self.player.hitbox.center
        for i in range (len(level)):
            ennemis_apparus=0
            while ennemis_apparus < level[i]:
                if i==0:
                    self.ennemis.tab.append(Mine(randint(40, SIZE[0] - 40), randint(40, SIZE[1] - 40), self.window, self.center_square))
                elif i==1:
                    self.ennemis.tab.append(Asteroid(randint(40, SIZE[0] - 40), randint(40, SIZE[1] - 40), self.window, self.center_square))
                elif i==2:
                    self.ennemis.tab.append(Chargeur(randint(40, SIZE[0] - 40), randint(40, SIZE[1] - 40), self.window, self.center_square))
                elif i==3:
                    self.ennemis.tab.append(Tourelle(randint(40, SIZE[0] - 40), randint(40, SIZE[1] - 40), self.window, self.center_square))
                elif i==4:
                    self.ennemis.tab.append(Miner(randint(40, SIZE[0] - 40), randint(40, SIZE[1] - 40), self.window, self.center_square))
                elif i==5:
                    self.ennemis.tab.append(Tourelle(randint(40, SIZE[0] - 40), randint(40, SIZE[1] - 40), self.window, self.center_square,True))
                spawncenter = pygame.rect.Rect((self.center_square.x, self.center_square.y), (
                self.center_square.width + self.ennemis.tab[-1].hitbox.width,
                self.center_square.height + self.ennemis.tab[-1].hitbox.height))
                spawncenter.center = self.center_square.center
                if self.ennemis.tab[-1].colide(spawnbox) or self.ennemis.tab[-1].colide(spawncenter):
                    self.ennemis.tab[-1].alive = False
                    self.ennemis.tab.pop(-1)
                else:
                    ennemis_apparus+=1


    def update(self):
        if not self.game_over:
            self.player_group.update(self.window)  # on continue à l'update pour savoir quand il doit respawn (on fait le calcul dans player)
            if self.player.alive:
                self.player.ennemis = self.ennemis.tab
                self.walls.update()

                particule_copy = [particle for particle in self.particles if particle.radius > 0]
                self.particles = particule_copy


                self.score = self.ennemis.update(self.player, self.player.projectiles, self.score)

                particule_copy = [particle for particle in self.player.particles if particle.radius > 0]
                self.player.particles = particule_copy


                for particle in self.player.particles:
                    particle.update()
                for particle in self.ennemis.particle_list:
                    particle.update()


                if len(self.ennemis.tab) == 0 or self.ennemis.only_bullet:
                    self.level+=1
                    self.player.respawn_function()
                    self.respawn()

                if self.test2:
                    if pygame.time.get_ticks() - self.test > 75 and pygame.time.get_ticks() - self.test < 1000:
                        pygame.time.delay(1000)

            else:
                self.respawn()
                self.test = pygame.time.get_ticks()

            self.score_text.change_text(str(self.score))

    def decompter (self):
        ret=[0 for i in range(6)]
        for en in self.ennemis.tab :
            if type(en)==Mine:
                ret[0]+=1
            if type(en)==Asteroid:
                ret[1]+=1
            if type(en)==Chargeur:
                ret[2]+=1
            if type(en)==Tourelle:
                if en.shield:
                    ret[5]+=1
                else:
                    ret[3]+=1
            if type(en)==Miner:
                ret[4]+=1
        return ret

    def respawn(self):
        if self.player.nb_life >= 0:
            if self.player.respawn:
                if len(self.ennemis.tab) == 0 or self.ennemis.only_bullet:
                    self.ennemis = Ennemy_list()
                    self.spawn(self.levels[self.level-1])
                else:
                    tempo_level=self.decompter()
                    self.ennemis = Ennemy_list()
                    self.spawn(tempo_level)
                self.player.respawn = False
                self.player.alive = True
                self.player.projectiles = pygame.sprite.Group()
                self.test = pygame.time.get_ticks()
                self.test2 = True
        else:
            self.game_over = True

            # on update le meilleur score
            if self.high_score < self.score:
                with open("score.txt", "w") as fichier:
                    fichier.write(str(self.score))

    def draw(self):
        if not self.in_menu:
            self.window.blit(self.background, (0, 0))

            for i in range(self.player.nb_life):
                # on affiche un vaisseau pour chaque vie du personnage
                self.window.blit(self.player_image, (self.center_square.left, self.center_square.top + i * 50))

            for wall in self.walls.sprites():
                if wall.displayed:
                    wall.draw(self.window)

            self.player.player_anim.draw(self.window)
            if self.player.alive:
                self.player_group.draw(self.window)

            self.ennemis.draw()
            self.player.projectiles.draw(self.window)

            self.text_group.draw(self.window)  # on affiche l'ensemble des sprites Text dans text_group

            for particle in self.player.particles:
                pygame.draw.circle(self.window, "white", (particle.x, particle.y), particle.radius)
            for particle in self.ennemis.particle_list:
                pygame.draw.circle(self.window, "white", (particle.x, particle.y), particle.radius)

            pygame.draw.rect(self.window, "white", self.center_square, 2)  # rectangle du milieu

        else:
            self.window.fill(LIGHT_GREY)  # on remplit l'image de gris
            self.window.blit(self.background, (0, 0))  # on applique le fond transparent par dessus le fond gris
            self.menu.draw()

        if self.game_over:
            self.window.blit(self.game_over_image, (0, 0))


    def menu_loop(self):
        if self.menu.menu_actions():
            pygame.mixer.music.unload()
            self.in_menu = False

    def game_loop(self):
        keys = pygame.key.get_pressed()

        self.update()
        self.wall_collisions()  # sert uniquement pour l'affichage des murs

        if keys[pygame.K_ESCAPE]:
            self.in_menu = True
        """
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(GAME_MUSIC)
            pygame.mixer.music.play(fade_ms=1000)"""

    def run(self):
        continuer = True
        self.spawn(self.levels[self.level-1])
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

            pygame.display.flip()

            self.clock.tick(60)
