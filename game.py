import random
import pygame.time
from player import Player
from ennemis import *
from text import Text
from wall import Wall
from random import randint
from constantes import *
import csv
import sys

class Game:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock
        self.playing_music = False
        self.window = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(TITLE)

        self.sound_volume = 1

        self.continuer = True

        self.backgrounds = ["image/background/Space Background(3).png", "image/background/Space Background.png", "image/background/Space Background2.png", "image/background/Space Background3.png", "image/background/Space Background4.png", "image/background/Space Background5.png"]

        self.background_img = pygame.image.load(random.choice(self.backgrounds))
        # 255 = 1.0 donc on garde la couleur de base de l'image et on mutliplie simplement le canal alpha : 1 * (160/255)
        # permet d'obtenir un arrière plan en parti transparent
        # self.background_img.fill((255, 255, 255, 150), special_flags=BLEND_RGBA_MULT)

        # on créer une image pour le nombre de vies tourné vers la droite
        self.player_image = pygame.transform.rotate(pygame.image.load(PLAYER_IMAGE).convert_alpha(), - 90)

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

        self.level_text = Text("niveau 1", 24, self.center_square.center[0], self.center_square.top + 5, "white")

        # on créer un groupe qui contient les sprites de text
        self.text_group = pygame.sprite.Group(text1, self.score_text, text3, text4, self.level_text)

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
        
        self.game_over = GameOver(self.window, self.clock)

        self.time_after_death = 0
        self.respawn_with_pause = False

        pygame.mixer.music.set_volume(0.4)

    def pause(self):
        continuer = True

        pause_text = Text("Pause", 80, 0, 0, "orange")
        pause_text.rect.center = SIZE[0]//2, SIZE[1]//2

        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        continuer = False

            self.window.blit(pause_text.image, pause_text.rect)
            pygame.display.flip()
    
    
    def reset_game(self):
        self.playing_music = False

        self.continuer = True

        self.background_img = pygame.image.load(random.choice(self.backgrounds))

        self.score = 0
        with open("score.txt", "r") as fichier:
            self.high_score = int(fichier.readline())

        self.ennemis = Ennemy_list()

        self.level=1
        self.level_text.change_text("Niveau " + str(self.level))
        
        self.player.nb_life = LIFE_NB
        self.player.alive = True
        self.player.explosion_anim.show = False
        self.player.respawn_function()
        
        self.spawn(self.levels[self.level-1])
        

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
            
            if self.respawn_with_pause:
                if pygame.time.get_ticks() - self.time_after_death > 75 and pygame.time.get_ticks() - self.time_after_death < 1000:
                    pygame.time.delay(1000)
            
        else:
            self.time_after_death = pygame.time.get_ticks() # on appelle cette ligne qu'une seule fois après la mort du joueur

        
        self.respawn() # le joueur ne respawn que si il est mort ou qu'on passe au niveau suivant

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
            if len(self.ennemis.tab) == 0 or self.ennemis.only_bullet:
                self.level+=1
                self.level_text.change_text("niveau " + str(self.level))
                self.ennemis = Ennemy_list()
                self.spawn(self.levels[self.level-1])
                self.player.respawn = True # le joueur doit respawn pour ne pas être à la même position qu'au niveau précédent

            if self.player.respawn:
                self.player.respawn_function() # on fait réaparaitre le joueur
                tempo_level=self.decompter()
                self.ennemis = Ennemy_list()
                self.spawn(tempo_level)

                self.player.respawn = False
                self.player.alive = True # si le joueur était mort après son respawn il est à nouveau vivant
                self.player.projectiles = pygame.sprite.Group() # on enlève tous les projectiles du joueur
                self.time_after_death = pygame.time.get_ticks()
                self.respawn_with_pause = True
        else:
            # on update le meilleur score
            if self.high_score < self.score:
                with open("score.txt", "w") as fichier:
                    fichier.write(str(self.score))
                    
            self.continuer = False
            self.game_over.run()



    def draw(self):
        self.window.blit(self.background_img, (0, 0))

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


    def game_loop(self):
        keys = pygame.key.get_pressed()

        self.update()
        self.wall_collisions()  # sert uniquement pour l'affichage des murs

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(GAME_MUSIC)
            pygame.mixer.music.play(fade_ms=1000)

    def run(self):
        while self.continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        self.pause()
            
            self.game_loop()
            if self.game_over.restart:
                self.reset_game()
                self.game_over.restart = False
                
            if self.continuer: # évite un clignement à l'écran quand on revient au menu après un game over
                self.draw()

            pygame.display.flip()

            self.clock.tick(60)
            

class GameOver:
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock

        self.rejouer = Text("Rejouer", 60, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.rejouer.rect.center = SIZE[0] // 2, SIZE[1] // 2 - 70

        self.menu = Text("Menu", 60, SIZE[0] // 2, SIZE[1] // 2, "white")
        self.menu.rect.center = SIZE[0] // 2, SIZE[1] // 2 + 70

        self.text_group = pygame.sprite.Group(self.rejouer, self.menu)

        self.select_sound = pygame.mixer.Sound("sound/select.wav")

        self.menu_image = pygame.image.load("image/background/menu_background.png").convert_alpha()
        
        self.restart = False

        pygame.mixer.music.load(MENU_MUSIC)

        
        
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
                    
            self.rejouer.color = "white"
            self.rejouer.change_text("Rejouer", False)
            self.menu.color = "white"
            self.menu.change_text("Menu", False)
            
                    
            if self.rejouer.rect.collidepoint(pygame.mouse.get_pos()):
                self.rejouer.color = "orange"
                self.rejouer.change_text("Rejouer", False)
                if pressed:
                    self.select_sound.play()
                    self.restart = True
                    continuer = False

            elif self.menu.rect.collidepoint(pygame.mouse.get_pos()):
                self.menu.color = "orange"
                self.menu.change_text("Menu", False)
                if pressed:
                    self.select_sound.play()
                    continuer = False
            
            self.text_group.draw(self.window)
            pygame.display.update()


            self.clock.tick(60)

