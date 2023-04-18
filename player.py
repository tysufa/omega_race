import pygame
from math import radians, cos, sin

pygame.init()


class Player:
    def __init__(self, window):
        self.window = window
        self.img_vaisseau = pygame.image.load("vaisseau-spatial.png")
        self.img_vaisseau = pygame.transform.scale(self.img_vaisseau, (
        32, 32))  # on redimmensionne l'image du vaisseau à une taille plus adaptée
        self.img_vaisseau = pygame.transform.rotate(self.img_vaisseau, -90)

        self.rotated_img = self.img_vaisseau  # cette image est celle qui sera affichée
        self.vaisseau_rect = self.img_vaisseau.get_rect(center=(100, 100))
        self.x = 100  # on garde nous même la position pour pouvoir travailler avec des entiers
        self.y = 100  # x et y gardent la position du centre de l'image du vaisseau (nécessaire pour la rotation)
        self.velocity = pygame.math.Vector2(3, 3)
        self.max_velocity = 8
        self.angle = 0

    def draw(self):
        self.window.blit(self.rotated_img, self.vaisseau_rect)
        pygame.draw.rect(self.window, "red", self.vaisseau_rect, 2)

    def rotate(self, direction):
        self.rotated_img = pygame.transform.rotate(self.img_vaisseau,
                                                   self.angle)  # on tourne graphiquement l'image du vaisseau
        self.vaisseau_rect = self.rotated_img.get_rect(
            center=(self.x, self.y))  # on change la position de la hitbox car elle c'est décalé en tournant
        # self.x, self.y = self.vaisseau_rect.topleft
        # self.x = self.vaisseau_rect.x
        # self.y = self.vaisseau_rect.y

        if direction == "R":  # si on tourne vers la droite :
            self.angle -= 7
        else:
            self.angle += 7

    def move(self):
        self.velocity = pygame.math.Vector2(cos(radians(self.angle)), -sin(radians(self.angle))) # update de la vélocité, -sin car si y est positif on va vers le haut
        self.x += self.velocity[0] * 3 # multiplication par 3 pour la vitesse (TODO -> changer 3 par une variable vitesse)
        self.y += self.velocity[1] * 3
        print(self.vaisseau_rect.bottom)
        self.vaisseau_rect = self.rotated_img.get_rect(center=(self.x, self.y)) # on ne peut pas directement modifier par rapport au centre du rect donc on récupère le rectangle à partir de l'image en modifiant la position centrale
        # self.vaisseau_rect.x = self.x
        # self.vaisseau_rect.y = self.y

    def collision_bord(self):
        if self.vaisseau_rect.top < 0:
            self.y -= self.velocity[1] * 3
        if self.vaisseau_rect.bottom > 480:
            self.y -= self.velocity[1] * 3
        if self.vaisseau_rect.left < 0:
            self.x -= self.velocity[0] * 3
        if self.vaisseau_rect.right > 720:
            self.x -= self.velocity[0] * 3
