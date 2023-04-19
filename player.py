import pygame
from math import radians, cos, sin

pygame.init()


class Player:
    def __init__(self, window, size):
        self.window = window
        self.size = size
        self.img_flamme  = pygame.image.load("image/feu.png")
        self.img_vaisseau = pygame.image.load("image/vaisseau-spatial.png")
        self.img_vaisseau = pygame.transform.scale(self.img_vaisseau, (32, 32))  # on redimmensionne l'image du vaisseau à une taille plus adaptée
        self.img_vaisseau = pygame.transform.rotate(self.img_vaisseau, -90)
        self.img_flamme = pygame.transform.rotate(self.img_flamme, 90)

        self.rotated_img = self.img_vaisseau  # cette image est celle qui sera affichée
        self.vaisseau_rect = self.img_vaisseau.get_rect(center=(100, 100))
        self.x = 100  # on garde nous même la position pour pouvoir travailler avec des entiers
        self.y = 100  # x et y gardent la position du centre de l'image du vaisseau (nécessaire pour la rotation)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0.2

        self.max_velocity = 30
        self.angle = 0

    def draw(self):
        self.window.blit(self.rotated_img, self.vaisseau_rect)
        # self.window.blit(self.img_flamme, self.vaisseau_rect)
        # pygame.draw.rect(self.window, "red", self.vaisseau_rect, 2)

    def rotate(self, direction):
        for i in range(5):
            self.rotated_img = pygame.transform.rotate(self.img_vaisseau, self.angle)  # on tourne graphiquement l'image du vaisseau
            self.vaisseau_rect = self.rotated_img.get_rect(center=(self.x, self.y))  # on change la position de la hitbox car elle c'est décalé en tournant
            self.vaisseau_rect.center=(self.x,self.y)

            if direction == "R":  # si on tourne vers la droite :
                self.angle -= 1
            else:
                self.angle += 1

    def move(self, acceleration):
        if acceleration:
            # update de la vélocité, -sin car si y est positif on va vers le haut
            if abs(self.velocity.x + cos(radians(self.angle))) < self.max_velocity:
                self.velocity.x += cos(radians(self.angle))

            if abs(self.velocity.y - sin(radians(self.angle))) < self.max_velocity:
                self.velocity.y -= sin(radians(self.angle))

        self.x += self.velocity.x * self.speed  # multiplication par 3 pour la vitesse (TODO -> changer 3 par une variable vitesse)
        self.y += self.velocity.y * self.speed

        self.vaisseau_rect = self.rotated_img.get_rect(center=(self.x, self.y))  # on ne peut pas directement modifier par rapport au centre du rect donc on récupère le rectangle à partir de l'image en modifiant la position centrale


    def collision_bord(self):
        if self.vaisseau_rect.top <= 0 or self.vaisseau_rect.bottom > self.size[1]:
            self.velocity.y = -self.velocity.y
        if self.vaisseau_rect.left < 0 or self.vaisseau_rect.right > self.size[0]:
            self.velocity.x = -self.velocity.x

    def central_square_collision(self, central_square):
        if self.vaisseau_rect.colliderect(central_square):
            if abs(self.vaisseau_rect.bottom - central_square.top) <= 10:
                self.velocity.y = -self.velocity.y
            elif abs(self.vaisseau_rect.top - central_square.bottom) <= 10:
                self.velocity.y = -self.velocity.y

            if abs(self.vaisseau_rect.right - central_square.left) <= 10:
                self.velocity.x = -self.velocity.x
            elif abs(self.vaisseau_rect.left - central_square.right) <= 10:
                self.velocity.x = -self.velocity.x
