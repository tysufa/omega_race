import pygame
from math import sin, cos, radians
from constantes import *
from animation import Anim


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x, self.y = x, y
        self.direction = direction
        self.bullet_anim = Anim(self.x, self.y, 3, (8, 16), 50,
                                BULLET_SPRITESHEET, True)

        self.image = self.bullet_anim.image

        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.velocity = cos(radians(self.direction)) * BULLET_SPEED, sin(radians(self.direction)) * BULLET_SPEED

    def update(self):
        self.bullet_anim.show = True # on veut être sur d'afficher l'animation même une fois fini
        self.bullet_anim.angle = self.direction-90 # l'angle de la balle est dans la direction du joueur -90 degrées pour la tourner vers la droite comme le joueur au début de la partie

        self.rect.x += self.velocity[0] # on update la position x et y en fonction de la vélocité
        self.rect.y -= self.velocity[1]

        self.bullet_anim.update() # on update l'animation du tir
        self.image = self.bullet_anim.image # l'image actuelle du tir devient l'image de l'animation en cours