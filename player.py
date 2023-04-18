import pygame

pygame.init()


class Player:
    def __init__(self, window):
        self.window = window
        self.img_vaisseau = pygame.image.load("vaisseau-spatial.png")
        self.img_vaisseau = pygame.transform.scale(self.img_vaisseau, (32, 32)) # on redimmensionne l'image du vaisseau à une taille plus adaptée
        self.rotated_img = self.img_vaisseau # cette image est celle qui sera affichée
        self.vaisseau_rect = self.img_vaisseau.get_rect(center=(100, 100))
        self.angle = 0

    def draw(self, img, rect):
        self.window.blit(img, rect)

    def rotate(self, direction):
        self.rotated_img = pygame.transform.rotate(self.img_vaisseau, self.angle) # on tourne graphiquement l'image du vaisseau
        self.vaisseau_rect = self.rotated_img.get_rect(center=self.vaisseau_rect.center) # on change la position de la hitbox
        if direction == "R": # si on tourne vers la droite :
            self.angle -= 2.5
        else:
            self.angle += 2.5
