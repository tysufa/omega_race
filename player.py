import pygame
from math import radians, cos, sin

pygame.init()


class Player:
    def __init__(self, window, size, sussy_walls=[]):
        self.window = window
        self.size = size
        self.img_vaisseau = pygame.image.load("image/Kla'ed - Fighter - Base.png")
        self.img_vaisseau = pygame.transform.scale(self.img_vaisseau, (80, 80))  # on redimmensionne l'image du vaisseau à une taille plus adaptée
        self.img_vaisseau = pygame.transform.rotate(self.img_vaisseau, -90)

        self.rotated_img = self.img_vaisseau  # cette image est celle qui sera affichée
        self.vaisseau_rect = self.img_vaisseau.get_rect(center=(100, 100))
        self.x = 100  # on garde nous même la position pour pouvoir travailler avec des entiers
        self.y = 100  # x et y gardent la position du centre de l'image du vaisseau (nécessaire pour la rotation)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0.2
        self.velocity_lost = 0.6

        self.max_velocity = 3
        self.angle = 0

        self.tempo = pygame.rect.Rect(0, 0, 32, 32)
        self.tempo_flamme = False

        self.affichage_sussy_walls = -1
        self.sussy_walls = sussy_walls

        self.t = pygame.time.get_ticks()
        self.a = 0

    def draw(self):

        #if self.tempo_flamme:
        #    self.img_vaisseau = pygame.image.load("image/vaisseau_avec_flamme.png")
        #    self.img_vaisseau = pygame.transform.scale(self.img_vaisseau, (32, 32))
        #    self.img_vaisseau = pygame.transform.rotate(self.img_vaisseau, -90)
        #else:
        #    self.img_vaisseau = pygame.image.load("image/vaisseau_sans_couille.png")
        #    self.img_vaisseau = pygame.transform.scale(self.img_vaisseau, (32, 32))
        #    self.img_vaisseau = pygame.transform.rotate(self.img_vaisseau, -90)

        self.rotate(None)  # on appel rotate simplement pour update rotated img (donc afficher ou pas le feu)

        self.window.blit(self.rotated_img, self.vaisseau_rect)
        # pygame.draw.rect(self.window, "red", self.vaisseau_rect, 2)
        # pygame.draw.rect(self.window, "red", self.tempo, 2)

        if self.affichage_sussy_walls != -1:
            self.a += 1
            pygame.draw.rect(self.window, "white", self.sussy_walls[self.affichage_sussy_walls])
            if self.a >= 15:
                self.affichage_sussy_walls = -1
                a = 0

    def rotate(self, direction):

        for i in range(5):
            if direction == "R":  # si on tourne vers la droite :
                self.angle -= 1
            elif direction == "L":
                self.angle += 1

            self.rotated_img = pygame.transform.rotate(self.img_vaisseau,
                                                       self.angle)  # on tourne graphiquement l'image du vaisseau
            # on change la position de la hitbox car elle c'est décalé en tournant
            self.vaisseau_rect = self.rotated_img.get_rect(center=(self.x, self.y))
            self.tempo = pygame.rect.Rect(0, 0, 32, 32)
            self.tempo.center = (self.x, self.y)

    def move(self, acceleration):
        self.tempo_flamme = False  # on considère qu'on accélère pas
        if acceleration:
            # on augmente la velicité que si elle ne dépasse pas la vélocité max
            if abs((self.velocity.x + cos(radians(self.angle))) * self.speed) < self.max_velocity:
                self.velocity.x += cos(radians(self.angle))

            if abs((self.velocity.y - sin(radians(self.angle))) * self.speed) < self.max_velocity:
                self.velocity.y -= sin(radians(self.angle))

            self.tempo_flamme = True  # si on accélère on affichera la flamme

        # on change les coordonnées en fonction de la velocité et de la vitesse qu'on veut pour notre joueur
        self.x += self.velocity.x * self.speed  # speed est là pour gérer l'accélération du joueur
        self.y += self.velocity.y * self.speed

        self.tempo = pygame.rect.Rect(0, 0, 32, 32)
        self.tempo.center = (self.x, self.y)

        # on ne peut pas directement modifier par rapport au centre du rect donc on récupère le rectangle à partir de l'image en modifiant la position centrale
        self.vaisseau_rect = self.rotated_img.get_rect(center=(self.x, self.y))

    def collision_bord(self):
        if self.tempo.top < 20:
            self.tempo.top = 21
            self.y = self.tempo.center[1]
            self.velocity.y *= -self.velocity_lost
            # self.velocity.x *= self.velocity_lost

        elif self.tempo.bottom > self.size[1] - 20:
            self.tempo.bottom = self.size[1] - 20
            self.y = self.tempo.center[1]
            self.velocity.y *= -self.velocity_lost
            # self.velocity.x *= self.velocity_lost

        elif self.tempo.left < 0:
            self.tempo.left = 0
            self.x = self.tempo.center[0]
            self.velocity.x *= -self.velocity_lost
            # self.velocity.y *= self.velocity_lost

        elif self.tempo.right > self.size[0]:
            self.tempo.right = self.size[0]
            self.x = self.tempo.center[0]
            self.velocity.x *= -self.velocity_lost
            # self.velocity.y *= self.velocity_lost

    def central_square_collision(self, central_square):
        if self.tempo.colliderect(central_square):
            if abs(self.tempo.bottom - central_square.top) <= self.max_velocity:
                self.tempo.bottom = central_square.top
                self.y = self.tempo.center[1]
                self.velocity.y *= -self.velocity_lost
                # self.velocity.x *= self.velocity_lost

            if abs(self.tempo.top - central_square.bottom) <= self.max_velocity:
                self.tempo.top = central_square.bottom
                self.y = self.tempo.center[
                             1] + 1  # droite et bas ne se comportent pas pareil que haut et gauche donc + 1
                self.velocity.y *= -self.velocity_lost
                # self.velocity.x *= self.velocity_lost

            if abs(self.tempo.right - central_square.left) <= self.max_velocity:
                self.tempo.right = central_square.left
                self.x = self.tempo.center[0]
                # self.velocity.y *= self.velocity_lost
                self.velocity.x *= -self.velocity_lost

            if abs(self.tempo.left - central_square.right) <= self.max_velocity:
                self.tempo.left = central_square.right
                self.x = self.tempo.center[0] + 1
                # self.velocity.y *= self.velocity_lost
                self.velocity.x *= -self.velocity_lost
