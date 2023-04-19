import pygame
from player import Player
from ennemis import *

pygame.init()

class Game:
    def __init__(self, size, title):
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.center_square = pygame.rect.Rect(
            (0, 0, size[0] // 3, size[1] // 3))  # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square.center = (size[0] // 2, size[1] // 2)  # on place le carré au centre de l'écran

        self.score = 100
        self.high_score = 0
        self.ariel = pygame.font.SysFont("Comic Sans MS", 30)  # on créer la police de caractère ariel

        self.score_text1_surface = self.ariel.render("score", False, "white")  # le texte à afficher
        self.score_text1_rect = self.score_text1_surface.get_rect()  # le rectangle pour avoir la position du text
        self.score_text1_rect.topright = self.center_square.topright  # on place le text dans l'angle en haut à droite du rectangle
        self.score_text1_rect.x -= 10;
        self.score_text1_rect.y += 10  # légère correction sur la position

        # on refait la même chose pour l'affichage de la valeur du score
        self.score_text2_surface = self.ariel.render(str(self.score), False, "white")
        self.score_text2_rect = self.score_text2_surface.get_rect()
        self.score_text2_rect.topright = self.score_text1_rect.bottomright

        self.player = Player(self.window, self.size) # on creer une instance du joueur
        self.ennemy_list=[]
        self.clock = pygame.time.Clock() # module pygame pour gérer le temps dans le jeu (notamment les fps)

    def draw(self):
        self.window.fill("black") # on remplit la fenetre de noir à chaque tour de boucle pour effacer les éléments précédents
        pygame.draw.rect(self.window, "white", self.center_square, 5) # on affiche le rectangle central
        self.window.blit(self.score_text1_surface, self.score_text1_rect) # on affiche le texte "score"
        self.window.blit(self.score_text2_surface, self.score_text2_rect) # on affiche la valeur du score
        self.player.draw() # affichage du joueur
        for i in range(len(self.ennemy_list)):
            if self.ennemy_list[i].alive:
                self.ennemy_list[i].draw()

    def update_ennemy(self):
        tmp=self.ennemy_list.copy()#on copie self.ennemy_list pour pas retirer des éléments de la liste pendant qu'on bosse dessus
        a=0#a=nombre d'entités suprimées du tableau a ce parcours de self.ennemy_list
        for i in range(len(self.ennemy_list)):
            if self.ennemy_list[i].alive:
                self.ennemy_list[i].moove()
            else :
                tmp.pop(i-a)#comme on retire des éléments, il faut se décaler pour suprimer l'élément qui correspond a self.ennemy_list[i]
                a+=1
        self.ennemy_list=tmp.copy()

    def run(self):
        continuer = True

        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    pygame.quit()

            # on récupère à chaque tour de boucle les touches enfoncées par le joueur
            keys = pygame.key.get_pressed()

            # rotation du vaisseau (juste graphique pour l'instant
            if keys[pygame.K_RIGHT]:
                self.player.rotate("R")
            if keys[pygame.K_LEFT]:
                self.player.rotate("L")
            if keys[pygame.K_UP]:
                self.player.move(True)
            else:
                self.player.move(False)

            # collision (TODO -> faire une fonction update ou on mettra les collisions et les trucs similaire)
            self.player.collision_bord()

            tu=pygame.display.get_window_size()
            self.ennemy_list.append(bull(tu[0]//2,tu[1]//2,self.player.x,self.player.y,self.window))

            # affichage des éléments graphiques
            self.update_ennemy()
            self.draw()
            # on update l'affichage
            pygame.display.flip()

            # on fait en sorte d'avoir 60 fps
            self.clock.tick(60)
