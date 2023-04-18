import pygame
from player import Player

pygame.init()


class Game:
    def __init__(self, size, title):
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.center_square = pygame.rect.Rect((0, 0, size[0]//3, size[1]//3)) # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square.center = (size[0]//2, size[1]//2) # on place le carré au centre de l'écran

        self.score = 100
        self.high_score = 0
        self.ariel = pygame.font.SysFont("Comic Sans MS", 30) # on créer la police de caractère ariel

        self.score_text1_surface = self.ariel.render("score", False, "white") # le texte à afficher
        self.score_text1_rect = self.score_text1_surface.get_rect() # le rectangle pour avoir la position du text
        self.score_text1_rect.topright = self.center_square.topright # on place le text dans l'angle en haut à droite du rectangle
        self.score_text1_rect.x -= 10; self.score_text1_rect.y += 10 # légère correction sur la position

        # on refait la même chose pour l'affichage de la valeur du score
        self.score_text2_surface = self.ariel.render(str(self.score), False, "white")
        self.score_text2_rect = self.score_text2_surface.get_rect()
        self.score_text2_rect.topright = self.score_text1_rect.bottomright

        self.clock = pygame.time.Clock()

    def draw(self):
        self.window.fill("black")
        pygame.draw.rect(self.window, "white", self.center_square, 5)
        self.window.blit(self.score_text1_surface, self.score_text1_rect)
        self.window.blit(self.score_text2_surface, self.score_text2_rect)

    def run(self):
        continuer = True
        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    pygame.quit()

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
