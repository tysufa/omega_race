import pygame

pygame.init()


class Game:
    def __init__(self, size, title):
        self.size = size
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.center_square = pygame.rect.Rect((0, 0, size[0]//3, size[1]//3)) # on fait le carré principale en fonction de la taille de la fenetre
        self.center_square.center = (size[0]//2, size[1]//2) # on place le carré au centre de l'écran

        self.clock = pygame.time.Clock()

    def draw(self):
        self.window.fill("black")
        pygame.draw.rect(self.window, "white", self.center_square, 5)

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
