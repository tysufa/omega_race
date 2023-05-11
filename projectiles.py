import pygame
from math import sin, cos, radians, degrees, asin, acos
from constantes import *
from animation import Anim


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, rocket=False):
        super().__init__()
        self.x, self.y = x, y
        self.direction = direction
        self.rocket = rocket
        if not rocket:
            self.bullet_anim = Anim(self.x, self.y, 3, (8, 16), 50,
                                    BULLET_SPRITESHEET, True)
        else:
            self.bullet_anim = Anim(self.x, self.y, 5, (16, 32), 50,
                                    "image/Nautolan/Weapon Effects - Projectiles/Nautolan - Rocket.png", True)

        self.image = self.bullet_anim.image


        self.bullet_anim.angle = self.direction-90 # l'angle de la balle est dans la direction du joueur -90 degrées pour la tourner vers la droite comme le joueur au début de la partie


        self.hitbox = pygame.rect.Rect((self.x, self.y), (10, 10))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.velocity = [cos(radians(self.direction)) * BULLET_SPEED, sin(radians(self.direction)) * BULLET_SPEED]

    def update(self):
        if self.rocket:
            self.get_direction()
            self.velocity[1] = cos(radians(self.bullet_anim.angle)) * BULLET_SPEED
            self.velocity[0] = -sin(radians(self.bullet_anim.angle)) * BULLET_SPEED


        self.bullet_anim.show = True # on veut être sur d'afficher l'animation même une fois fini

        self.bullet_anim.update() # on update l'animation du tir

        self.image = self.bullet_anim.image # l'image actuelle du tir devient l'image de l'animation en cours

        self.x += self.velocity[0] # on update la position x et y en fonction de la vélocité
        self.y -= self.velocity[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hitbox.center = self.rect.center

    def rotation(self, xa, ya, xb, yb):
        """
        renvoie en degrés la rotation nescaissaire a l'objet (xa,ya) pour être tourné vers (xb,yb)
        """
        ret = degrees(acos((xb - xa) / ((xb - xa) ** 2 + (yb - ya) ** 2) ** (1 / 2)))
        if asin((yb - ya) / ((xb - xa) ** 2 + (yb - ya) ** 2) ** (1 / 2)) < 0:
            ret = -ret
        return ret

    def get_direction(self):
        pos = pygame.mouse.get_pos()

        self.bullet_anim.angle = self.bullet_anim.angle%360

        objectif = self.rotation(self.x, self.y, pos[0],pos[1])%360

        calcul_dirrection = (objectif + self.bullet_anim.angle)%360-90

        if calcul_dirrection > 0 and calcul_dirrection < 180:
            self.bullet_anim.angle += 3
        else:
            self.bullet_anim.angle -= 3


    